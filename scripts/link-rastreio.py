#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o código de rastreio por pessoa, para o link que o consultor manda numa conversa em
andamento.

    python3 scripts/link-rastreio.py 41999998888
    python3 scripts/link-rastreio.py --cadencia          # um código por lead do CSV
    python3 scripts/link-rastreio.py --codigo a7f3       # de quem é este código?

Por que existe: analytics conta visita, não pessoa. Quando o consultor já está falando com
alguém no WhatsApp e manda uma página como retomada, o que interessa é saber se **aquela**
pessoa abriu. O código vai no link (`<site>/l/<código>`); o site grava a abertura e
redireciona. ⚠️ Essa rota `/l/<código>` e a lista de aberturas moram no site do consultor e
não fazem parte deste repositório — por isso o script entrega o código, não o link pronto.

**O código é derivado do telefone, e não volta a ser telefone.** É um hash curto com um
segredo local: mesmo telefone dá sempre o mesmo código, e quem vir o código não descobre o
número. O de/para vive aqui, na cópia local do consultor (dados/, fora do Git), nunca no
banco do site.

O segredo mora em `dados/.link-segredo` (fora do Git, criado na primeira execução). Trocar o
arquivo invalida os códigos já enviados.
"""
import argparse
import csv
import hashlib
import os
import re
import secrets
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")
SEGREDO = os.path.join(DADOS, ".link-segredo")
CADENCIA = os.path.join(DADOS, "cadencia.csv")
TAMANHO = 4  # 4 caracteres base32 ≈ 1 milhão de combinações: curto de digitar e difícil de adivinhar


def segredo():
    """Cria na primeira execução e reaproveita depois. Sem ele, qualquer um que
    conheça a fórmula reproduziria o código de qualquer telefone."""
    if not os.path.exists(SEGREDO):
        os.makedirs(DADOS, exist_ok=True)
        with open(SEGREDO, "w", encoding="utf-8") as f:
            f.write(secrets.token_hex(32))
        os.chmod(SEGREDO, 0o600)
        print(f"segredo novo criado em {os.path.relpath(SEGREDO, RAIZ)} — não versione, não apague",
              file=sys.stderr)
    return open(SEGREDO, encoding="utf-8").read().strip()


def so_digitos(telefone):
    d = re.sub(r"\D", "", telefone or "")
    if len(d) < 10:
        raise ValueError(f"telefone curto demais: {telefone!r}")
    return d[-11:] if len(d) > 11 else d


def codigo_de(telefone):
    bruto = hashlib.blake2s(so_digitos(telefone).encode(), key=segredo().encode()[:32]).hexdigest()
    # base36 sem ambiguidade visual: sem 0/o e 1/l, que erram ao ditar por voz
    alfabeto = "23456789abcdefghjkmnpqrstuvwxyz"
    n = int(bruto[:16], 16)
    saida = ""
    for _ in range(TAMANHO):
        n, r = divmod(n, len(alfabeto))
        saida += alfabeto[r]
    return saida


def linhas_da_cadencia():
    if not os.path.exists(CADENCIA):
        sys.exit(f"não achei {os.path.relpath(CADENCIA, RAIZ)} — rode com um telefone direto")
    with open(CADENCIA, encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            tel = next((linha[c] for c in linha if c.lower() in ("telefone", "celular", "whatsapp") and linha[c]), "")
            if tel:
                yield linha, tel


def main():
    p = argparse.ArgumentParser(description="Código de rastreio por pessoa")
    p.add_argument("telefone", nargs="?", help="telefone do lead, com ou sem máscara")
    p.add_argument("--cadencia", action="store_true", help="gera um código por lead do CSV de cadência")
    p.add_argument("--codigo", help="descobre de quem é um código recebido")
    args = p.parse_args()

    if args.codigo:
        alvo = args.codigo.strip().lower()
        achou = False
        for linha, tel in linhas_da_cadencia():
            if codigo_de(tel) == alvo:
                nome = next((linha[c] for c in linha if c.lower() in ("nome", "lead", "contato")), "")
                print(f"{alvo} → {nome or '(sem nome)'} · {tel}")
                achou = True
        if not achou:
            print(f"{alvo} → nenhum lead do CSV bate com esse código")
        return

    if args.cadencia:
        for linha, tel in linhas_da_cadencia():
            nome = next((linha[c] for c in linha if c.lower() in ("nome", "lead", "contato")), "")
            print(f"{nome or tel}\t{codigo_de(tel)}")
        return

    if not args.telefone:
        p.error("informe um telefone, ou use --cadencia / --codigo")
    print(codigo_de(args.telefone))


if __name__ == "__main__":
    main()
