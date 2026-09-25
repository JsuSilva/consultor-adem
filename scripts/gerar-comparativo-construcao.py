#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera saida/comparativo-construcao.html — o card comparativo consórcio × financiamento Caixa de
construção, para exportar como imagem.

    python3 scripts/gerar-comparativo-construcao.py

Duas regras:

1. **O design vem do design.py.** Nenhuma cor escrita aqui.
2. **O conteúdo vem da conta do `calculista`**: o lado do consórcio sai dos parâmetros da linha
   imóvel em config/consultor.json (taxa de administração, fundo de reserva, prazo e índice de
   reajuste, via scripts/config.py — campo vazio para o script com aviso); o lado do
   financiamento sai da taxa de juros `mercado.juros_imobiliario_am` (com a fonte em
   `mercado._fonte`) e dos parâmetros públicos da Caixa — TR, tarifa mensal, vistoria —,
   congelados no bloco CASO abaixo com fonte e data. A curva de custo é recalculada a cada
   execução (ver `_financiamento`). Mudou a conta, muda aqui — nesta ordem, nunca ao contrário.

Os textos que dependem do resultado (quem sai mais barato na conclusão, renda exigida) são
condicionais: a peça nunca afirma o que a conta não sustenta.

O bloco CASO é o exemplo que acompanha o modelo (obra de 12 meses, crédito de R$ 250 mil, quitação
na venda). Para outro caso, troque o bloco e os textos do corpo.

O card é um artefato de campo: passa pelas regras de
conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md, e só vai a pessoa real
com aval do consultor naquela rodada.

Tema fixo em escuro: artefato feito para virar PNG, não para herdar o tema do leitor.
"""
import io, os, sys, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
import design
from config import carregar, exigir

DESTINO = os.path.join(RAIZ, "saida", "comparativo-construcao.html")

# ─────────────────────────────────────────────────────────────────────────────
# CASO — exemplo editável. Nada aqui é calculado na prosa.
# ─────────────────────────────────────────────────────────────────────────────

CREDITO_V = 250_000.00
CREDITO = "R$ 250.000"

OBRA_MESES = 12          # cronograma presumido: uma medição por mês, liberações iguais
PRAZO_FIN = 360          # meses de amortização (SAC) depois da obra
JANELA = 20              # meses de negociação após a obra mostrados no gráfico
MARCOS = (0, 3, 6, 12)   # meses marcados na curva

# parâmetros públicos da Caixa e do Banco Central (fonte e data no rodapé)
TR_AM = 0.00169          # TR de 01/09/2026 — BCB, SGS 226
TARIFA_MES = 25.00       # tarifa de administração mensal do contrato — tabela de tarifas Caixa, 03/07/2026
VISTORIA = 750.00        # vistoria por medição na fase de obra — mesma tabela

# ─────────────────────────────────────────────────────────────────────────────
# CONSÓRCIO — linha imóvel, lida de config/consultor.json. Parcela e renda são DERIVADAS aqui,
# nunca na prosa. Lida só no main(), para quem importa o CSS deste módulo não precisar da linha.
# ─────────────────────────────────────────────────────────────────────────────

def pct(v): return f"{v:.2f}".replace(".", ",")


def _financiamento(i):
    """Custo do crédito no financiamento (SAC), acumulado até cada mês de negociação após a obra.

    Fase de obra: o crédito é liberado em OBRA_MESES parcelas iguais, no início de cada mês; a TR
    corrige o saldo (AM = SD × TR) e os juros incidem sobre o saldo corrigido ((SD + AM) × i),
    como na cartilha da Caixa; cada mês paga tarifa e uma vistoria.
    Depois da obra: amortização SAC sobre o saldo corrigido em PRAZO_FIN meses; o custo de cada
    mês é juros + TR + tarifa. A amortização não entra no custo: volta como saldo menor na
    quitação. MIP e DFI ficam de fora (sem tabela pública) — o custo é piso.

    Devolve (custo acumulado por mês 0..JANELA, 1º encargo da obra, 1ª parcela de amortização,
    TR acumulada em obra + 12 meses)."""
    sd = tr_total = custo = 0.0
    encargo_1 = None
    for _ in range(OBRA_MESES):
        sd += CREDITO_V / OBRA_MESES
        am = sd * TR_AM
        juros = (sd + am) * i
        sd += am
        tr_total += am
        custo += am + juros + TARIFA_MES + VISTORIA
        if encargo_1 is None:
            encargo_1 = juros + TARIFA_MES + VISTORIA
    amort = sd / PRAZO_FIN
    curva, parcela_1 = [custo], None
    for k in range(1, JANELA + 1):
        am = sd * TR_AM
        juros = (sd + am) * i
        sd += am
        if k <= 12:
            tr_total += am
        if parcela_1 is None:
            parcela_1 = amort + juros + TARIFA_MES
        custo += am + juros + TARIFA_MES
        sd -= amort
        curva.append(custo)
    return curva, encargo_1, parcela_1, tr_total


def _pontos_curva():
    return list(enumerate(CURVA_TODA))


def _cruzamento(piso):
    """Mês de negociação em que a curva do financiamento alcança o custo fixo do consórcio —
    interpolação linear entre os pontos da curva."""
    pts = _pontos_curva()
    if piso <= pts[0][1]:
        return float(pts[0][0])
    for (m0, v0), (m1, v1) in zip(pts, pts[1:]):
        if v0 <= piso <= v1:
            return m0 + (piso - v0) / (v1 - v0) * (m1 - m0)
    sys.exit(f"ERRO: o custo do consórcio fica acima da curva do financiamento em toda a janela de "
             f"{JANELA} meses do gráfico — refaça o bloco CASO antes de gerar este card.")


def _conta():
    global TAXA_ADM, FUNDO, K, PRAZO_CONS, INDICE, CATEGORIA, PARCELA_CONS, RENDA_CONS
    global TAXA_AA_CONS, CONSORCIO_PISO, CRUZA_PISO, LINHAS, CONSULTOR, ASSINATURA
    global JUROS_AM, JUROS_FONTE, CURVA_TODA, CURVA, CUSTO_MES, ENCARGO_OBRA_1, PARCELA_FIN_1A
    global RENDA_FIN, TR_24M, TRAVAS, JUROS_AA, INCC_12M
    cfg = carregar()
    JUROS_AM = exigir(cfg, "mercado.juros_imobiliario_am")
    JUROS_FONTE = exigir(cfg, "mercado._fonte")
    INCC_12M = exigir(cfg, "mercado.incc_12m")   # fração; fonte em mercado._fonte
    JUROS_AA = (1 + JUROS_AM) ** 12 - 1          # equivalente anual composto da taxa mensal
    TAXA_ADM = exigir(cfg, "produto.linhas.imovel.taxa_administracao")
    FUNDO = exigir(cfg, "produto.linhas.imovel.fundo_reserva")      # 0 quando a linha não tem
    PRAZO_CONS = exigir(cfg, "produto.linhas.imovel.prazo_meses")
    INDICE = exigir(cfg, "produto.linhas.imovel.indice_reajuste")
    CONSULTOR = exigir(cfg, "consultor.nome")
    ASSINATURA = exigir(cfg, "consultor.assinatura")
    K = TAXA_ADM + FUNDO
    CATEGORIA = CREDITO_V * (1 + K)
    PARCELA_CONS = CATEGORIA / PRAZO_CONS
    RENDA_CONS = PARCELA_CONS / 0.30        # mesma régua dos 30% aplicada ao financiamento
    TAXA_AA_CONS = K * 100 / PRAZO_CONS * 12   # custo do plano diluído no prazo — não é juro
    CONSORCIO_PISO = CATEGORIA - CREDITO_V

    CURVA_TODA, ENCARGO_OBRA_1, PARCELA_FIN_1A, TR_24M = _financiamento(JUROS_AM)
    CURVA = [(m, CURVA_TODA[m]) for m in MARCOS]
    CUSTO_MES = (CURVA_TODA[12] - CURVA_TODA[6]) / 6   # custo médio de um mês a mais, meses 7 a 12
    RENDA_FIN = PARCELA_FIN_1A / 0.30
    CRUZA_PISO = _cruzamento(CONSORCIO_PISO)  # meses de negociação até o financiamento alcançar o consórcio

    # rótulo, consórcio, financiamento, destaque
    LINHAS = [
        ("Crédito",                    CREDITO,                    CREDITO,                     ""),
        ("Prazo",                      f"{PRAZO_CONS} meses",      f"{OBRA_MESES} de obra + {PRAZO_FIN}", ""),
        ("Recursos próprios exigidos", "não há",                   "R$ 100.000 + giro da obra", "c"),
        ("Custo do crédito",           f"{pct(TAXA_AA_CONS)}% a.a. + {INDICE} *",
                                                                   f"{pct(JUROS_AM*100)}% a.m. · {pct(JUROS_AA*100)}% a.a. + TR *", ""),
        ("Parcela",                    f"R$ {PARCELA_CONS:,.0f}".replace(",", "."),
                                                                   f"{brl(ENCARGO_OBRA_1)} → {brl(PARCELA_FIN_1A)}", ""),
        ("Renda comprovada",           f"R$ {RENDA_CONS:,.0f}".replace(",", "."), brl(RENDA_FIN),  "c"),
        ("Quando o dinheiro sai",      "após a contemplação",      "por medição, data contratada", "f"),
        ("Se a obra encarecer",        "crédito acompanha o índice", "valor fixo, sem complemento", "c"),
    ]

    # as travas do financiamento — tudo publicado pela própria Caixa
    TRAVAS = [
        ("Moradia própria",   "a linha veda construção de empreendimento para comercialização"),
        ("Reembolso",         f"você banca a etapa, a vistoria libera depois — {brl(VISTORIA)} por vistoria"),
        ("Últimos 5%",        "só saem com habite-se e averbação na matrícula"),
        ("TR fora da taxa",   f"corrige o saldo todo mês — ~{brl(TR_24M)} em {OBRA_MESES + 12} meses"),
        ("MIP e DFI",         "obrigatórios, sem tabela pública — todo custo aqui é piso"),
    ]

# ─────────────────────────────────────────────────────────────────────────────

def esc(s): return html.escape(str(s), quote=True)

def brl(v): return f"R$ {v:,.0f}".replace(",", ".")


def grafico(larg=1000, alt=340):
    """Curva do custo do financiamento contra a régua fixa do consórcio.
    SVG inline, sem biblioteca, cores só por token do design.py."""
    ml, mr, mt, mb = 74, 26, 26, 52
    W, H = larg - ml - mr, alt - mt - mb
    topo = max(max(CURVA_TODA), CONSORCIO_PISO) * 1.08
    x1, y1 = float(JANELA), float(-(-topo // 10000) * 10000)   # meses de negociação, custo

    def X(m): return ml + W * (m / x1)
    def Y(v): return mt + H * (1 - v / y1)

    p = []
    # grade horizontal
    passo = 20000 if y1 <= 120000 else 40000
    for v in range(0, int(y1), passo):
        p.append(f'<line x1="{ml}" y1="{Y(v):.1f}" x2="{ml+W}" y2="{Y(v):.1f}" '
                 f'stroke="var(--rule)" stroke-width="1"/>')
        p.append(f'<text x="{ml-10}" y="{Y(v)+4:.1f}" text-anchor="end" class="ax">{brl(v)}</text>')
    # eixo dos meses
    for m in range(0, JANELA, 3):
        p.append(f'<text x="{X(m):.1f}" y="{mt+H+20}" text-anchor="middle" class="ax">{m}</text>')
    p.append(f'<text x="{ml+W/2:.1f}" y="{mt+H+42}" text-anchor="middle" class="ax">'
             f'MESES DE NEGOCIAÇÃO APÓS A CONCLUSÃO DA OBRA</text>')

    # réguas do consórcio
    p.append(f'<line x1="{ml}" y1="{Y(CONSORCIO_PISO):.1f}" x2="{ml+W}" y2="{Y(CONSORCIO_PISO):.1f}" '
             f'stroke="var(--ink-2)" stroke-width="2"/>')
    p.append(f'<text x="{ml+12}" y="{Y(CONSORCIO_PISO)-10:.1f}" class="lb">'
             f'CONSÓRCIO · {brl(CONSORCIO_PISO)} FIXOS</text>')

    # curva do financiamento — âncoras da conta, prolongadas pelo custo mensal
    pts = _pontos_curva()
    d = " ".join(("M" if i == 0 else "L") + f"{X(m):.1f} {Y(v):.1f}" for i, (m, v) in enumerate(pts))
    p.append(f'<path d="{d}" fill="none" stroke="var(--accent)" stroke-width="3" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    for m, v in CURVA:
        p.append(f'<circle cx="{X(m):.1f}" cy="{Y(v):.1f}" r="5" fill="var(--accent)"/>')
    p.append(f'<text x="{X(0)+12:.1f}" y="{Y(CURVA[0][1])+5:.1f}" class="lb on">'
             f'{brl(CURVA[0][1])} SE VENDER NA CONCLUSÃO</text>')

    # o cruzamento
    p.append(f'<line x1="{X(CRUZA_PISO):.1f}" y1="{mt}" x2="{X(CRUZA_PISO):.1f}" y2="{mt+H}" '
             f'stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 4" opacity=".7"/>')
    p.append(f'<circle cx="{X(CRUZA_PISO):.1f}" cy="{Y(CONSORCIO_PISO):.1f}" r="7" '
             f'fill="none" stroke="var(--accent)" stroke-width="2.5"/>')

    return (f'<svg class="g" viewBox="0 0 {larg} {alt}" width="{larg}" height="{alt}" '
            f'role="img" aria-label="Custo do financiamento por mês de negociação, contra o custo '
            f'fixo do consórcio">{"".join(p)}</svg>')


CSS = """
html,body{background:var(--ground)}
.card{width:1200px;margin:0 auto;padding:52px 56px 40px;background:var(--ground)}
header.top{border-bottom:2px solid var(--ink);padding-bottom:26px;margin-bottom:30px}
.eyebrow{font:600 12px/1 "IBM Plex Mono",monospace;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);margin:0 0 14px}
h1{font:800 58px/1.02 var(--fonte-titulo);letter-spacing:-.03em;margin:0 0 16px;
  text-wrap:balance;max-width:19ch}
.tese{margin:0;max-width:74ch;font-size:19px;line-height:1.5;color:var(--ink-2)}
.tese b{color:var(--ink);font-weight:600}

.hero{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 30px}
.kpi{background:var(--surface);border:1px solid var(--rule);border-radius:var(--radius);
  padding:20px 22px}
.kpi.on{border-color:var(--accent);background:var(--accent-soft)}
.kpi .v{font:700 40px/1 var(--fonte-titulo);letter-spacing:-.025em;
  font-variant-numeric:tabular-nums;display:block}
.kpi.on .v{color:var(--accent)}
.kpi .r{font:500 13px/1.45 var(--fonte-texto);color:var(--ink-3);margin-top:10px;display:block}

.fig{margin:0 0 34px;padding:22px 20px 14px;background:var(--surface);border:1px solid var(--rule);
  border-radius:var(--radius)}
.fig .cap{font:600 11px/1.4 "IBM Plex Mono",monospace;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 12px}
svg.g{display:block;width:100%;height:auto}
svg .ax{font:500 11px/1 "IBM Plex Mono",monospace;fill:var(--ink-3);letter-spacing:.06em}
svg .lb{font:600 11.5px/1 "IBM Plex Mono",monospace;fill:var(--ink-2);letter-spacing:.08em}
svg .lb.on{fill:var(--accent)}
svg .lb.dim{fill:var(--ink-3)}

.grid{display:grid;grid-template-columns:1.35fr 1fr;gap:22px;margin:0 0 30px}
h2{font:700 14px/1.3 "IBM Plex Mono",monospace;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 14px;padding-bottom:10px;border-bottom:1px solid var(--rule)}
table{width:100%;border-collapse:collapse;font-size:14.5px}
th{font:600 10.5px/1.3 "IBM Plex Mono",monospace;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);text-align:left;padding:0 10px 10px 0;border-bottom:1px solid var(--rule)}
th.a{color:var(--ink-2)}
th.b{color:var(--accent)}
td{padding:11px 10px 11px 0;border-bottom:1px solid var(--rule-2);vertical-align:top;
  color:var(--ink-2)}
td.k{color:var(--ink-3);font:500 12.5px/1.45 var(--fonte-texto);width:31%}
td.v{color:var(--ink);font-weight:600}
tr.c td.b{color:var(--accent)}
tr.f td.a{color:var(--ink);font-weight:700}

ul.tr{list-style:none;padding:0;margin:0}
ul.tr li{border-bottom:1px solid var(--rule-2);padding:11px 0;font-size:13.5px;line-height:1.5;
  color:var(--ink-2)}
ul.tr b{color:var(--ink);font-weight:600;display:block;margin-bottom:3px;
  font-family:var(--fonte-titulo);font-size:13.5px}

.faixa{background:var(--accent-soft);border:1px solid var(--accent);border-radius:var(--radius);
  padding:24px 28px;margin:0 0 30px}
.faixa .q{font:700 25px/1.3 var(--fonte-titulo);color:var(--accent);margin:0 0 10px;
  letter-spacing:-.02em}
.faixa p{margin:0;font-size:15.5px;line-height:1.55;color:var(--ink-2);max-width:80ch}
.faixa p b{color:var(--ink)}

.ficha{background:var(--surface-2);border:1px solid var(--rule);border-radius:var(--radius);
  padding:20px 22px;margin:0 0 22px}
.ficha h3{font:600 11px/1.3 "IBM Plex Mono",monospace;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 12px}
.ficha dl{display:grid;grid-template-columns:repeat(4,1fr);gap:12px 22px;margin:0}
.ficha dt{font:500 11px/1.4 var(--fonte-texto);color:var(--ink-3)}
.ficha dd{margin:2px 0 0;font:600 14px/1.35 var(--fonte-titulo);color:var(--ink)}
.ficha .obs{margin:14px 0 0;font-size:12.5px;line-height:1.55;color:var(--ink-3);max-width:100ch}
.ficha .obs b{color:var(--ink-2)}

footer{border-top:2px solid var(--ink);padding-top:18px;font:400 11.5px/1.6 var(--fonte-texto);
  color:var(--ink-3)}
footer p{margin:0 0 7px;max-width:106ch}
footer b{color:var(--ink-2);font-weight:600}
"""


def main():
    _conta()
    linhas = []
    for rot, cons, fin, cls in LINHAS:
        linhas.append(
            f'<tr class="{cls}"><td class="k">{esc(rot)}</td>'
            f'<td class="v a">{esc(cons)}</td><td class="v b">{esc(fin)}</td></tr>')

    travas = "".join(f"<li><b>{esc(t)}</b>{esc(d)}</li>" for t, d in TRAVAS)

    # Textos que dependem do resultado da conta — nunca afirmar o que ela não sustenta.
    fin_mais_barato = CURVA_TODA[0] < CONSORCIO_PISO
    n = round(CRUZA_PISO)
    if not fin_mais_barato:
        folga_v, folga_r = "Nenhum mês", ("de folga: vendendo na conclusão da obra, o custo do "
                                          "financiamento já passa o custo fixo do consórcio")
    else:
        folga_v = "menos de 1 mês" if n < 1 else f"~{n} {'mês' if n == 1 else 'meses'}"
        folga_r = "de venda após a obra antes de o financiamento alcançar o custo do consórcio"
    renda = (f", com renda comprovada de {brl(RENDA_CONS)} contra {brl(RENDA_FIN)} do financiamento"
             if RENDA_CONS < RENDA_FIN else "")
    if fin_mais_barato:
        faixa = (f"""Vendeu rápido, <b>o financiamento é o crédito certo desta obra</b>. O consórcio
  não disputa melhor cenário que o financiamento da Caixa: ele vale como <b>plano B que pode rodar
  em paralelo se a parcela couber no orçamento</b> — sem entrada, sem projeto, sem vistoria{renda} —
  e que o caixa desta venda pode acionar como lance, antes de a próxima obra chegar.""")
    else:
        faixa = (f"""Nesta conta, <b>o financiamento custa mais que o consórcio mesmo com a venda na
  conclusão da obra</b>. Ainda assim, o crédito do consórcio só é liberado após a contemplação, sem
  data: ele não paga esta obra. Vale como <b>plano B que pode rodar em paralelo se a parcela couber
  no orçamento</b> — sem entrada, sem projeto, sem vistoria{renda} — e que o caixa desta venda pode
  acionar como lance, antes de a próxima obra chegar.""")

    pagina = f"""<!doctype html>
<html lang="pt-BR" data-theme="dark"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=1200">
<title>Quanto tempo você tem para vender</title>
{design.FONTES}
<style>{design.TOKENS}{CSS}</style>
</head><body>
<div class="card">

<header class="top">
  <p class="eyebrow">Construção de casa para venda · crédito de {esc(CREDITO)}</p>
  <h1>Quanto tempo você tem para vender</h1>
  <p class="tese">O financiamento cobra <b>por mês</b>. O consórcio cobra <b>uma vez só</b>.
  Por isso a pergunta não é qual é o mais barato — é <b>em quanto tempo preciso vender para o
  financiamento continuar sendo mais vantajoso</b>.</p>
</header>

<div class="hero">
  <div class="kpi on"><span class="v">{folga_v}</span>
    <span class="r">{folga_r}</span></div>
  <div class="kpi"><span class="v">{brl(CUSTO_MES)}</span>
    <span class="r">o que cada mês a mais até a venda acrescenta ao custo do crédito, depois que a
    obra termina: juros, tarifa e correção do saldo pela TR. A parcela desembolsada é de
    {brl(PARCELA_FIN_1A)} — a amortização não entra na conta porque volta como saldo menor na
    quitação</span></div>
  <div class="kpi"><span class="v">{brl(CURVA[0][1])}</span>
    <span class="r">custo do crédito se vender na conclusão — contra {brl(CONSORCIO_PISO)}
    fixos do consórcio</span></div>
</div>

<figure class="fig">
  <figcaption class="cap">Custo do crédito · financiamento Caixa (SAC) × consórcio de imóvel ·
  mesmo crédito de {esc(CREDITO)}</figcaption>
  {grafico()}
</figure>

<div class="grid">
  <div>
    <h2>Lado a lado</h2>
    <table>
      <thead><tr><th></th><th class="a">Consórcio de imóvel</th>
      <th class="b">Financiamento Caixa</th></tr></thead>
      <tbody>{"".join(linhas)}</tbody>
    </table>
  </div>
  <div>
    <h2>O que trava no financiamento</h2>
    <ul class="tr">{travas}</ul>
  </div>
</div>

<div class="faixa">
  <p class="q">Em quanto tempo essa casa vende?</p>
  <p>{faixa}</p>
</div>

<div class="ficha">
  <h3>Consórcio de imóvel — discriminação de custos</h3>
  <dl>
    <div><dt>Crédito</dt><dd>{esc(CREDITO)}</dd></div>
    <div><dt>Prazo do plano</dt><dd>{PRAZO_CONS} meses</dd></div>
    <div><dt>Taxa de administração</dt><dd>{pct(TAXA_ADM*100)}% sobre o crédito</dd></div>
    <div><dt>Fundo de reserva</dt><dd>{"não há nesta linha" if not FUNDO else pct(FUNDO*100) + "% sobre o crédito"}</dd></div>
    <div><dt>Total dos pagamentos previstos</dt><dd>{brl(CATEGORIA)}</dd></div>
    <div><dt>Custo sobre o crédito</dt><dd>{pct(K*100)}%</dd></div>
    <div><dt>Parcela</dt><dd>{brl(PARCELA_CONS)}</dd></div>
    <div><dt>Reajuste</dt><dd>existe, anual, por índice contratual</dd></div>
  </dl>
  <p class="obs"><b>* As duas taxas estão em regimes diferentes e não se comparam como número.</b>
  No consórcio, {pct(TAXA_AA_CONS)}% a.a. é o custo do plano — {pct(K*100)}% sobre o
  crédito, cobrado uma vez — diluído pelos {PRAZO_CONS} meses; ele não incide sobre saldo e não
  cresce se o plano durar mais. No financiamento, {pct(JUROS_AM*100)}% a.m. ({pct(JUROS_AA*100)}% a.a.,
  equivalente composto) são juros que incidem
  <b>todo mês sobre o saldo devedor</b>, e por isso o custo aumenta enquanto a dívida existir.
  {esc(INDICE)} e TR corrigem os valores de cada lado e não estão dentro desses percentuais.</p>
  <p class="obs"><b>Diferença estrutural entre as operações:</b> o consórcio é rateio de custo
  administrativo entre o grupo — autofinanciamento, sem juros de banco —, e o crédito só é liberado
  <b>após a contemplação, por sorteio ou lance, condicionada à existência de recursos no grupo</b>;
  não há data nem probabilidade de contemplação, e contemplação não é carta na mão — ainda há
  análise de crédito e garantias. Enquanto espera, o valor pago não fica disponível a você. O lance
  <b>reduz a parcela, não encurta o prazo</b>; o lance embutido é deduzido do próprio crédito.
  O financiamento é amortização mais juros sobre crédito recebido por medição, em data contratada.</p>
</div>

<footer>
  <p><b>{esc(CONSULTOR)} · {esc(ASSINATURA)}.</b> Não é material oficial da
  administradora nem parecer da Caixa.</p>
  <p>Premissas do caso: obra de {OBRA_MESES} meses, quitação na venda, terreno próprio em
  garantia, cronograma de {OBRA_MESES} medições presumido. Projeções marcadas como tais — mudou a
  premissa, muda a conta. Juros do financiamento de {pct(JUROS_AM*100)}% a.m. + TR:
  {esc(JUROS_FONTE)}. TR de {f"{TR_AM*100:.3f}".replace(".", ",")}% a.m. (Banco Central, SGS 226, 01/09/2026); tarifa
  mensal de {brl(TARIFA_MES)} e vistoria de {brl(VISTORIA)} por medição (tabela de tarifas Caixa,
  03/07/2026). Regras de enquadramento, tarifas e liberação por medição: caixa.gov.br e Cartilha
  Habitação PF v.12 (dez/2025). Reajuste do consórcio projetado pelo índice contratual corrente
  (INCC de {pct(INCC_12M*100)}% em 12 meses: {esc(JUROS_FONTE)}).</p>
</footer>

</div>
</body></html>"""

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    io.open(DESTINO, "w", encoding="utf-8").write(pagina)
    print(f"ok → {os.path.relpath(DESTINO, RAIZ)}")


if __name__ == "__main__":
    main()
