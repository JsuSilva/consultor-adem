"""
Travas de gasto — o que separa o agente de um anúncio no ar.

1. Teto: `anuncios.teto_diario_brl` em config/consultor.json. Sem teto, nada que envolva
   orçamento roda. Orçamento acima do teto é recusado, sem exceção nem flag para pular.
2. Moeda: o teto é em reais; conta em outra moeda é recusada.
3. Teto somado: ativar e mudar orçamento somam o orçamento diário de TODAS as campanhas ativas
   (ENABLED) da conta — orçamento compartilhado conta uma vez só — com o orçamento pedido, e
   recusam se a soma passar do teto.
4. Confirmação por rodada: ativar e mudar orçamento exigem terminal interativo e o NOME EXATO da
   campanha digitado pelo consultor. Entrada vinda de pipe (echo ... |) é recusada. Pausar reduz
   gasto: pede só um s/N, também em terminal interativo.
"""
import sys

from config import carregar, valor  # scripts/config.py (caminho ajustado por gads.py)
from auth import so_digitos


def customer_id():
    cid = valor(carregar(), "anuncios.google.customer_id")
    if cid is None:
        sys.exit("ERRO: `anuncios.google.customer_id` não preenchido em config/consultor.json.\n"
                 "É o número da conta do Google Ads (canto superior direito, 123-456-7890). "
                 "Rode a skill `configuracao` ou preencha o campo.")
    return so_digitos(cid, "anuncios.google.customer_id")


def teto_brl():
    teto = valor(carregar(), "anuncios.teto_diario_brl")
    if teto is None:
        sys.exit("ERRO: `anuncios.teto_diario_brl` não preenchido em config/consultor.json.\n"
                 "Sem teto de verba configurado pelo consultor, nenhuma operação com orçamento "
                 "roda.")
    try:
        teto = float(teto)
    except (TypeError, ValueError):
        sys.exit(f"ERRO: `anuncios.teto_diario_brl` precisa ser número; veio {teto!r}.")
    if teto <= 0:
        sys.exit("ERRO: `anuncios.teto_diario_brl` precisa ser maior que zero.")
    return teto


def dentro_do_teto(valor_brl, teto, rotulo="orçamento diário"):
    if valor_brl <= 0:
        sys.exit(f"ERRO: {rotulo} precisa ser maior que zero.")
    if valor_brl > teto:
        sys.exit(f"RECUSADO: {rotulo} de {brl(valor_brl)} passa do teto de {brl(teto)} "
                 "(anuncios.teto_diario_brl). Mudar o teto é decisão do consultor, na config.")


def soma_dentro_do_teto(quadro, teto):
    """Recusa se a soma resultante das campanhas ativas passar do teto. `quadro` já formatado."""
    if quadro["resultante"] > teto:
        sys.exit("RECUSADO: a soma dos orçamentos diários das campanhas ativas passaria do teto "
                 "(anuncios.teto_diario_brl). Nada foi alterado.\n" + texto_quadro(quadro, teto)
                 + "\nMudar o teto é decisão do consultor, na config.")


def texto_quadro(quadro, teto):
    linhas = [f"  teto (config):            {brl(teto)} por dia",
              f"  soma atual das ativas:    {brl(quadro['atual'])} por dia "
              f"({quadro['n_ativas']} campanha(s) ativa(s))",
              f"  orçamento pedido:         {brl(quadro['pedido'])} por dia"]
    if quadro.get("descontado"):
        linhas.append(f"  sai da soma (é trocado):  {brl(quadro['descontado'])} por dia")
    linhas.append(f"  soma resultante:          {brl(quadro['resultante'])} por dia")
    if quadro.get("nota"):
        linhas.append(f"  ({quadro['nota']})")
    return "\n".join(linhas)


def exigir_brl(moeda):
    if moeda != "BRL":
        sys.exit(f"RECUSADO: a conta está em {moeda}, e o teto é em reais. Nada foi alterado.")


def confirmar_por_nome(nome_campanha, resumo):
    """Mostra o resumo e exige o nome exato da campanha digitado no terminal."""
    if not sys.stdin.isatty():
        sys.exit("RECUSADO: esta operação exige confirmação digitada pelo consultor num terminal "
                 "interativo. Rode o comando você mesmo, no seu terminal.")
    print(resumo)
    print(f"\nPara confirmar, digite o nome exato da campanha: {nome_campanha}")
    try:
        digitado = input("> ").strip()
    except EOFError:
        digitado = ""
    if digitado != nome_campanha:
        sys.exit("Nome não confere. Nada foi alterado.")


def confirmar_simples(resumo):
    """Mostra o resumo e pede s/N no terminal. Para operação que só reduz gasto (pausar).

    Fora de terminal interativo (agente, pipe, script), segue SEM pedir s/N: pausar só reduz
    gasto, e o agente precisa conseguir pausar numa emergência."""
    print(resumo)
    if not sys.stdin.isatty():
        print("\nFora de terminal interativo: pausando sem pedir s/N (pausar só reduz gasto).")
        return
    try:
        resp = input("\nConfirmar? [s/N] ").strip().lower()
    except EOFError:
        resp = ""
    if resp not in ("s", "sim"):
        sys.exit("Não confirmado. Nada foi alterado.")


def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def micros(v_brl):
    # Google Ads exige micros múltiplos de 10.000 (centavo).
    return int(round(v_brl * 100)) * 10_000


def de_micros(m):
    return (m or 0) / 1_000_000
