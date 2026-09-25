#!/usr/bin/env python3
"""
Monta e envia o placar diário do consultor — o lembrete do fim do dia no formato do grupo.

    python3 scripts/placar-dia.py              # monta e envia por e-mail (Brevo)
    python3 scripts/placar-dia.py --dry-run    # só imprime o texto, não envia
    python3 scripts/placar-dia.py --data 2026-09-03

De onde vem cada número:
  novos contatos    → dados/ativacoes.csv, linhas com a data do dia e status `enviado`/`ok`
                      — só a linha que criou card no CRM
  reunião agendada  → eventos do calendário cujo CREATED cai no dia
  reunião realizada → eventos do calendário cujo DTSTART cai no dia
  vendas            → sempre 00; o consultor edita à mão antes de postar no grupo

Lê de config/consultor.json (via scripts/config.py):
  consultor.nome                      → linha "Consultor:" e remetente do e-mail
  administradora.nome                 → remetente do e-mail (opcional)
  operacao.placar.grupo               → vai no assunto do e-mail (opcional)
  operacao.placar.minimo_contatos     → mínimo diário de novos contatos do grupo
  operacao.placar.minimo_agendadas    → mínimo diário de reuniões agendadas do grupo
  operacao.placar.formato             → opcional: texto do placar com os campos {consultor},
                                        {data}, {contatos}, {agendadas}, {realizadas},
                                        {minimo_contatos}, {minimo_agendadas}. Sem ele, sai o
                                        formato padrão abaixo (monta_texto).
  operacao.placar.horario             → não é lido aqui: é a hora em que o agendador roda isto.

Segredos em .env na raiz (fora do Git): CALENDARIO_ICS_URL, BREVO_API_KEY, BREVO_REMETENTE,
BREVO_DESTINATARIO.

O calendário e o CSV têm dado nominal — nome de lead, título de reunião. Este script NUNCA
imprime título de evento nem linha de lead: só contagens e o texto do placar, que é agregado.
"""
import argparse, base64, csv, datetime, json, os, pathlib, re, sys, urllib.request
from zoneinfo import ZoneInfo

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from config import carregar, exigir, valor  # noqa: E402

DADOS = RAIZ / "dados"
ATIVACOES = DADOS / "ativacoes.csv"
TZ = ZoneInfo("America/Sao_Paulo")

JANELA_RETRATO = 30  # dias à frente guardados para detectar cancelamento

# O print do CRM é produzido pela rodada de ativação (skill crm-apollo), com o filtro de
# período fechado no dia. Sem ele o placar sai marcado como FALHA: o e-mail vai com falha no
# placar para avisar o consultor de que a rodada ficou com algo pendente.
def print_do_dia(dia):
    return DADOS / f"placar-crm-{dia}.png"


def observacao_do_print(dia):
    """Nota livre gravada junto com o print, quando a tela pede explicação.

    Existe porque o print pode mostrar um número maior que o do placar — em dia de recuperação, a
    coluna traz também os registros de levas anteriores. Sem essa linha, quem lê o e-mail vê 30 no
    texto e outro número na imagem.
    """
    caminho = DADOS / f"placar-crm-{dia}.json"
    if not caminho.exists():
        return None
    try:
        return json.loads(caminho.read_text(encoding="utf-8")).get("observacao") or None
    except Exception:
        return None


def ligacoes_do_print(dia):
    """Ligações registradas no dia, contando só os leads criados naquele dia.

    Regra: bater significa que a contagem de ativos no dia é igual à de ligações registradas
    no dia no print — comparando só os leads criados no dia. Registro atrasado de leva anterior
    não entra na conta, senão todo dia de recuperação sairia como falha.

    O número é gravado pela rodada, junto com o print, em placar-crm-<dia>.json. O placar só
    compara — ele não abre o CRM.
    """
    caminho = DADOS / f"placar-crm-{dia}.json"
    if not caminho.exists():
        return None
    try:
        return int(json.loads(caminho.read_text(encoding="utf-8"))["ligacoes_no_dia"])
    except Exception:
        return None


def carrega_env():
    env = {}
    caminho = RAIZ / ".env"
    if not caminho.exists():
        sys.exit("ERRO: .env não existe na raiz do repo.")
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if "=" in linha and not linha.strip().startswith("#"):
            k, v = linha.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


# ── calendário ──────────────────────────────────────────────────────────────
def baixa_ics(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def desdobra(raw):
    """iCal quebra linha longa com CRLF + espaço. Junta antes de qualquer parse."""
    return raw.replace("\r\n ", "").replace("\r\n\t", "").replace("\r\n", "\n")


def _data(bloco, campo):
    """Devolve a data local do campo, aceitando as três formas do Google:
    ...Z (UTC), ;TZID=Zona:local, e ;VALUE=DATE (dia inteiro)."""
    m = re.search(rf"^{campo}(;[^:]*)?:(\d{{8}})(T(\d{{6}})(Z?))?", bloco, re.M)
    if not m:
        return None
    params, dia, _, hora, zulu = m.groups()
    if not hora:
        return datetime.datetime.strptime(dia, "%Y%m%d").date()
    dt = datetime.datetime.strptime(dia + hora, "%Y%m%d%H%M%S")
    if zulu == "Z":
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        tzid = re.search(r"TZID=([^;:]+)", params or "")
        try:
            dt = dt.replace(tzinfo=ZoneInfo(tzid.group(1)) if tzid else TZ)
        except Exception:
            dt = dt.replace(tzinfo=TZ)
    return dt.astimezone(TZ).date()


def eventos_do_feed(raw):
    out = []
    for bloco in desdobra(raw).split("BEGIN:VEVENT")[1:]:
        uid = re.search(r"^UID:(.+)$", bloco, re.M)
        status = re.search(r"^STATUS:(.+)$", bloco, re.M)
        out.append({
            "uid": uid.group(1).strip() if uid else "",
            "status": (status.group(1).strip().upper() if status else ""),
            "criado": _data(bloco, "CREATED"),
            "inicio": _data(bloco, "DTSTART"),
        })
    return out


def retrato(eventos, hoje):
    """UIDs dos eventos na janela à frente — serve para achar cancelamento no dia seguinte."""
    limite = hoje + datetime.timedelta(days=JANELA_RETRATO)
    return sorted(e["uid"] for e in eventos
                  if e["inicio"] and hoje <= e["inicio"] <= limite and e["status"] != "CANCELLED")


def cancelamentos(uids_hoje, hoje):
    """Compara com o retrato de ontem, quando existir. Devolve quantos sumiram."""
    ontem = DADOS / f"calendario-retrato-{hoje - datetime.timedelta(days=1)}.json"
    if not ontem.exists():
        return None
    try:
        antes = set(json.loads(ontem.read_text(encoding="utf-8")))
    except Exception:
        return None
    return len(antes - set(uids_hoje))


# ── ativações ───────────────────────────────────────────────────────────────
def contatos_do_dia(dia):
    """Novos contatos do dia — uma linha por card criado no CRM, não por mensagem enviada.

    O filtro de status é o que faz as duas réguas baterem: segunda mensagem no mesmo dia e
    follow-up de lead antiga entram no CSV com `status = followup` e ficam de fora. Sem isso,
    todo dia com encaminhamento ou encerramento sairia como FALHA na comparação com o print
    (mais linhas no CSV do que cards no CRM). A regra de registro mora na skill
    `whatsapp-web`.
    """
    if not ATIVACOES.exists():
        return 0
    n = 0
    with ATIVACOES.open(encoding="utf-8") as fh:
        for linha in csv.DictReader(fh):
            if (linha.get("data_hora") or "")[:10] != dia.isoformat():
                continue
            if (linha.get("status") or "enviado").strip().lower() in ("enviado", "ok"):
                n += 1
    return n


# ── texto ───────────────────────────────────────────────────────────────────
def monta_texto(cfg, dia, contatos, agendadas, realizadas):
    data_br = dia.strftime("%d/%m/%Y")
    CONSULTOR = exigir(cfg, "consultor.nome")
    MINIMO_CONTATOS = exigir(cfg, "operacao.placar.minimo_contatos")
    MINIMO_AGENDADAS = exigir(cfg, "operacao.placar.minimo_agendadas")

    formato = valor(cfg, "operacao.placar.formato")
    if formato:
        return formato.format(consultor=CONSULTOR, data=data_br, contatos=contatos,
                              agendadas=agendadas, realizadas=realizadas,
                              minimo_contatos=MINIMO_CONTATOS, minimo_agendadas=MINIMO_AGENDADAS)

    if contatos >= MINIMO_CONTATOS:
        bloco_crm = f"( x )  Entregou - fiz {contatos}\n(    ) Não entregou"
    else:
        bloco_crm = f"(    ) Entregou\n( x ) Não entregou - fiz {contatos}"

    if agendadas >= MINIMO_AGENDADAS:
        bloco_ag = f"( x ) Entregou - agendei {agendadas}\n(  ) Não entregou"
    else:
        bloco_ag = f"(  ) Entregou \n( x )Não entregou - agendei {agendadas}"

    return (
        f"Consultor: {CONSULTOR} - {data_br}\n\n"
        f"CRM: mínimo {MINIMO_CONTATOS}/dia novos contatos \n\n"
        f"{bloco_crm}\n\n"
        f"Reunião agendada: mínimo {MINIMO_AGENDADAS}/dia\n\n"
        f"{bloco_ag}\n\n"
        f"Reunião Realizada\n\n"
        f"Realizou: {realizadas}\n\n"
        f"Vendas \n\n"
        f"Realizou: 00\n"
    )


# ── envio ───────────────────────────────────────────────────────────────────
def envia_brevo(cfg, env, assunto, texto, anexo=None):
    """anexo: pathlib.Path de um PNG, ou None. A API do Brevo quer base64 em `attachment`."""
    chave = env.get("BREVO_API_KEY", "")
    if not chave or chave in ("...", "sua-chave"):
        return False, "BREVO_API_KEY não preenchida no .env"
    payload = {
        "sender": {"name": " · ".join(x for x in (valor(cfg, "administradora.nome"),
                                                  exigir(cfg, "consultor.nome")) if x),
                   "email": env["BREVO_REMETENTE"]},
        "to": [{"email": env["BREVO_DESTINATARIO"]}],
        "subject": assunto,
        "textContent": texto,
    }
    if anexo is not None:
        payload["attachment"] = [{
            "name": anexo.name,
            "content": base64.b64encode(anexo.read_bytes()).decode(),
        }]
    corpo = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email", data=corpo,
        headers={"api-key": chave, "content-type": "application/json", "accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status in (200, 201), f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} — {e.reason}"
    except Exception as e:
        return False, str(e)


def main():
    ap = argparse.ArgumentParser(description="Placar diário do consultor, por e-mail.")
    ap.add_argument("--data", default=None, help="AAAA-MM-DD (padrão: hoje)")
    ap.add_argument("--dry-run", action="store_true", help="imprime o texto e não envia")
    a = ap.parse_args()

    dia = (datetime.date.fromisoformat(a.data) if a.data
           else datetime.datetime.now(TZ).date())

    cfg = carregar()
    exigir(cfg, "consultor.nome")
    exigir(cfg, "operacao.placar.minimo_contatos")
    exigir(cfg, "operacao.placar.minimo_agendadas")
    grupo = valor(cfg, "operacao.placar.grupo")
    rotulo = f" · {grupo}" if grupo else ""

    env = carrega_env()
    eventos = eventos_do_feed(baixa_ics(env["CALENDARIO_ICS_URL"]))
    vivos = [e for e in eventos if e["status"] != "CANCELLED"]

    agendadas = sum(1 for e in vivos if e["criado"] == dia)
    realizadas = sum(1 for e in vivos if e["inicio"] == dia)
    contatos = contatos_do_dia(dia)

    uids = retrato(vivos, dia)
    sumidos = cancelamentos(uids, dia)
    DADOS.mkdir(parents=True, exist_ok=True)
    (DADOS / f"calendario-retrato-{dia}.json").write_text(json.dumps(uids), encoding="utf-8")

    texto = monta_texto(cfg, dia, contatos, agendadas, realizadas)
    if sumidos:
        texto += f"\n---\n{sumidos} reunião(ões) sumiu(ram) da agenda desde ontem — confira antes de postar.\n"

    print_crm = print_do_dia(dia)
    tem_print = print_crm.exists() and print_crm.stat().st_size > 0

    ligacoes_crm = ligacoes_do_print(dia) if tem_print else None

    if tem_print and ligacoes_crm == contatos:
        assunto = f"Placar do dia{rotulo} — {dia.strftime('%d/%m/%Y')}"
        nota = observacao_do_print(dia)
        if nota:
            texto += f"\n---\nSobre o print: {nota}\n"
    elif tem_print:
        assunto = f"FALHA no placar{rotulo} — {dia.strftime('%d/%m/%Y')}"
        if ligacoes_crm is None:
            texto += (
                "\n---\n"
                "FALHA: o print do CRM existe, mas veio sem a contagem de ligações do dia.\n"
                f"Esperado o arquivo placar-crm-{dia}.json com o campo ligacoes_no_dia.\n"
                "Sem esse número não dá para conferir se o print bate com o placar.\n"
            )
        else:
            texto += (
                "\n---\n"
                "FALHA: o print do CRM não bate com o placar.\n"
                f"Ativos do dia no CSV: {contatos}. Ligações dos leads criados no dia, no print: {ligacoes_crm}.\n"
                "Confira antes de postar: ou sobrou registro de outro dia, ou faltou registrar alguém.\n"
            )
    else:
        assunto = f"FALHA no placar{rotulo} — {dia.strftime('%d/%m/%Y')}"
        texto += (
            "\n---\n"
            "FALHA: o print do CRM do dia não foi gerado.\n"
            f"Esperado em {print_crm.name}, dentro de dados/.\n"
            "Isso quer dizer que a rodada não fechou — travou no CRM ou faltou interação no chat.\n"
            "Os números acima saíram do CSV e do calendário, então valem; o que ficou pendente é a\n"
            "conferência contra o CRM.\n"
        )

    print(f"[assunto] {assunto}")
    print(texto)
    if a.dry_run:
        print("--- dry-run: não enviado ---")
        return

    ok_email, detalhe = envia_brevo(cfg, env, assunto, texto, print_crm if tem_print else None)
    print("enviado:" if ok_email else "NÃO enviado:", detalhe, "| print:", "sim" if tem_print else "NAO")

    # O e-mail é o entregável primário: só ele manda no código de saída.
    sys.exit(0 if ok_email else 1)


if __name__ == "__main__":
    main()
