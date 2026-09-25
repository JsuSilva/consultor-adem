#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monta a planilha XLSX de importação de leads para o CRM Apollo (crmapollo.com.br), a partir da
fila gerada por scripts/fila-ativacao.py.

    python3 scripts/crm-xlsx.py --fila dados/fila-estetica-2026-09-04.json \\
        --tags "Estetica;Abordagem 1;Sem Resposta"

    python3 scripts/crm-xlsx.py --fila fila.json --tags "Contador;Abordagem 2;Sem Resposta" \\
        --somente-enviados --obs "Prospecção fria via WhatsApp"

Grava em dados/ (fora do Git). O JSON de entrada e o XLSX de saída são dado nominal — nome,
telefone, endereço de lead real (LGPD). Por isso o script NUNCA imprime nome, telefone ou
endereço, nem no terminal nem em log: só contagens e o caminho do arquivo.

Contrato da tela de importação do CRM (verificado em campo), nesta ordem exata:
  nome          — texto livre
  celular       — só números, 10 ou 11 dígitos, com DDD, sem o 55
  classificacao — etiquetas separadas por ";", máximo 90 caracteres no total
  obs           — texto livre, máximo 1000 caracteres

Sem openpyxl/pandas (dependência zero: roda em qualquer Python 3). O XLSX é montado
na mão com zipfile: [Content_Types].xml, _rels/.rels, xl/workbook.xml, xl/_rels/workbook.xml.rels
e xl/worksheets/sheet1.xml, com inline strings (sem tabela de strings compartilhadas). Esse caminho
já importou 20 de 20 linhas no CRM numa rodada real.
"""
import argparse
import datetime
import json
import os
import re
import sys
import unicodedata
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COLUNAS = ["nome", "celular", "classificacao", "obs"]
LETRAS = ["A", "B", "C", "D"]

LIMITE_CLASSIFICACAO = 90
LIMITE_OBS = 1000

MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho",
    7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}

# Caracteres inválidos em XML 1.0 (fora dos controles de espaço em branco permitidos).
_CONTROLE_RE = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f]")
_DATA_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b")


# ─────────────────────────────────────────────────────────────────────────────
# Saneamento — o CRM engole a barra "/" nos campos de texto
# ─────────────────────────────────────────────────────────────────────────────

def _por_extenso(m):
    dia, mes, ano = m.group(1), m.group(2), m.group(3)
    try:
        nome_mes = MESES[int(mes)]
    except (KeyError, ValueError):
        return m.group(0)
    if ano:
        return f"{dia} de {nome_mes} de {ano}"
    return f"{dia} de {nome_mes}"


def sanear_barra(texto):
    """Tenta reconhecer datas DD/MM ou DD/MM/AAAA e escrevê-las por extenso; qualquer barra que
    sobrar (ex.: hora escrita errado) é simplesmente removida. Retorna (texto_saneado, mudou?)."""
    if not texto:
        return texto, False
    original = texto
    texto = _DATA_RE.sub(_por_extenso, texto)
    if "/" in texto:
        # Barra que não era data (ex.: "e/ou", "24/7") vira espaço, não some: colar as palavras
        # produziria "eou" no CRM. Espaços repetidos são colapsados em seguida.
        texto = re.sub(r"\s{2,}", " ", texto.replace("/", " ")).strip()
    return texto, texto != original


def limpar_controle(texto):
    return _CONTROLE_RE.sub("", texto) if texto else texto


# ─────────────────────────────────────────────────────────────────────────────
# Leitura da fila
# ─────────────────────────────────────────────────────────────────────────────

def extrair_itens(dados):
    """Aceita lista no topo, ou objeto com a lista sob 'itens', 'fila' ou 'leads'."""
    if isinstance(dados, list):
        return dados
    if isinstance(dados, dict):
        for chave in ("itens", "fila", "leads"):
            valor = dados.get(chave)
            if isinstance(valor, list):
                return valor
    sys.exit(
        "ERRO: não encontrei uma lista de itens no JSON da fila "
        "(esperava uma lista no topo, ou um objeto com 'itens'/'fila'/'leads')."
    )


def foi_enviado(item):
    if item.get("enviado") is True:
        return True
    status = str(item.get("status", "")).strip().lower()
    return status in ("enviado", "ok")


def apenas_digitos(valor):
    return re.sub(r"\D", "", str(valor or ""))


def remover_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def derivar_rotulo(tags):
    primeira = tags.split(";")[0]
    s = remover_acentos(primeira).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "leads"


# ─────────────────────────────────────────────────────────────────────────────
# Montagem das linhas + relatório numérico
# ─────────────────────────────────────────────────────────────────────────────

def montar_linhas(itens, tags, obs_padrao):
    """Valida e transforma os itens da fila em linhas prontas para a planilha.
    Não imprime nem retorna nome/telefone/endereço em texto de erro — só contagens."""
    relatorio = {
        "lidos": len(itens),
        "rejeitados_celular_invalido": 0,
        "rejeitados_celular_duplicado": 0,
        "rejeitados_sem_nome": 0,
        "obs_truncados": 0,
        "campos_saneados": 0,
    }
    linhas = []
    celulares_vistos = set()

    for item in itens:
        celular = apenas_digitos(item.get("telefone"))
        if len(celular) not in (10, 11):
            relatorio["rejeitados_celular_invalido"] += 1
            continue
        if celular in celulares_vistos:
            relatorio["rejeitados_celular_duplicado"] += 1
            continue
        celulares_vistos.add(celular)

        nome = limpar_controle(str(item.get("nome", "")).strip())
        if not nome:
            # Lead sem nome importa como linha em branco no CRM e vira retrabalho manual.
            relatorio["rejeitados_sem_nome"] += 1
            celulares_vistos.discard(celular)
            continue
        obs = str(item.get("obs") or obs_padrao or "")

        nome, saneou_nome = sanear_barra(nome)
        obs, saneou_obs = sanear_barra(obs)
        if saneou_nome:
            relatorio["campos_saneados"] += 1
        if saneou_obs:
            relatorio["campos_saneados"] += 1

        obs = limpar_controle(obs)
        if len(obs) > LIMITE_OBS:
            obs = obs[:LIMITE_OBS]
            relatorio["obs_truncados"] += 1

        linhas.append({
            "nome": nome,
            "celular": celular,
            "classificacao": tags,
            "obs": obs,
        })

    relatorio["gravados"] = len(linhas)
    return linhas, relatorio


# ─────────────────────────────────────────────────────────────────────────────
# Geração do XLSX, sem biblioteca — zipfile puro com inline strings
# ─────────────────────────────────────────────────────────────────────────────

def esc_xml(valor):
    s = limpar_controle(str(valor))
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace('"', "&quot;").replace("'", "&apos;")
    return s


def gerar_xlsx(caminho, linhas):
    linhas_xml = []

    celulas_cabecalho = "".join(
        f'<c r="{LETRAS[i]}1" t="inlineStr"><is><t>{esc_xml(c)}</t></is></c>'
        for i, c in enumerate(COLUNAS)
    )
    linhas_xml.append(f'<row r="1">{celulas_cabecalho}</row>')

    for idx, linha in enumerate(linhas, start=2):
        celulas = "".join(
            f'<c r="{LETRAS[i]}{idx}" t="inlineStr"><is><t>{esc_xml(linha[c])}</t></is></c>'
            for i, c in enumerate(COLUNAS)
        )
        linhas_xml.append(f'<row r="{idx}">{celulas}</row>')

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(linhas_xml)}</sheetData></worksheet>'
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.'
        'relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-'
        'officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.'
        'openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '</Types>'
    )

    rels_raiz = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>'
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="leads" sheetId="1" r:id="rId1"/></sheets>'
        '</workbook>'
    )

    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '</Relationships>'
    )

    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with zipfile.ZipFile(caminho, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels_raiz)
        z.writestr("xl/workbook.xml", workbook_xml)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Gera o XLSX de importação de leads para o CRM Apollo, a partir da fila de "
                    "ativação. Não imprime dado nominal — só contagens."
    )
    ap.add_argument("--fila", required=True,
                     help="JSON produzido por scripts/fila-ativacao.py")
    ap.add_argument("--tags", required=True,
                     help='classificação, ex.: "Estetica;Abordagem 1;Sem Resposta"')
    ap.add_argument("--saida", default="dados/",
                     help="diretório de saída (padrão: dados/)")
    ap.add_argument("--nome-arquivo", default=None,
                     help="nome do XLSX (padrão: crm-import-<rotulo>-<AAAA-MM-DD>.xlsx)")
    ap.add_argument("--rotulo", default=None,
                     help="rótulo do arquivo (padrão: derivado da primeira etiqueta de --tags)")
    ap.add_argument("--obs", default="",
                     help="observação padrão para item sem 'obs' no JSON")
    ap.add_argument("--somente-enviados", action="store_true",
                     help="inclui só os itens marcados como efetivamente ativados "
                          "(enviado: true, ou status 'enviado'/'ok')")
    a = ap.parse_args()

    if len(a.tags) > LIMITE_CLASSIFICACAO:
        sys.exit(
            f"ERRO: --tags tem {len(a.tags)} caracteres, acima do limite de "
            f"{LIMITE_CLASSIFICACAO} da tela de importação do CRM. Ajuste as etiquetas."
        )

    if not os.path.exists(a.fila):
        sys.exit(f"ERRO: {a.fila} não existe.")
    with open(a.fila, encoding="utf-8") as f:
        dados = json.load(f)
    itens = extrair_itens(dados)

    total_lidos = len(itens)
    if a.somente_enviados:
        itens = [i for i in itens if foi_enviado(i)]

    linhas, relatorio = montar_linhas(itens, a.tags, a.obs)
    relatorio["lidos"] = total_lidos
    relatorio["apos_filtro_enviados"] = len(itens)

    if not linhas:
        sys.exit("ERRO: nenhuma linha válida para gravar depois da validação.")

    rotulo = a.rotulo or derivar_rotulo(a.tags)
    nome_arquivo = a.nome_arquivo or f"crm-import-{rotulo}-{datetime.date.today().isoformat()}.xlsx"

    destino_dir = a.saida if os.path.isabs(a.saida) else os.path.join(RAIZ, a.saida)
    caminho = os.path.join(destino_dir, nome_arquivo)

    gerar_xlsx(caminho, linhas)

    print("Fila lida:", relatorio["lidos"])
    if a.somente_enviados:
        print("Após filtro --somente-enviados:", relatorio["apos_filtro_enviados"])
    print("Rejeitados por celular inválido (fora de 10-11 dígitos):",
          relatorio["rejeitados_celular_invalido"])
    print("Rejeitados por celular duplicado:", relatorio["rejeitados_celular_duplicado"])
    print("Rejeitados por falta de nome:", relatorio["rejeitados_sem_nome"])
    print("Campos com barra saneada:", relatorio["campos_saneados"])
    print("Campos 'obs' truncados (>1000 caracteres):", relatorio["obs_truncados"])
    print("Linhas gravadas:", relatorio["gravados"])
    print("Arquivo:", caminho)


if __name__ == "__main__":
    main()
