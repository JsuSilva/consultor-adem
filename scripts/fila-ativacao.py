#!/usr/bin/env python3
"""
Monta a fila de ativação ativa por WhatsApp a partir de uma lista de alvos do consultor.

    python3 scripts/fila-ativacao.py --lista dados/lista-estetica.csv \\
        --segmento estetica [--saida DIR] [--limite N] [--saudacao auto|"bom dia"|"boa tarde"] \\
        [--pular telefones-trabalhados.txt] [--incluir-fixo]

A lista é um CSV simples em dados/ (fora do Git), UTF-8, com cabeçalho, uma linha por alvo e
na ordem em que devem ser abordados (1ª onda antes da 2ª). Colunas:

  nome      — nome exibido do alvo (empresa ou pessoa). Obrigatória.
  telefone  — com ou sem máscara, com ou sem 55. Obrigatória (linha sem telefone é podada).
  mensagem  — texto da primeira mensagem, com a saudação ("bom dia"/"boa tarde") dentro, que o
              script troca pela escolhida em --saudacao. Obrigatória.
  socio     — nome de quem vai receber a mensagem, quando o alvo é empresa. Opcional.
  cnpj      — opcional.
  endereco  — opcional; entra no sobrenome do contato salvo no WhatsApp.
  movel     — 1 para celular, 0 para fixo. Opcional: vazio, o script considera celular o
              número que, na forma canônica, tem 11 dígitos com o 9 depois do DDD.

Grava um JSON com a fila já podada, pronta para a rodada de ativação e para a carga no CRM
(scripts/crm-xlsx.py).

⚠️ DADO DE LEAD (LGPD — script processa, agente não lê; dado de lead fora do Git). A lista de
entrada tem nome, sócio, CNPJ, endereço e telefone de pessoa e empresa. Este script SÓ IMPRIME
CONTAGENS no terminal — nunca uma linha de lead, nunca um nome, nunca um telefone. Os nomes só
existem dentro do JSON de saída, que fica em dados/ (fora do controle de versão).
"""
import argparse, csv, json, os, re, sys, unicodedata, urllib.parse
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Marcadores de pessoa jurídica no nome do sócio. HEURÍSTICA, não certeza: o caso real que motivou
# isso foi um sócio "Hospital Isb Ltda", que geraria a saudação "Hospital, bom dia". A lista cobre
# os marcadores mais comuns de razão social — pode haver falso positivo (sócio "Instituto" que seja
# apelido de pessoa) e falso negativo (razão social sem nenhum destes marcadores).
MARCADORES_PJ = [
    "ltda", "me", "epp", "eireli", "s/a", "s.a", "mei", "cia",
    "associacao", "instituto", "hospital", "clinica", "comercio",
    "servicos", "empreendimentos",
]

def sem_acento(s):
    """Minúsculo e sem diacrítico, para comparação de texto (não para exibição)."""
    return "".join(c for c in unicodedata.normalize("NFD", (s or "").lower())
                   if unicodedata.category(c) != "Mn")


def so_digitos(s):
    return re.sub(r"\D", "", s or "")


# A forma canônica é a de `scripts/telefone.py` — regra única do repositório. Aqui ela é
# obrigatória dos dois lados da comparação: os CSV da operação guardam o celular com o nono
# dígito, e o telefone de lista antiga ou base pública costuma vir sem ele. Comparar sem normalizar faria o `--pular` deixar passar quem já foi abordado.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from telefone import canonico  # noqa: E402


def parece_pessoa_juridica(socio):
    """True quando o texto do sócio tem marcador típico de razão social. Ver MARCADORES_PJ:
    é heurística por palavra inteira (com fronteira), não prova."""
    t = sem_acento(socio)
    for m in MARCADORES_PJ:
        if m in ("s/a", "s.a"):
            if m in t:
                return True
        elif re.search(rf"\b{re.escape(m)}\b", t):
            return True
    return False


def saudacao_efetiva(escolha):
    if escolha != "auto":
        return escolha
    return "bom dia" if datetime.now().hour < 12 else "boa tarde"


def troca_saudacao(msg, saudacao):
    """A mensagem da lista vem com uma saudação fixa (normalmente 'boa tarde'). Troca pela
    escolhida, preservando maiúscula/minúscula da primeira letra."""
    def repl(m):
        orig = m.group(0)
        novo = saudacao
        return novo[0].upper() + novo[1:] if orig[0].isupper() else novo
    return re.sub(r"\b(bom dia|boa tarde)\b", repl, msg, flags=re.IGNORECASE)


COLUNAS_OBRIGATORIAS = ("nome", "telefone", "mensagem")


def eh_movel(bruto, tel):
    """Coluna `movel` quando preenchida (1/0); vazia, deduz da forma canônica."""
    b = (bruto or "").strip().lower()
    if b in ("1", "sim", "s", "true"):
        return True
    if b in ("0", "nao", "não", "n", "false"):
        return False
    return len(tel) == 11 and tel[2] == "9"


def le_cards(caminho_csv):
    """Lê o CSV da lista e devolve um card por linha, na ordem em que aparecem no arquivo
    (1ª onda antes da 2ª, como o consultor ordenou a lista)."""
    with open(caminho_csv, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        faltam = [c for c in COLUNAS_OBRIGATORIAS if c not in (leitor.fieldnames or [])]
        if faltam:
            sys.exit(f"ERRO: a lista não tem a(s) coluna(s) obrigatória(s): {', '.join(faltam)}. "
                     f"Ver as colunas no topo de scripts/fila-ativacao.py.")
        cards = []
        for linha in leitor:
            pega = lambda c: (linha.get(c) or "").strip()
            telefone = pega("telefone")
            cards.append({
                "nome": pega("nome"), "socio": pega("socio"), "cnpj": pega("cnpj"),
                "endereco": pega("endereco"), "telefone": telefone,
                "mensagem": pega("mensagem"),
                "movel": eh_movel(linha.get("movel"), canonico(telefone)),
            })
    return cards


def le_pulados(caminho):
    """Telefones já trabalhados, um por linha, em qualquer formatação. Normaliza para dígitos
    e tira um eventual DDI 55 quando sobra dígito de mais (12-13 dígitos)."""
    pulados = set()
    for linha in open(caminho, encoding="utf-8"):
        d = canonico(linha)
        if not d:
            continue
        pulados.add(d)
    return pulados


def monta_fila(cards, incluir_fixo, pulados, segmento, saudacao):
    """Aplica a poda na ordem do enunciado e devolve (fila, contagens). Cada card cai no
    primeiro motivo que casar — a soma dos motivos mais a fila fecha com o total lido."""
    contagens = {"sem_telefone": 0, "fixo": 0, "repetido": 0, "pulado": 0, "razao_social": 0}
    vistos, fila = set(), []
    for c in cards:
        tel = canonico(c["telefone"])
        if not tel:
            contagens["sem_telefone"] += 1
            continue
        if not incluir_fixo and not c["movel"]:
            contagens["fixo"] += 1
            continue
        if tel in vistos:
            contagens["repetido"] += 1
            continue
        if tel in pulados:
            contagens["pulado"] += 1
            continue
        if c["socio"] and parece_pessoa_juridica(c["socio"]):
            contagens["razao_social"] += 1
            continue

        vistos.add(tel)
        msg = troca_saudacao(c["mensagem"], saudacao)
        # proxy da razão social: a lista só traz o nome exibido (coluna `nome`), que pode ser o
        # nome fantasia — não há razão social separada nesta fonte.
        sobrenome_wa = f"{c['nome']} - {c['endereco']}".strip(" -")
        fila.append({
            "nome": c["nome"],
            "socio": c["socio"],
            "cnpj": c["cnpj"],
            "endereco": c["endereco"],
            "telefone": tel,
            "mensagem": msg,
            "url": f"https://web.whatsapp.com/send?phone=55{tel}&text={urllib.parse.quote(msg)}",
            "sobrenome_whatsapp": sobrenome_wa,
            "obs": f"Prospecção ativa — lista {segmento}",
        })
    return fila, contagens


def main():
    ap = argparse.ArgumentParser(description="Monta a fila de ativação por WhatsApp a partir de "
                                              "uma lista CSV de alvos, já podada.")
    ap.add_argument("--lista", required=True, help="caminho do CSV de origem (em dados/)")
    ap.add_argument("--saida", default=os.path.join(RAIZ, "dados/"),
                    help="diretório de saída (padrão: dados/)")
    ap.add_argument("--segmento", required=True, help="rótulo curto p/ o nome do arquivo, ex.: estetica")
    ap.add_argument("--limite", type=int, default=None, help="máximo de itens na fila (padrão: todos)")
    ap.add_argument("--saudacao", choices=["auto", "bom dia", "boa tarde"], default="auto")
    ap.add_argument("--pular", default=None, help="arquivo com telefones já trabalhados, um por linha")
    ap.add_argument("--incluir-fixo", action="store_true",
                    help="não poda os telefones fixos (movel=0)")
    a = ap.parse_args()

    if not os.path.exists(a.lista):
        sys.exit(f"ERRO: lista não encontrada: {a.lista}")

    saudacao = saudacao_efetiva(a.saudacao)
    pulados = le_pulados(a.pular) if a.pular else set()

    cards = le_cards(a.lista)
    fila, contagens = monta_fila(cards, a.incluir_fixo, pulados, a.segmento, saudacao)
    truncada = a.limite is not None and len(fila) > a.limite
    if truncada:
        fila = fila[:a.limite]

    os.makedirs(a.saida, exist_ok=True)
    data_iso = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"fila-{a.segmento}-{data_iso}.json"
    caminho_saida = os.path.join(a.saida, nome_arquivo)

    saida = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "lista_origem": os.path.relpath(a.lista, RAIZ),
        "segmento": a.segmento,
        "saudacao": saudacao,
        "limite": a.limite,
        "poda": contagens,
        "lidos": len(cards),
        "na_fila": len(fila),
        "itens": fila,
    }
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    # Regra de confidencialidade: só contagem no terminal. Nenhuma linha de lead, nunca.
    print(f"lidos: {len(cards)}")
    print(f"podados — sem telefone: {contagens['sem_telefone']} · fixo: {contagens['fixo']} · "
          f"repetido: {contagens['repetido']} · pulado: {contagens['pulado']} · "
          f"razão social no sócio: {contagens['razao_social']}")
    print(f"na fila: {len(fila)}" + (" (truncada pelo --limite)" if truncada else ""))
    print(f"saudação aplicada: {saudacao}")
    print(f"→ {os.path.relpath(caminho_saida, RAIZ)}")


if __name__ == "__main__":
    main()
