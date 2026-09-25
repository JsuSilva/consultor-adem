"""
Operações do Google Ads: leitura (contas, relatório), escrita sem gasto (campanha pausada,
conversão, pausar) e escrita que libera gasto (ativar, orçamento — sempre com as travas de
travas.py, incluindo o teto somado das campanhas ativas).

Padrões (regra, aprovados pelo consultor):
- conversão medida pela tag no site, contagem "uma por clique"; tipo site = visita a página
  (PAGE_VIEW), whatsapp = CONTACT, formulario = SUBMIT_LEAD_FORM;
- parceiros de pesquisa desligados, salvo `"parceiros_de_pesquisa": true` no JSON da campanha;
- grupo e anúncio nascem ATIVOS sob a campanha PAUSADA — quem segura o gasto é a campanha.
"""
import json
import os
import sys
import time

import auth
import travas
from config import RAIZ, CONFIG

PERIODOS = {
    "hoje": "TODAY",
    "ontem": "YESTERDAY",
    "7d": "LAST_7_DAYS",
    "14d": "LAST_14_DAYS",
    "30d": "LAST_30_DAYS",
    "mes": "THIS_MONTH",
    "mes-passado": "LAST_MONTH",
}

CORRESPONDENCIA = {"exata": "EXACT", "frase": "PHRASE", "ampla": "BROAD"}

# Regra: tipo pedido → categoria da ação de conversão (todas medidas pela tag no site).
CONVERSOES = {
    "formulario": "SUBMIT_LEAD_FORM",   # envio de formulário de contato/lead
    "whatsapp": "CONTACT",              # clique no botão/link de WhatsApp do site
    "site": "PAGE_VIEW",                # visita a uma página (ex.: página de obrigado)
}


# ---------------------------------------------------------------- utilitários

def _consultar(client, cid, gaql):
    svc = client.get_service("GoogleAdsService")
    return list(svc.search(customer_id=cid, query=gaql))


def _moeda(client, cid):
    linhas = _consultar(client, cid,
                        "SELECT customer.currency_code, customer.descriptive_name FROM customer")
    c = linhas[0].customer
    return c.currency_code, c.descriptive_name


def _tabela(cabecalho, linhas):
    larg = [max(len(str(x)) for x in col) for col in zip(cabecalho, *linhas)]
    fmt = "  ".join("{:<%d}" % w for w in larg)
    print(fmt.format(*cabecalho))
    print("  ".join("-" * w for w in larg))
    for ln in linhas:
        print(fmt.format(*[str(x) for x in ln]))


_CAMPOS_CAMPANHA = """
        SELECT campaign.id, campaign.name, campaign.status, campaign.resource_name,
               campaign.advertising_channel_type,
               campaign_budget.resource_name, campaign_budget.amount_micros,
               campaign_budget.explicitly_shared
        FROM campaign"""


def _campanha(client, cid, campanha_id):
    if not str(campanha_id).isdigit():
        sys.exit(f"ERRO: --campanha-id deve ser numérico; veio {campanha_id!r}.")
    linhas = _consultar(client, cid, f"{_CAMPOS_CAMPANHA} WHERE campaign.id = {campanha_id}")
    if not linhas:
        sys.exit(f"ERRO: campanha {campanha_id} não encontrada na conta {cid}.")
    return linhas[0]


def _campanha_por_nome(client, cid, nome):
    esc = nome.replace("\\", "\\\\").replace("'", "\\'")
    linhas = _consultar(client, cid, f"""{_CAMPOS_CAMPANHA}
        WHERE campaign.name = '{esc}' AND campaign.status != 'REMOVED'""")
    if not linhas:
        sys.exit(f"ERRO: nenhuma campanha com o nome exato {nome!r} na conta {cid}.")
    if len(linhas) > 1:
        ids = ", ".join(str(r.campaign.id) for r in linhas)
        sys.exit(f"ERRO: {len(linhas)} campanhas com o nome {nome!r} (ids {ids}). "
                 "Use --campanha-id.")
    return linhas[0]


def _ativas(client, cid):
    """Orçamentos das campanhas ENABLED, um por orçamento (compartilhado conta uma vez).

    Devolve (soma_brl, {chave_do_orcamento: brl}, n_campanhas_ativas).
    """
    linhas = _consultar(client, cid, """
        SELECT campaign.id, campaign_budget.resource_name, campaign_budget.amount_micros
        FROM campaign WHERE campaign.status = 'ENABLED'""")
    orcs = {}
    for r in linhas:
        chave = r.campaign_budget.resource_name or f"campanha:{r.campaign.id}"
        orcs[chave] = travas.de_micros(r.campaign_budget.amount_micros)
    return sum(orcs.values()), orcs, len(linhas)


def _quadro(client, cid, orc_rn, pedido, troca):
    """Soma resultante das ativas com o orçamento `pedido`.

    troca=True (orcamento): se o orçamento `orc_rn` já está na soma, o valor atual sai e o
    pedido entra no lugar. troca=False (ativar/criar): se o orçamento já está na soma
    (compartilhado com campanha ativa), nada entra de novo.
    """
    soma, orcs, n = _ativas(client, cid)
    q = {"atual": soma, "pedido": pedido, "n_ativas": n, "descontado": 0.0, "nota": ""}
    if orc_rn and orc_rn in orcs:
        if troca:
            q["descontado"] = orcs[orc_rn]
            q["resultante"] = soma - orcs[orc_rn] + pedido
            q["nota"] = "este orçamento já é usado por campanha ativa: o valor atual é trocado"
        else:
            q["resultante"] = soma
            q["nota"] = ("orçamento compartilhado com campanha já ativa: já está na soma, "
                         "não conta em dobro")
    else:
        q["resultante"] = soma + pedido
    return q


# ---------------------------------------------------------------- leitura

def contas():
    client = auth.cliente()
    cid_config = None
    try:
        cid_config = travas.customer_id()
    except SystemExit:
        pass  # listar contas não depende da config
    nomes = client.get_service("CustomerService").list_accessible_customers().resource_names
    if not nomes:
        print("Nenhuma conta acessível com estas credenciais.")
        return
    linhas = []
    for rn in nomes:
        cid = rn.split("/")[-1]
        try:
            c = _consultar(client, cid, """SELECT customer.descriptive_name,
                customer.currency_code, customer.time_zone, customer.manager,
                customer.test_account FROM customer""")[0].customer
            tipo = "MCC" if c.manager else ("teste" if c.test_account else "anunciante")
            linhas.append([cid, c.descriptive_name, c.currency_code, c.time_zone, tipo])
        except Exception:  # conta listada, mas sem acesso direto (ex.: sob MCC)
            linhas.append([cid, "(sem acesso direto)", "-", "-", "-"])
    for ln in linhas:
        ln.append("← config" if ln[0] == cid_config else "")
    _tabela(["customer_id", "nome", "moeda", "fuso", "tipo", ""], linhas)


def relatorio(periodo=None, de=None, ate=None):
    cid = travas.customer_id()
    if de or ate:
        if not (de and ate):
            sys.exit("ERRO: use --de e --ate juntos (AAAA-MM-DD).")
        filtro = f"segments.date BETWEEN '{de}' AND '{ate}'"
        rotulo = f"{de} a {ate}"
    else:
        periodo = periodo or "7d"
        filtro = f"segments.date DURING {PERIODOS[periodo]}"
        rotulo = periodo
    client = auth.cliente()
    moeda, nome_conta = _moeda(client, cid)
    linhas = _consultar(client, cid, f"""
        SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros,
               metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM campaign
        WHERE {filtro} AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC""")
    print(f"Conta {cid} — {nome_conta} — período: {rotulo} — valores em {moeda}\n")
    if not linhas:
        print("Nenhuma campanha com dados no período (campanha sem impressão não aparece).")
        return
    tab, tot = [], {"impr": 0, "cliques": 0, "custo": 0.0, "conv": 0.0}
    for r in linhas:
        m = r.metrics
        custo = travas.de_micros(m.cost_micros)
        ctr = (m.clicks / m.impressions * 100) if m.impressions else 0
        cpc = (custo / m.clicks) if m.clicks else 0
        cpa = (custo / m.conversions) if m.conversions else None
        tab.append([r.campaign.id, r.campaign.name[:40], r.campaign.status.name,
                    f"{travas.de_micros(r.campaign_budget.amount_micros):.2f}",
                    m.impressions, m.clicks, f"{ctr:.2f}%", f"{cpc:.2f}", f"{custo:.2f}",
                    f"{m.conversions:.1f}", f"{cpa:.2f}" if cpa is not None else "-"])
        tot["impr"] += m.impressions
        tot["cliques"] += m.clicks
        tot["custo"] += custo
        tot["conv"] += m.conversions
    tab.append(["", "TOTAL", "", "", tot["impr"], tot["cliques"], "", "",
                f"{tot['custo']:.2f}", f"{tot['conv']:.1f}",
                f"{tot['custo'] / tot['conv']:.2f}" if tot["conv"] else "-"])
    _tabela(["id", "campanha", "status", "orç/dia", "impr.", "cliques", "CTR", "CPC méd.",
             "custo", "conv.", "custo/conv."], tab)


# ---------------------------------------------------------------- campanha (nasce PAUSADA)

def _ler_plano(arquivo):
    if not os.path.isfile(arquivo):
        sys.exit(f"ERRO: arquivo não encontrado: {arquivo}")
    with open(arquivo, encoding="utf-8") as f:
        p = json.load(f)
    erros = []

    def exige(cond, msg):
        if not cond:
            erros.append(msg)

    exige(isinstance(p.get("nome"), str) and p["nome"].strip(), "`nome` vazio")
    exige(isinstance(p.get("orcamento_diario_brl"), (int, float)),
          "`orcamento_diario_brl` precisa ser número")
    est = p.get("estrategia_lance")
    exige(est in ("cpc_manual", "maximizar_conversoes"),
          "`estrategia_lance` deve ser 'cpc_manual' ou 'maximizar_conversoes'")
    if est == "cpc_manual":
        exige(isinstance(p.get("cpc_max_brl"), (int, float)) and p["cpc_max_brl"] > 0,
              "`cpc_max_brl` obrigatório (> 0) com cpc_manual")
    for campo in ("geo_ids", "idioma_ids"):
        v = p.get(campo)
        exige(isinstance(v, list) and v and all(str(x).isdigit() for x in v),
              f"`{campo}` precisa ser lista de IDs numéricos (sem ele a campanha mira o mundo "
              "todo / todos os idiomas)")
    kws = p.get("palavras_chave") or []
    exige(kws, "`palavras_chave` vazio")
    for k in kws:
        if not isinstance(k, dict):
            erros.append(f"palavra-chave deve ser objeto {{texto, correspondencia}}: {k!r}")
            continue
        t = k.get("texto", "")
        exige(t and len(t) <= 80 and len(t.split()) <= 10,
              f"palavra-chave inválida (até 80 caracteres e 10 palavras): {t!r}")
        exige(k.get("correspondencia") in CORRESPONDENCIA,
              f"`correspondencia` de {t!r} deve ser exata, frase ou ampla")
    a = p.get("anuncio") or {}
    url = str(a.get("url_final") or "")
    exige(url.startswith("https://") or url.startswith("http://"), "`anuncio.url_final` inválida")
    tit, desc = a.get("titulos") or [], a.get("descricoes") or []
    exige(3 <= len(tit) <= 15, f"`anuncio.titulos`: de 3 a 15 (veio {len(tit)})")
    exige(2 <= len(desc) <= 4, f"`anuncio.descricoes`: de 2 a 4 (veio {len(desc)})")
    for t in tit:
        exige(isinstance(t, str) and 0 < len(t) <= 30, f"título vazio ou com mais de 30 caracteres: {t!r}")
    for d in desc:
        exige(isinstance(d, str) and 0 < len(d) <= 90, f"descrição vazia ou com mais de 90 caracteres: {d!r}")
    for c in ("caminho1", "caminho2"):
        exige(len(a.get(c) or "") <= 15, f"`anuncio.{c}` com mais de 15 caracteres")
    if erros:
        sys.exit("ERRO no arquivo da campanha:\n  - " + "\n  - ".join(erros))
    return p


def _montar_operacoes(client, cid, p):
    """Todas as operações num só pedido, ligadas por IDs temporários (negativos)."""
    ga = client.get_service("GoogleAdsService")
    enums = client.enums
    ops = []
    orc_rn = ga.campaign_budget_path(cid, "-1")
    camp_rn = ga.campaign_path(cid, "-2")
    grupo_rn = ga.ad_group_path(cid, "-3")
    carimbo = time.strftime("%Y%m%d-%H%M%S")

    op = client.get_type("MutateOperation")
    orc = op.campaign_budget_operation.create
    orc.resource_name = orc_rn
    orc.name = f"{p['nome']} — orçamento {carimbo}"
    orc.amount_micros = travas.micros(p["orcamento_diario_brl"])
    orc.delivery_method = enums.BudgetDeliveryMethodEnum.STANDARD
    orc.explicitly_shared = False
    ops.append(op)

    op = client.get_type("MutateOperation")
    c = op.campaign_operation.create
    c.resource_name = camp_rn
    c.name = p["nome"]
    c.status = enums.CampaignStatusEnum.PAUSED          # SEMPRE pausada
    c.advertising_channel_type = enums.AdvertisingChannelTypeEnum.SEARCH
    c.campaign_budget = orc_rn
    c.network_settings.target_google_search = True
    c.network_settings.target_search_network = bool(p.get("parceiros_de_pesquisa", False))
    c.network_settings.target_content_network = False
    c.network_settings.target_partner_search_network = False
    c.contains_eu_political_advertising = (
        enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING)
    if p["estrategia_lance"] == "cpc_manual":
        client.copy_from(c.manual_cpc, client.get_type("ManualCpc"))
    else:
        client.copy_from(c.maximize_conversions, client.get_type("MaximizeConversions"))
    ops.append(op)

    for geo in p["geo_ids"]:
        op = client.get_type("MutateOperation")
        cc = op.campaign_criterion_operation.create
        cc.campaign = camp_rn
        cc.location.geo_target_constant = f"geoTargetConstants/{geo}"
        ops.append(op)
    for idioma in p["idioma_ids"]:
        op = client.get_type("MutateOperation")
        cc = op.campaign_criterion_operation.create
        cc.campaign = camp_rn
        cc.language.language_constant = f"languageConstants/{idioma}"
        ops.append(op)

    op = client.get_type("MutateOperation")
    g = op.ad_group_operation.create
    g.resource_name = grupo_rn
    g.name = p.get("grupo_nome") or "Grupo 1"
    g.campaign = camp_rn
    g.type_ = enums.AdGroupTypeEnum.SEARCH_STANDARD
    g.status = enums.AdGroupStatusEnum.ENABLED     # quem segura o gasto é a campanha pausada
    if p["estrategia_lance"] == "cpc_manual":
        g.cpc_bid_micros = travas.micros(p["cpc_max_brl"])
    ops.append(op)

    for k in p["palavras_chave"]:
        op = client.get_type("MutateOperation")
        crit = op.ad_group_criterion_operation.create
        crit.ad_group = grupo_rn
        crit.status = enums.AdGroupCriterionStatusEnum.ENABLED
        crit.keyword.text = k["texto"]
        crit.keyword.match_type = getattr(enums.KeywordMatchTypeEnum,
                                          CORRESPONDENCIA[k["correspondencia"]])
        ops.append(op)

    a = p["anuncio"]
    op = client.get_type("MutateOperation")
    aga = op.ad_group_ad_operation.create
    aga.ad_group = grupo_rn
    aga.status = enums.AdGroupAdStatusEnum.ENABLED
    aga.ad.final_urls.append(a["url_final"])
    rsa = aga.ad.responsive_search_ad
    for t in a["titulos"]:
        ativo = client.get_type("AdTextAsset")
        ativo.text = t
        rsa.headlines.append(ativo)
    for d in a["descricoes"]:
        ativo = client.get_type("AdTextAsset")
        ativo.text = d
        rsa.descriptions.append(ativo)
    if a.get("caminho1"):
        rsa.path1 = a["caminho1"]
    if a.get("caminho2"):
        rsa.path2 = a["caminho2"]
    ops.append(op)
    return ops


def _resultados(resp):
    for r in resp.mutate_operation_responses:
        qual = type(r).pb(r).WhichOneof("response")
        if qual:
            print(f"  {getattr(r, qual).resource_name}")


def criar_campanha(arquivo, aplicar):
    p = _ler_plano(arquivo)
    cid = travas.customer_id()
    teto = travas.teto_brl()
    travas.dentro_do_teto(float(p["orcamento_diario_brl"]), teto)
    if p["estrategia_lance"] == "cpc_manual" and p["cpc_max_brl"] > p["orcamento_diario_brl"]:
        sys.exit("ERRO: `cpc_max_brl` maior que o orçamento diário.")
    client = auth.cliente()
    moeda, nome_conta = _moeda(client, cid)
    travas.exigir_brl(moeda)

    ops = _montar_operacoes(client, cid, p)
    q = _quadro(client, cid, None, float(p["orcamento_diario_brl"]), troca=False)
    a = p["anuncio"]
    print(f"Conta {cid} — {nome_conta}")
    print(f"Campanha de Pesquisa: {p['nome']}  (nasce PAUSADA)")
    print("Teto somado, se esta campanha fosse ativada hoje:")
    print(travas.texto_quadro(q, teto))
    if q["resultante"] > teto:
        print("  AVISO: passaria do teto — `ativar` vai recusar enquanto a soma não couber. "
              "Criar pausada não gasta.")
    print(f"Lance: {p['estrategia_lance']}  ·  locais: {p['geo_ids']}  ·  idiomas: "
          f"{p['idioma_ids']}  ·  parceiros de pesquisa: "
          f"{bool(p.get('parceiros_de_pesquisa', False))}")
    print(f"Palavras-chave ({len(p['palavras_chave'])}): "
          + ", ".join(f"{k['texto']} [{k['correspondencia']}]" for k in p["palavras_chave"]))
    print(f"Anúncio → {a['url_final']}")
    for t in a["titulos"]:
        print(f"  T: {t}")
    for d in a["descricoes"]:
        print(f"  D: {d}")
    print("Lembrete: os textos passam pela régua de "
          "conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md.\n")

    req = client.get_type("MutateGoogleAdsRequest")
    req.customer_id = cid
    req.mutate_operations.extend(ops)
    req.validate_only = not aplicar
    resp = client.get_service("GoogleAdsService").mutate(request=req)
    if not aplicar:
        print(f"SIMULAÇÃO OK: a API validou {len(ops)} operações; nada foi criado.\n"
              "Para criar (pausada), rode de novo com --aplicar.")
        return
    print("CRIADO (campanha PAUSADA — não gasta até `gads.py ativar`):")
    _resultados(resp)


# ---------------------------------------------------------------- conversão

def _gravar_conversao_principal(conv_id):
    if not os.path.exists(CONFIG):
        sys.exit("ERRO: config/consultor.json não existe (só o modelo). Rode a skill "
                 "`configuracao` antes; o id não foi gravado.")
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("anuncios", {}).setdefault("google", {})["conversao_principal"] = conv_id
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Gravado: anuncios.google.conversao_principal = {conv_id} em "
          f"{os.path.relpath(CONFIG, RAIZ)}")


def criar_conversao(nome, tipo, aplicar, gravar_principal):
    cid = travas.customer_id()
    client = auth.cliente()
    enums = client.enums
    op = client.get_type("ConversionActionOperation")
    ca = op.create
    ca.name = nome
    ca.type_ = enums.ConversionActionTypeEnum.WEBPAGE
    ca.category = getattr(enums.ConversionActionCategoryEnum, CONVERSOES[tipo])
    ca.status = enums.ConversionActionStatusEnum.ENABLED
    ca.counting_type = enums.ConversionActionCountingTypeEnum.ONE_PER_CLICK

    req = client.get_type("MutateConversionActionsRequest")
    req.customer_id = cid
    req.operations.append(op)
    req.validate_only = not aplicar
    print(f"Conta {cid} — ação de conversão '{nome}' (tipo: {tipo} → {CONVERSOES[tipo]}, "
          "medida pela tag no site, uma por clique)")
    resp = client.get_service("ConversionActionService").mutate_conversion_actions(request=req)
    if not aplicar:
        print("SIMULAÇÃO OK: nada foi criado. Para criar, rode de novo com --aplicar.")
        if gravar_principal:
            print("(--gravar-principal ignorado na simulação.)")
        return
    rn = resp.results[0].resource_name
    conv_id = rn.split("/")[-1]
    print(f"CRIADA: {rn}  (id {conv_id})")
    print("Próximo passo: instalar o evento dessa conversão no site junto com a tag do Google "
          "(ver .agents/skills/anuncios-google/SKILL.md).")
    if gravar_principal:
        _gravar_conversao_principal(conv_id)


# ---------------------------------------------------------------- gasto (confirmação por rodada)

def ativar(campanha_id):
    cid = travas.customer_id()
    teto = travas.teto_brl()
    client = auth.cliente()
    moeda, nome_conta = _moeda(client, cid)
    travas.exigir_brl(moeda)
    r = _campanha(client, cid, campanha_id)
    atual = travas.de_micros(r.campaign_budget.amount_micros)
    if r.campaign.status.name == "ENABLED":
        sys.exit(f"A campanha '{r.campaign.name}' já está ativa. Nada foi alterado.")
    travas.dentro_do_teto(atual, teto, "orçamento diário atual da campanha")
    q = _quadro(client, cid, r.campaign_budget.resource_name, atual, troca=False)
    travas.soma_dentro_do_teto(q, teto)
    resumo = (f"\nATIVAR CAMPANHA — a partir daqui ela GASTA\n"
              f"  conta:            {cid} — {nome_conta}\n"
              f"  campanha:         {r.campaign.name} (id {r.campaign.id})\n"
              f"  status:           {r.campaign.status.name} → ENABLED\n"
              f"  orçamento diário: {travas.brl(atual)}"
              + ("  (compartilhado com outras campanhas)"
                 if r.campaign_budget.explicitly_shared else "")
              + "\n" + travas.texto_quadro(q, teto))
    travas.confirmar_por_nome(r.campaign.name, resumo)

    from google.api_core import protobuf_helpers
    op = client.get_type("CampaignOperation")
    c = op.update
    c.resource_name = r.campaign.resource_name or client.get_service(
        "CampaignService").campaign_path(cid, r.campaign.id)
    c.status = client.enums.CampaignStatusEnum.ENABLED
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, type(c).pb(c)))
    client.get_service("CampaignService").mutate_campaigns(customer_id=cid, operations=[op])
    print(f"ATIVADA: {r.campaign.name}.")


def orcamento(campanha_id, novo_brl):
    cid = travas.customer_id()
    teto = travas.teto_brl()
    travas.dentro_do_teto(novo_brl, teto, "novo orçamento diário")
    client = auth.cliente()
    moeda, nome_conta = _moeda(client, cid)
    travas.exigir_brl(moeda)
    r = _campanha(client, cid, campanha_id)
    atual = travas.de_micros(r.campaign_budget.amount_micros)
    q = _quadro(client, cid, r.campaign_budget.resource_name, novo_brl, troca=True)
    travas.soma_dentro_do_teto(q, teto)
    resumo = (f"\nMUDAR ORÇAMENTO DIÁRIO\n"
              f"  conta:          {cid} — {nome_conta}\n"
              f"  campanha:       {r.campaign.name} (id {r.campaign.id}, "
              f"{r.campaign.status.name})\n"
              f"  atual:          {travas.brl(atual)}\n"
              f"  novo:           {travas.brl(novo_brl)}"
              + ("\n  ATENÇÃO: orçamento compartilhado — muda para todas as campanhas que o usam."
                 if r.campaign_budget.explicitly_shared else "")
              + "\n" + travas.texto_quadro(q, teto))
    travas.confirmar_por_nome(r.campaign.name, resumo)

    from google.api_core import protobuf_helpers
    op = client.get_type("CampaignBudgetOperation")
    b = op.update
    b.resource_name = r.campaign_budget.resource_name
    b.amount_micros = travas.micros(novo_brl)
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, type(b).pb(b)))
    client.get_service("CampaignBudgetService").mutate_campaign_budgets(
        customer_id=cid, operations=[op])
    print(f"ORÇAMENTO ALTERADO: {travas.brl(atual)} → {travas.brl(novo_brl)} por dia.")


# ---------------------------------------------------------------- pausar (reduz gasto)

def pausar(campanha_id, nome, aplicar):
    cid = travas.customer_id()
    client = auth.cliente()
    _, nome_conta = _moeda(client, cid)
    r = _campanha(client, cid, campanha_id) if campanha_id else _campanha_por_nome(client, cid, nome)
    if r.campaign.status.name == "PAUSED":
        sys.exit(f"A campanha '{r.campaign.name}' já está pausada. Nada foi alterado.")
    if r.campaign.status.name == "REMOVED":
        sys.exit(f"A campanha '{r.campaign.name}' foi removida. Nada foi alterado.")

    from google.api_core import protobuf_helpers
    op = client.get_type("CampaignOperation")
    c = op.update
    c.resource_name = r.campaign.resource_name or client.get_service(
        "CampaignService").campaign_path(cid, r.campaign.id)
    c.status = client.enums.CampaignStatusEnum.PAUSED
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, type(c).pb(c)))
    req = client.get_type("MutateCampaignsRequest")
    req.customer_id = cid
    req.operations.append(op)
    req.validate_only = not aplicar

    resumo = (f"\nPAUSAR CAMPANHA — ela para de gastar\n"
              f"  conta:            {cid} — {nome_conta}\n"
              f"  campanha:         {r.campaign.name} (id {r.campaign.id})\n"
              f"  status:           {r.campaign.status.name} → PAUSED\n"
              f"  orçamento diário: "
              f"{travas.brl(travas.de_micros(r.campaign_budget.amount_micros))}")
    if not aplicar:
        print(resumo)
        client.get_service("CampaignService").mutate_campaigns(request=req)
        print("\nSIMULAÇÃO OK: a API validou; nada foi alterado. Para pausar, rode de novo com "
              "--aplicar.")
        return
    travas.confirmar_simples(resumo)
    client.get_service("CampaignService").mutate_campaigns(request=req)
    print(f"PAUSADA: {r.campaign.name}.")
