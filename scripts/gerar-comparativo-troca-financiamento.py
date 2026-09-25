#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera saida/comparativo-troca-financiamento.html — o card comparativo "vale trocar o financiamento
pelo consórcio?", para exportar como imagem.

    python3 scripts/gerar-comparativo-troca-financiamento.py          # só o HTML
    python3 scripts/gerar-comparativo-troca-financiamento.py --png    # HTML e PNG ao lado

Modelo irmão do gerar-comparativo-construcao.py, e segue as mesmas duas regras:

1. **O design vem do design.py**, e o CSS do card é o do comparativo da construção — importado de
   lá, não copiado. Nenhuma cor escrita aqui.
2. **O conteúdo vem da conta**, para um caso PF de veículo: dois cenários de financiamento sobre
   R$ 79.000 liberados (24x a juros zero e 36x de R$ 3.000, IOF financiado), contra uma carta de
   veículo com lance embutido que quita o financiamento. Taxa de administração, fundo de reserva,
   prazo e índice da linha automóvel vêm de config/consultor.json (via scripts/config.py); as
   condições de grupo usadas na conta e o resultado da conta do `calculista` vêm do bloco CONTA
   abaixo. Campo vazio para o script com aviso. Mudou a conta, muda aqui — nesta ordem, nunca ao
   contrário.

Para reutilizar em outro caso: troque os blocos CASO e CONTA e os textos do corpo; a estrutura (três
destaques, gráfico do ganho por mês de contemplação, tabela lado a lado, bloco do consórcio, faixa
de sugestão, ficha de custos e rodapé de premissas) é o modelo.

Tema fixo em escuro: artefato feito para virar PNG, não para herdar o tema do leitor.
"""
import io, os, sys, html, subprocess, importlib.util

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
import design
from config import carregar, exigir

DESTINO = os.path.join(RAIZ, "saida", "comparativo-troca-financiamento.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

_spec = importlib.util.spec_from_file_location(
    "construcao", os.path.join(RAIZ, "scripts", "gerar-comparativo-construcao.py"))
_construcao = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_construcao)
CSS = _construcao.CSS

# ─────────────────────────────────────────────────────────────────────────────
# CASO — exemplo editável: o financiamento do cliente e as premissas de mercado.
# ─────────────────────────────────────────────────────────────────────────────
CARTA = 110_000.0          # crédito da carta, escolhido para cobrir o saldo do financiamento
SALDO_3A = "R$ 76.307"     # saldo do financiamento de 36x a partir da 3ª parcela
PARCELA_FIN = 3_000.0      # parcela do financiamento de 36x
RESTAM_FIN = 34            # parcelas do financiamento que ainda faltam
CDI_AA = ("13,90%", "Banco Central, 11/09/2026")        # desconto a valor presente, bruto, sem IR
INDICE_12M = ("3,98%", "Banco Central, 14/09/2026")     # variação do índice de reajuste da linha

# ─────────────────────────────────────────────────────────────────────────────
# CONTA — o que a conta do `calculista` usou e devolveu para este caso. Tudo depende das regras
# e dos parâmetros da sua administradora: preencha com a conta refeita, nunca com estimativa.
# ─────────────────────────────────────────────────────────────────────────────
REDUCAO = None       # redução da parcela até a contemplação, em fração do fundo comum (ex.: 0.5)
LANCE_PCT = None     # lance embutido do caso, em fração do total do plano, dentro do teto do grupo
MATURACAO = None     # meses — premissa declarada pelo consultor, sem medição estatística
# ganho da troca por mês de contemplação (1..N), cenário de 36x, com reajuste pelo índice da linha:
# VP = valor presente a CDI; NOM = desembolso nominal. Sobra de crédito abate as últimas parcelas
# do consórcio.
VP = None            # lista, um valor por mês de contemplação
NOM = None           # lista, mesmo tamanho de VP

_faltam = [n for n in ("REDUCAO", "LANCE_PCT", "MATURACAO", "VP", "NOM") if globals()[n] is None]
if _faltam:
    sys.exit("ERRO: bloco CONTA de scripts/gerar-comparativo-troca-financiamento.py sem "
             + ", ".join(_faltam) + ".\nPeça a conta ao `calculista` com as condições do grupo da "
             "sua administradora e preencha o bloco antes de gerar esta peça.")

# ─────────────────────────────────────────────────────────────────────────────
# CONSÓRCIO — linha automóvel, de config/consultor.json. Tudo DERIVADO aqui, nunca na prosa.
# ─────────────────────────────────────────────────────────────────────────────
_cfg = carregar()
TAXA_ADM = exigir(_cfg, "produto.linhas.auto.taxa_administracao")
FUNDO = exigir(_cfg, "produto.linhas.auto.fundo_reserva")
PRAZO = exigir(_cfg, "produto.linhas.auto.prazo_meses")
INDICE = exigir(_cfg, "produto.linhas.auto.indice_reajuste")
CONSULTOR = exigir(_cfg, "consultor.nome")
ASSINATURA = exigir(_cfg, "consultor.assinatura")

K = TAXA_ADM + FUNDO
TOTAL = CARTA * (1 + K)
PARCELA = TOTAL / PRAZO
# parcela reduzida: só a fração não reduzida do fundo comum, com taxa e fundo integrais
REDUZIDA = CARTA * (1 - REDUCAO) / PRAZO + CARTA * K / PRAZO
LANCE = LANCE_PCT * TOTAL
LIQUIDO = CARTA - LANCE
ESPERA = PARCELA_FIN + REDUZIDA
def _depois(m): return (TOTAL - REDUZIDA * m - LANCE) / (PRAZO - m)

# leituras do resultado — derivadas da série, nunca digitadas
N_MESES = len(VP)
ULTIMO_GANHO = max((m for m, v in enumerate(VP, 1) if v > 0), default=0)
ULTIMO_5MIL = max((m for m, v in enumerate(VP, 1) if v > 5000), default=0)
EQUILIBRIO = next((m + v / (v - VP[m]) for m, v in enumerate(VP, 1)
                   if m < N_MESES and v > 0 >= VP[m]), float(ULTIMO_GANHO))
# o desembolso nominal: negativo em todos os meses, em alguns, ou em nenhum
NOM_NEGATIVOS = sum(1 for v in NOM if v < 0)
# a sugestão sai da conta: o ganho a valor presente precisa alcançar a maturação declarada
TROCA_CABE = ULTIMO_GANHO >= MATURACAO

def esc(s): return html.escape(str(s), quote=True)


def brl(v):
    s = f"{abs(v):,.0f}".replace(",", ".")
    return ("−R$ " if v < 0 else "R$ ") + s


def brl2(v): return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(v, n=1): return f"{v*100:.{n}f}".replace(".", ",") + "%"


def grafico(larg=1000, alt=340):
    ml, mr, mt, mb = 80, 26, 26, 52
    W, H = larg - ml - mr, alt - mt - mb
    y0, y1 = -30000.0, 20000.0

    def X(m): return ml + W * ((m - 1) / (N_MESES - 1))
    def Y(v): return mt + H * (1 - (v - y0) / (y1 - y0))

    p = []
    for v in (-30000, -20000, -10000, 0, 10000, 20000):
        p.append(f'<line x1="{ml}" y1="{Y(v):.1f}" x2="{ml+W}" y2="{Y(v):.1f}" '
                 f'stroke="{"var(--ink-3)" if v == 0 else "var(--rule)"}" '
                 f'stroke-width="{1.5 if v == 0 else 1}"/>')
        p.append(f'<text x="{ml-10}" y="{Y(v)+4:.1f}" text-anchor="end" class="ax">{brl(v)}</text>')
    for m in (1, 6, 10, 18, 24, 30, 33):
        p.append(f'<text x="{X(m):.1f}" y="{mt+H+20}" text-anchor="middle" class="ax">{m}</text>')
    p.append(f'<text x="{ml+W/2:.1f}" y="{mt+H+42}" text-anchor="middle" class="ax">'
             f'MÊS DA CONTEMPLAÇÃO, CONTADO DA ADESÃO</text>')

    # faixa em que a troca ainda ganha
    p.append(f'<rect x="{X(1):.1f}" y="{mt}" width="{X(EQUILIBRIO)-X(1):.1f}" height="{H}" '
             f'fill="var(--accent-soft)" opacity=".55"/>')
    # maturação estimada do grupo
    p.append(f'<line x1="{X(MATURACAO):.1f}" y1="{mt}" x2="{X(MATURACAO):.1f}" y2="{mt+H}" '
             f'stroke="var(--ink-2)" stroke-width="1.5" stroke-dasharray="2 5"/>')
    p.append(f'<text x="{X(MATURACAO)+10:.1f}" y="{mt+H-12}" class="lb">'
             f'MATURAÇÃO ESTIMADA · {MATURACAO} MESES</text>')

    d = " ".join(("M" if i == 0 else "L") + f"{X(i+1):.1f} {Y(v):.1f}" for i, v in enumerate(NOM))
    p.append(f'<path d="{d}" fill="none" stroke="var(--ink-2)" stroke-width="2" stroke-dasharray="6 5"/>')
    d = " ".join(("M" if i == 0 else "L") + f"{X(i+1):.1f} {Y(v):.1f}" for i, v in enumerate(VP))
    p.append(f'<path d="{d}" fill="none" stroke="var(--accent)" stroke-width="3" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')

    p.append(f'<line x1="{X(EQUILIBRIO):.1f}" y1="{mt}" x2="{X(EQUILIBRIO):.1f}" y2="{mt+H}" '
             f'stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 4"/>')
    p.append(f'<circle cx="{X(EQUILIBRIO):.1f}" cy="{Y(0):.1f}" r="7" fill="none" '
             f'stroke="var(--accent)" stroke-width="2.5"/>')
    p.append(f'<text x="{X(1)+12:.1f}" y="{mt+H-12}" class="lb on">A TROCA AINDA GANHA</text>')
    p.append(f'<text x="{X(EQUILIBRIO)+12:.1f}" y="{mt+H-12}" class="lb">A PARTIR DO MÊS {ULTIMO_GANHO + 1}, PERDE</text>')
    p.append(f'<text x="{X(1)+12:.1f}" y="{Y(VP[0])-12:.1f}" class="lb on">'
             f'VALOR PRESENTE · {brl(VP[0])} NO MÊS 1</text>')
    if NOM_NEGATIVOS == N_MESES:
        rot_nom = "DESEMBOLSO · NEGATIVO EM QUALQUER MÊS"
    elif NOM_NEGATIVOS == 0:
        rot_nom = "DESEMBOLSO · POSITIVO EM QUALQUER MÊS"
    else:
        rot_nom = f"DESEMBOLSO · NEGATIVO EM {NOM_NEGATIVOS} DE {N_MESES} MESES"
    p.append(f'<text x="{X(12):.1f}" y="{Y(NOM[11])+26:.1f}" class="lb dim">{rot_nom}</text>')

    return (f'<svg class="g" viewBox="0 0 {larg} {alt}" width="{larg}" height="{alt}" role="img" '
            f'aria-label="Ganho da troca pelo consórcio por mês de contemplação">{"".join(p)}</svg>')


# rótulo, 24 meses, 36 meses, destaque
LINHAS = [
    ("Valor liberado",             "R$ 79.000",               "R$ 79.000",                ""),
    ("IOF financiado",             "R$ 2.172",                "R$ 2.449",                 ""),
    ("Parcela",                    "R$ 3.382,17",             "R$ 3.000,00",              ""),
    ("Juros do contrato",          "0,00% a.m.",              "1,61% a.m. · 21,16% a.a.", "c"),
    ("CET",                        "0,22% a.m. · 2,65% a.a.", "1,80% a.m. · 23,85% a.a.", "c"),
    ("Total pago",                 "R$ 81.172",               "R$ 108.000",               ""),
    ("Custo sobre os R$ 79 mil",   "R$ 2.172 · 2,75%",        "R$ 29.000 · 36,71%",       "c"),
    ("Saldo para quitar hoje · 2 parcelas pagas", "R$ 74.408",               "R$ 78.049",                ""),
    ("Juros que a quitação evita · nominal / valor presente", "R$ 0 / −R$ 8.570", "R$ 23.951 / R$ 6.796", "c"),
    ("Troca pelo consórcio",       "não vale",
     f"só com contemplação até o mês {ULTIMO_GANHO}" if ULTIMO_GANHO else "não vale", "f"),
]

CONS = [
    ("Carta",            f"{brl(CARTA)} · cobre o saldo a partir da 3ª parcela do carro ({SALDO_3A})"),
    ("Lance embutido",   f"{pct(LANCE_PCT, 0)} do total do plano ({brl(TOTAL)}) · {brl(LANCE)}, deduzidos do próprio crédito"),
    ("Crédito líquido",  f"{brl(LIQUIDO)} para quitar o financiamento"),
    ("Parcela integral", f"{brl2(PARCELA)} · {PRAZO} meses"),
    ("Parcela reduzida", f"{brl2(REDUZIDA)} até a contemplação"),
    ("Enquanto espera",  f"{brl(ESPERA)} por mês · carro e consórcio juntos"),
    ("Depois do lance",  f"{brl(_depois(1))} por mês se contemplada no mês 1, {brl(_depois(12))} no mês 12 — reajustada pelo {INDICE}"),
    ("Sobra de crédito", "abate as últimas parcelas — não volta em dinheiro enquanto houver parcela"),
]


def faixa():
    """Título e texto da sugestão, derivados da série — se a conta mudar, o texto muda."""
    if ULTIMO_GANHO == 0:
        ganho = "Em 36 meses <b>a troca não ganha em nenhum mês de contemplação</b>, nem trazendo os valores a hoje."
    else:
        ganho = (f"Em 36 meses <b>o ganho só existe se a contemplação sair até o mês {ULTIMO_GANHO}</b>"
                 + (f" — bem antes da maturação do grupo, estimada em {MATURACAO} meses. O horizonte do "
                    f"ganho não cabe no prazo de maturação do grupo." if not TROCA_CABE else
                    f" — horizonte que alcança a maturação do grupo, estimada em {MATURACAO} meses, "
                    f"premissa sem medição estatística; o consórcio não tem data de contemplação."))
    if NOM_NEGATIVOS == N_MESES:
        nominal = (f" Em dinheiro que sai do bolso, com o reajuste, <b>a troca custa mais em qualquer "
                   f"mês</b>: ela troca {RESTAM_FIN} meses de dívida por um plano de {PRAZO} meses.")
    elif NOM_NEGATIVOS:
        nominal = (f" Em dinheiro que sai do bolso, com o reajuste, a troca custa mais em "
                   f"{NOM_NEGATIVOS} dos {N_MESES} meses de contemplação: ela troca {RESTAM_FIN} meses "
                   f"de dívida por um plano de {PRAZO} meses.")
    else:
        nominal = ""
    if TROCA_CABE:
        titulo = "Sugestão: a troca pode valer — com uma condição."
    else:
        titulo = "Sugestão: não trocar pelo consórcio."
    return titulo, "Em 24 meses não há o que ganhar. " + ganho + nominal


def destaque_36():
    """Destaque do cenário de 36 meses — sem "mês 0" quando a troca não ganha em mês nenhum."""
    if ULTIMO_GANHO == 0:
        return ("Não vale", "em 36 meses: a troca não ganha em nenhum mês de contemplação, trazendo os "
                "valores a hoje pelo CDI e com reajuste")
    acima = (f"Ganho acima de R$ 5 mil só até o mês {ULTIMO_5MIL}" if ULTIMO_5MIL
             else "O ganho não passa de R$ 5 mil em nenhum mês")
    return (f"Até o mês {ULTIMO_GANHO}",
            "em 36 meses: último mês de contemplação em que a troca ainda ganha, trazendo os valores "
            f"a hoje pelo CDI e com reajuste. {acima}")


def main():
    faixa_q, faixa_p = faixa()
    d36_v, d36_r = destaque_36()
    linhas = "".join(f'<tr class="{c}"><td class="k">{esc(r)}</td><td class="v a">{esc(a)}</td>'
                     f'<td class="v b">{esc(b)}</td></tr>' for r, a, b, c in LINHAS)
    cons = "".join(f"<li><b>{esc(t)}</b>{esc(d)}</li>" for t, d in CONS)

    pagina = f"""<!doctype html>
<html lang="pt-BR" data-theme="dark"><head>
<meta charset="utf-8"><meta name="viewport" content="width=1200">
<title>Vale trocar o financiamento pelo consórcio?</title>
{design.FONTES}
<style>{design.TOKENS}{CSS}</style>
</head><body>
<div class="card">

<header class="top">
  <p class="eyebrow">Financiamento de veículo · R$ 79.000 liberados · IOF incluído</p>
  <h1>Vale trocar o financiamento pelo consórcio?</h1>
  <p class="tese">Em <b>24 meses a taxa zero</b> não há juros a evitar. Em <b>36 meses</b> há — mas a
  troca só compensa se a contemplação sair <b>cedo</b>, e o consórcio não tem data de contemplação.</p>
</header>

<div class="hero">
  <div class="kpi"><span class="v">Não vale</span>
    <span class="r">em 24 meses: juros zero, nada a economizar — nem trazendo os valores a hoje, em
    nenhum mês de contemplação. A troca acrescentaria os {pct(K)} do consórcio</span></div>
  <div class="kpi on"><span class="v">{d36_v}</span>
    <span class="r">{d36_r}</span></div>
  <div class="kpi"><span class="v">{brl(ESPERA)}</span>
    <span class="r">por mês enquanto não contempla: parcela do carro mais a reduzida do consórcio.
    Cada mês de espera reduz o ganho</span></div>
</div>

<figure class="fig">
  <figcaption class="cap">Ganho da troca por mês de contemplação · cenário de 36 meses · com reajuste
  pelo {INDICE} · linha cheia: valor presente a CDI · tracejada: desembolso nominal · degraus nos meses 13 e 25:
  reajuste anual do crédito e das parcelas</figcaption>
  {grafico()}
</figure>

<div class="grid">
  <div>
    <h2>Lado a lado</h2>
    <table>
      <thead><tr><th></th><th class="a">24 meses · taxa zero</th><th class="b">36 meses · R$ 3.000</th></tr></thead>
      <tbody>{linhas}</tbody>
    </table>
  </div>
  <div>
    <h2>O consórcio para quitar o de 36 meses</h2>
    <ul class="tr">{cons}</ul>
  </div>
</div>

<div class="faixa">
  <p class="q">{faixa_q}</p>
  <p>{faixa_p}</p>
</div>

<div class="ficha">
  <h3>Consórcio de veículo — discriminação de custos</h3>
  <dl>
    <div><dt>Crédito</dt><dd>{brl(CARTA)}</dd></div>
    <div><dt>Prazo do plano</dt><dd>{PRAZO} meses</dd></div>
    <div><dt>Taxa de administração + fundo de reserva</dt><dd>{pct(K)} sobre o crédito</dd></div>
    <div><dt>Total dos pagamentos previstos</dt><dd>{brl(TOTAL)}</dd></div>
    <div><dt>Custo sobre o crédito</dt><dd>{brl(TOTAL - CARTA)} · piso, sem seguro</dd></div>
    <div><dt>Parcela integral</dt><dd>{brl2(PARCELA)}</dd></div>
    <div><dt>Parcela reduzida</dt><dd>{brl2(REDUZIDA)}</dd></div>
    <div><dt>Reajuste</dt><dd>anual, pelo {INDICE}</dd></div>
  </dl>
  <p class="obs"><b>Diferença estrutural entre as operações:</b> o consórcio é rateio de custo
  administrativo entre o grupo — autofinanciamento, sem juros de banco —, e o crédito só é liberado
  <b>após a contemplação, por sorteio ou lance, condicionada à existência de recursos no grupo</b>;
  não há data nem probabilidade de contemplação, e contemplação não é carta na mão — ainda há análise
  de crédito e garantias. A quitação de financiamento pelo crédito precisa ser <b>total</b> e do mesmo
  tipo de bem (Res. BCB 285/2023, art. 15). O crédito que sobra depois da quitação <b>abate as
  últimas parcelas do plano</b>; não é entregue em dinheiro enquanto houver parcela a pagar. O lance
  <b>reduz a parcela, não encurta o prazo</b>; o lance embutido é deduzido do próprio crédito. Os meses
  do gráfico são cenários, não previsão.</p>
</div>

<footer>
  <p><b>{esc(CONSULTOR)} · {esc(ASSINATURA)}.</b> Não é material oficial da
  administradora nem da instituição financeira.</p>
  <p>Números de 15/09/2026. Os dois financiamentos são cenários sobre R$ 79.000 liberados, sem o
  contrato em mãos, com 2 parcelas do financiamento já pagas. IOF pelo Decreto 6.306/2007 (0,0082% ao dia até 365 dias, mais 0,38%), meses de 30
  dias, financiado junto; tarifa de cadastro e registro do contrato não incluídos. Consórcio: linha
  automóvel, custo e prazo de contrato real da administradora; parcela reduzida de {pct(REDUCAO, 0)} do fundo comum
  com taxa integral, condição disponível só em alguns grupos; sobra de crédito abatida das últimas
  parcelas; seguro prestamista e eventual taxa de adesão não incluídos, e por isso o custo do consórcio é piso. Maturação do grupo estimada em {MATURACAO} meses pela experiência comercial, sem medição
  estatística. Valor presente a CDI bruto de {CDI_AA[0]} a.a., sem IR ({CDI_AA[1]}); reajuste pelo {INDICE} de
  {INDICE_12M[0]} em 12 meses ({INDICE_12M[1]}). Mudou a premissa, muda a conta.</p>
</footer>

</div></body></html>"""

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    io.open(DESTINO, "w", encoding="utf-8").write(pagina)
    print(f"ok → {os.path.relpath(DESTINO, RAIZ)}")

    if "--png" in sys.argv:
        png = DESTINO[:-5] + ".png"
        bruto = png[:-4] + "-bruto.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=1200,2800",
                        "--virtual-time-budget=6000", f"--screenshot={bruto}", f"file://{DESTINO}"],
                       capture_output=True, check=False)
        # corta o fundo que sobra embaixo e devolve a margem lateral do card
        subprocess.run(["magick", bruto, "-fuzz", "2%", "-trim", "+repage", "-bordercolor", "black",
                        "-border", "112x96", png], capture_output=True, check=True)
        os.remove(bruto)
        print(f"ok → {os.path.relpath(png, RAIZ)}")


if __name__ == "__main__":
    main()
