#!/usr/bin/env python3
"""
gads.py — integração própria do consultor com o Google Ads (biblioteca oficial `google-ads`).

    python3 scripts/google-ads/gads.py <subcomando> --help

Leitura ............ contas, relatorio
Escrita sem gasto .. criar-campanha (nasce PAUSADA; --simular é o padrão), criar-conversao
Reduz gasto ........ pausar (--simular é o padrão; --aplicar pede s/N só em terminal
                     interativo — fora dele, pausa direto)
Escrita com gasto .. ativar, orcamento (soma das ativas ≤ teto da config + nome da campanha
                     digitado no terminal)
Credenciais ........ autenticar (grava em ~/.config/consultor-adem/google-ads.yaml, fora do Git)

IDs vêm de config/consultor.json → anuncios.google (customer_id) e anuncios.teto_diario_brl.
Guia completo: .agents/skills/anuncios-google/SKILL.md.
"""
import argparse
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(1, os.path.dirname(AQUI))  # scripts/ → config.py

import auth  # noqa: E402
import operacoes  # noqa: E402


def _data(s):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        raise argparse.ArgumentTypeError("use AAAA-MM-DD")
    return s


def _brl(s):
    try:
        return float(s.replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError("valor em reais, ex.: 30 ou 30,50")


def _parser():
    p = argparse.ArgumentParser(prog="gads.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", metavar="subcomando")
    sub.required = True

    s = sub.add_parser("autenticar", help="OAuth Desktop app → refresh token no ~/.config",
                       description=auth.__doc__,
                       formatter_class=argparse.RawDescriptionHelpFormatter)
    s.add_argument("--client-secret", required=True,
                   help="JSON do cliente OAuth 'Desktop app' baixado do Google Cloud "
                        "(guarde fora do repositório)")
    s.add_argument("--developer-token", help="opcional — desativado pelo Google em 09/09/2026; "
                                             "use só se a API pedir")
    s.add_argument("--login-customer-id", help="opcional — só para quem opera via MCC")

    sub.add_parser("contas", help="lista as contas acessíveis com as credenciais")

    s = sub.add_parser("relatorio", help="desempenho por campanha no período")
    s.add_argument("--periodo", choices=list(operacoes.PERIODOS), default=None,
                   help="padrão: 7d")
    s.add_argument("--de", type=_data, help="início AAAA-MM-DD (com --ate)")
    s.add_argument("--ate", type=_data, help="fim AAAA-MM-DD (com --de)")

    s = sub.add_parser("criar-campanha",
                       help="campanha de Pesquisa PAUSADA a partir de um JSON em dados/")
    s.add_argument("arquivo", help="ex.: dados/campanha-imovel.json (formato no README)")
    m = s.add_mutually_exclusive_group()
    m.add_argument("--simular", action="store_true",
                   help="padrão: a API só valida (validate_only), nada é criado")
    m.add_argument("--aplicar", action="store_true", help="cria de fato (continua PAUSADA)")

    s = sub.add_parser("criar-conversao", help="ação de conversão medida pela tag no site")
    s.add_argument("--nome", required=True)
    s.add_argument("--tipo", required=True, choices=list(operacoes.CONVERSOES),
                   help="formulario=envio de formulário · whatsapp=clique no WhatsApp · "
                        "site=visita a página (ex.: obrigado)")
    m = s.add_mutually_exclusive_group()
    m.add_argument("--simular", action="store_true", help="padrão: só valida")
    m.add_argument("--aplicar", action="store_true", help="cria de fato")
    s.add_argument("--gravar-principal", action="store_true",
                   help="só se o consultor pedir: grava o id em "
                        "anuncios.google.conversao_principal")

    s = sub.add_parser("ativar", help="PAUSADA → ATIVA (gasta; soma das ativas ≤ teto). "
                                      "Exige nome digitado no terminal")
    s.add_argument("--campanha-id", required=True)

    s = sub.add_parser("pausar", help="ATIVA → PAUSADA (reduz gasto). --aplicar pede s/N "
                                       "só em terminal interativo")
    q = s.add_mutually_exclusive_group(required=True)
    q.add_argument("--campanha-id", help="id numérico da campanha")
    q.add_argument("--nome", help="nome exato da campanha")
    m = s.add_mutually_exclusive_group()
    m.add_argument("--simular", action="store_true", help="padrão: a API só valida, nada muda")
    m.add_argument("--aplicar", action="store_true",
                   help="pausa de fato: em terminal interativo pede s/N; fora dele "
                        "(agente, pipe) pausa sem perguntar")

    s = sub.add_parser("orcamento", help="muda o orçamento diário (soma das ativas ≤ teto). "
                                         "Exige nome digitado")
    s.add_argument("--campanha-id", required=True)
    s.add_argument("--novo-brl", required=True, type=_brl, help="novo orçamento diário em R$")
    return p


def _executar(a):
    if a.cmd == "autenticar":
        auth.autenticar(a.client_secret, a.developer_token, a.login_customer_id)
    elif a.cmd == "contas":
        operacoes.contas()
    elif a.cmd == "relatorio":
        operacoes.relatorio(a.periodo, a.de, a.ate)
    elif a.cmd == "criar-campanha":
        operacoes.criar_campanha(a.arquivo, aplicar=a.aplicar)
    elif a.cmd == "criar-conversao":
        operacoes.criar_conversao(a.nome, a.tipo, a.aplicar, a.gravar_principal)
    elif a.cmd == "ativar":
        operacoes.ativar(a.campanha_id)
    elif a.cmd == "pausar":
        operacoes.pausar(a.campanha_id, a.nome, a.aplicar)
    elif a.cmd == "orcamento":
        operacoes.orcamento(a.campanha_id, a.novo_brl)


def main():
    a = _parser().parse_args()
    try:
        _executar(a)
    except KeyboardInterrupt:
        sys.exit("\nInterrompido. Nada além do que foi impresso acima foi alterado.")
    except Exception as e:  # erros da API viram mensagem limpa, sem traceback
        nome = type(e).__name__
        if nome == "GoogleAdsException":
            print(f"ERRO da API do Google Ads (request_id {e.request_id}):", file=sys.stderr)
            for err in e.failure.errors:
                print(f"  - {err.message}  [{err.error_code}]".rstrip(), file=sys.stderr)
            sys.exit(1)
        if nome == "RefreshError":
            sys.exit(f"ERRO de autenticação ({e}). O refresh token pode ter sido revogado ou "
                     "expirado: rode `gads.py autenticar` de novo.")
        raise


if __name__ == "__main__":
    main()
