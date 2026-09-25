#!/usr/bin/env python3
"""
Recalcula o motor de break-even com os parâmetros REAIS do consultor, sem que eles passem pela
conversa.

Uso:
    python3 scripts/calcular.py                  # linha `imovel`, grava em saida/
    python3 scripts/calcular.py --linha auto     # outra linha de produto.linhas
    python3 scripts/calcular.py --print          # também imprime no terminal (você decide olhar)

Lê:    config/consultor.json → produto.linhas.<linha>.taxa_administracao e .fundo_reserva
       (via scripts/config.py; fora do Git)
Grava: saida/motor-break-even-<linha>.md    (fora do Git)

O agente NÃO lê nem a entrada nem a saída. Você decide o que copiar para os docs versionados.
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import RAIZ, carregar, valor  # noqa: E402

SAIDA = os.path.join(RAIZ, "saida")

def pmt(C, i, n):
    if i == 0: return C / n
    f = (1 + i) ** n
    return C * i * f / (f - 1)

def bisect(f, a, b):
    fa = f(a)
    for _ in range(200):
        m = (a + b) / 2
        if fa * f(m) <= 0: b = m
        else: a, fa = m, f(m)
    return (a + b) / 2

def parametros_da_linha(cfg, linha):
    """Parâmetros da linha. Linha sem chave aborta: zero silencioso foi como o fundo de uma linha
    já entrou na conta de outra."""
    linhas = valor(cfg, "produto.linhas", {})
    if linha not in linhas:
        sys.exit(f"ERRO: linha `{linha}` não existe em `produto.linhas` da config. "
                 f"Linhas disponíveis: {', '.join(sorted(linhas)) or 'nenhuma'}.")
    return linhas[linha] or {}

def fundo_reserva(cfg, linha):
    """Fundo de reserva da linha. É por linha, nunca escalar — nem toda linha tem fundo.
    Campo vazio aborta: declare 0 quando a linha não tiver fundo, antes de calcular."""
    fr = parametros_da_linha(cfg, linha).get("fundo_reserva")
    if fr is None:
        sys.exit(f"ERRO: linha `{linha}` sem `fundo_reserva` declarado em "
                 f"config/consultor.json → produto.linhas.{linha}. "
                 f"Declare (0 quando não houver) antes de calcular.")
    return fr


def taxa_adm(cfg, linha):
    """Taxa de administração da linha. Mesma trava: linha sem parâmetro não calcula."""
    ta = parametros_da_linha(cfg, linha).get("taxa_administracao")
    if ta is None:
        sys.exit(f"ERRO: linha `{linha}` sem `taxa_administracao` declarada em "
                 f"config/consultor.json → produto.linhas.{linha}. "
                 f"Rode a skill `configuracao` (ou preencha o campo) antes de calcular.")
    return ta


def motor_break_even(cfg, linha="imovel"):
    ta = taxa_adm(cfg, linha); fr = fundo_reserva(cfg, linha)
    out = ["# Motor de break-even — valores REAIS\n",
           f"Parâmetros: taxa adm {ta*100:.2f}% · fundo reserva {fr*100:.2f}% · linha `{linha}`\n",
           "## Break-even de TAXA (% a.m. em que financiamento empata com consórcio)\n",
           "| Prazo | Taxa de equilíbrio |", "|---|---|"]
    for n in (60, 84, 120, 180, 200):
        alvo = (1 + ta + fr) / n
        i = bisect(lambda x: pmt(1, x, n) - alvo, 1e-9, 0.06)
        out.append(f"| {n} meses | {i*100:.2f}% a.m. |")
    return "\n".join(out) + "\n"

def main():
    ap = argparse.ArgumentParser(description="Motor de break-even de taxa, por linha de produto.")
    ap.add_argument("--linha", default="imovel", help="chave de produto.linhas (padrão: imovel)")
    ap.add_argument("--print", action="store_true", help="também imprime no terminal")
    a = ap.parse_args()

    cfg = carregar()
    saidas = {f"motor-break-even-{a.linha}.md": motor_break_even(cfg, a.linha)}
    os.makedirs(SAIDA, exist_ok=True)
    for nome, conteudo in saidas.items():
        caminho = os.path.join(SAIDA, nome)
        open(caminho, "w", encoding="utf-8").write(conteudo)
        print(f"gravado: saida/{nome}")
    if a.print:
        for c in saidas.values(): print("\n" + "="*60 + "\n" + c)
    else:
        print("\nUse --print para ver no terminal. Os arquivos ficam fora do Git:")
        print("você decide o que (e se) copia para os documentos versionados.")

if __name__ == "__main__":
    main()
