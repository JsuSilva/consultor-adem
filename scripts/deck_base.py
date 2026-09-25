"""
Base visual dos decks — CSS, ícones, arte de fundo e fotos embutidas, comum a todo deck do repo.

    import deck_base as B
    B.CSS, B.icone("aval"), B.cab("aval", "Título"), B.anim(0), B.datauri("capa.jpg"), B.skyline()

O design (cores e fontes) vem do design.py; este módulo só monta as peças que os decks
compartilham. Nenhuma cor da marca escrita aqui: ACENTO(a) e BRILHO(a) no CSS viram rgba do
acento da config.

Fotos: os decks procuram os slots em saida/fotos/ (fora do Git). Foto que falta não para o
deck — a imagem simplesmente não entra.
"""
import base64
import html
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
import design  # noqa: E402

DIR_FOTOS = os.path.join(RAIZ, "saida", "fotos")


def esc(s): return html.escape(str(s), quote=True)
def brl(v): return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
def brl2(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def pct(v, n=2): return f"{v*100:.{n}f}".replace(".", ",") + "%"

def datauri(nome):
    """Imagem embutida como data URI. O deck é feito para circular — mandado por
    e-mail, aberto do Downloads, servido de outra pasta — e caminho relativo quebra
    em todas essas situações, sem erro visível: o slide só fica preto. Embutir custa
    ~33% de tamanho e resolve de vez."""
    caminho = os.path.join(DIR_FOTOS, nome)
    if not os.path.exists(caminho):
        return ""
    ext = os.path.splitext(nome)[1].lower()
    mime = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp"}.get(ext)
    if not mime:
        return ""
    b64 = base64.b64encode(open(caminho, "rb").read()).decode("ascii")
    return f"data:image/{mime};base64,{b64}"


ICONES = {
  "relogio":  '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
  "queda":    '<polyline points="3 7 9 13 13 9 21 17"/><polyline points="15 17 21 17 21 11"/>',
  "escudo":   '<path d="M12 3l7.5 3v5.2c0 4.6-3.2 8.2-7.5 10.3C7.7 19.4 4.5 15.8 4.5 11.2V6z"/>'
              '<path d="M9.2 12.2l2 2 3.6-4.2"/>',
  "rota":     '<circle cx="6" cy="5.5" r="2.2"/><circle cx="6" cy="18.5" r="2.2"/>'
              '<circle cx="18" cy="12" r="2.2"/><path d="M6 7.7v8.6"/>'
              '<path d="M8.2 5.5h4.3a3.3 3.3 0 0 1 3.3 3.3v1"/>'
              '<path d="M8.2 18.5h4.3a3.3 3.3 0 0 0 3.3-3.3v-1"/>',
  "camadas":  '<path d="M12 3l9 4.8-9 4.8-9-4.8z"/><path d="M3 12.6l9 4.8 9-4.8"/>'
              '<path d="M3 17.2l9 4.8 9-4.8"/>',
  "etiqueta": '<path d="M3 3h7.6L21 13.4 13.4 21 3 10.6z"/><circle cx="7.4" cy="7.4" r="1.5"/>',
  "predio":   '<path d="M4 21V4.5A1.5 1.5 0 0 1 5.5 3h4A1.5 1.5 0 0 1 11 4.5V21"/>'
              '<path d="M11 21V9.5A1.5 1.5 0 0 1 12.5 8h5A1.5 1.5 0 0 1 19 9.5V21"/>'
              '<path d="M2.5 21h19"/><path d="M6.5 7h2M6.5 11h2M6.5 15h2M14 12h2M14 16h2"/>',
  "balanca":  '<path d="M12 3.5v17"/><path d="M5 7.5h14"/><path d="M8 21h8"/>'
              '<path d="M7.2 7.5L4 14.2h6.4z"/><path d="M16.8 7.5L13.6 14.2H20z"/>',
  "funcao":   '<circle cx="7.2" cy="7.2" r="2.6"/><circle cx="16.8" cy="16.8" r="2.6"/>'
              '<path d="M19 5L5 19"/>',
  "regua":    '<rect x="2.5" y="8" width="19" height="8" rx="1.4"/>'
              '<path d="M6.6 8v3.2M10.3 8v4.4M14 8v3.2M17.7 8v4.4"/>',
  "alerta":   '<path d="M12 3.8l9 16.4H3z"/><path d="M12 10v4.2"/>'
              '<circle cx="12" cy="17.6" r=".7" fill="currentColor" stroke="none"/>',
  "aval":     '<circle cx="12" cy="12" r="9"/><path d="M8 12.2l2.8 2.8L16 9"/>',
  "cenarios": '<path d="M4 6.5h16"/><path d="M4 12h11"/><path d="M4 17.5h6"/>'
              '<circle cx="20" cy="6.5" r="1.4" fill="currentColor" stroke="none"/>',
}

def icone(nome):
    return (f'<span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONES[nome]}</svg></span>')


def skyline(larg=1600, alt=300):
    """Horizonte de prédios, desenhado. Torres de altura e largura variáveis, uma
    notavelmente mais alta ao centro-direita. Nenhum prédio real é reproduzido."""
    # (x, largura, altura relativa) — série fixa, para o desenho ser reproduzível
    T = [(20,46,.34),(72,30,.52),(108,38,.44),(152,26,.66),(184,42,.38),(232,30,.58),
         (268,52,.30),(326,34,.72),(366,28,.50),(400,44,.40),(450,26,.62),(482,38,.46),
         (526,30,.80),(562,46,.36),(614,28,.56),(648,36,.48),(690,24,.68),(720,50,.32),
         (776,34,.60),(816,30,1.00),(852,26,.54),(884,44,.40),(934,28,.74),(968,38,.44),
         (1012,30,.58),(1048,46,.34),(1100,26,.64),(1132,36,.46),(1176,30,.78),(1212,42,.38),
         (1260,28,.56),(1294,34,.48),(1334,24,.66),(1364,48,.32),(1418,30,.60),(1454,38,.44),
         (1498,26,.70),(1530,42,.36),(1578,22,.52)]
    base = alt - 26
    p = []
    for x, w, h in T:
        y = base - h * (alt - 60)
        op = .10 + h * .16
        p.append(f'<rect x="{x}" y="{y:.1f}" width="{w}" height="{base-y:.1f}" '
                 f'fill="var(--accent)" opacity="{op:.3f}"/>')
        # marcação de andares: traços finos, só nas torres largas
        if w >= 34:
            k = y + 12
            while k < base - 8:
                p.append(f'<line x1="{x+5}" y1="{k:.1f}" x2="{x+w-5}" y2="{k:.1f}" '
                         f'stroke="#000" stroke-width="1.6" opacity=".30"/>')
                k += 13
    p.append(f'<line x1="0" y1="{base}" x2="{larg}" y2="{base}" stroke="var(--accent)" '
             f'stroke-width="1" opacity=".34"/>')
    for i in range(5):   # linha d\u0027água
        yy = base + 6 + i*4
        p.append(f'<line x1="{(i*57)%140}" y1="{yy}" x2="{larg}" y2="{yy}" '
                 f'stroke="var(--accent)" stroke-width="1" opacity="{.13-i*.022:.3f}" '
                 f'stroke-dasharray="{34+i*13} {22+i*9}"/>')
    return (f'<svg class="sky" viewBox="0 0 {larg} {alt}" preserveAspectRatio="xMidYMax slice" '
            f'aria-hidden="true">{"".join(p)}</svg>')


_CSS_BRUTO = """
html,body{height:100%;overflow:hidden}
body{background:#000;color:#fff}
.deck{position:fixed;inset:0;overflow:hidden;background:#000}
/* Marca, contador, bolinhas, dica e botões vêm de scripts/controles_deck.py — o padrão
   de todas as apresentações. */

.trilho{display:flex;height:100%;width:100%;will-change:transform;
  transition:transform .62s cubic-bezier(.76,0,.24,1)}
.slide{position:relative;height:100%;width:100%;flex:0 0 100%;overflow-y:auto;overflow-x:hidden}
.inner{min-height:100%;display:flex;flex-direction:column;justify-content:center;
  padding:84px clamp(24px,6vw,86px) 76px;max-width:1440px;margin:0 auto}
.slide::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(900px 540px at 50% -10%,ACENTO(.16),transparent 70%)}
.slide.g2::before{background:radial-gradient(760px 460px at 88% 108%,ACENTO(.13),transparent 70%)}
.slide.g3::before{background:none}

[data-anim]{opacity:0;transform:translateY(24px)}
.on [data-anim]{animation:rise .7s cubic-bezier(.76,0,.24,1) forwards;
  animation-delay:calc(var(--i,0) * 85ms + 110ms)}
@keyframes rise{to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){
  [data-anim]{opacity:1;transform:none}.on [data-anim]{animation:none}.trilho{transition:none}}

.eyebrow{font:600 11.5px/1 "IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase;
  color:var(--accent);margin:0}
h1{font:300 clamp(2.1rem,5.4vw,4rem)/1.05 var(--fonte-titulo);letter-spacing:-.03em;
  margin:26px 0 0;max-width:18ch;text-wrap:balance}
h2{font:300 clamp(1.6rem,3.4vw,2.5rem)/1.14 var(--fonte-titulo);letter-spacing:-.025em;
  margin:22px 0 0;max-width:34ch;text-wrap:balance}
b.hi{font-weight:800;color:var(--accent)}
.lead{margin:26px 0 0;max-width:64ch;font:300 clamp(1.05rem,1.45vw,1.3rem)/1.6 var(--fonte-texto);
  color:#D1D5DB}
.lead b{color:#fff;font-weight:600}
/* A .sub fecha um bloco de largura total (figura, tabela, KPIs) em duas ou três linhas:
   presa em 62ch ela abria um buraco à direita. Corre na largura do bloco. A .lead não —
   é a leitura principal do slide e mantém medida. Em slide com foto, as duas continuam
   presas na zona do véu (regra abaixo), para não cobrir o sol na água. */
.sub{margin:18px 0 0;max-width:none;font:300 17px/1.62 var(--fonte-texto);color:#9CA3AF}
.sub b{color:#E5E7EB;font-weight:600}

.cols{display:grid;grid-template-columns:1fr;gap:clamp(24px,4vw,52px);align-items:center}
@media(min-width:900px){.cols.c2{grid-template-columns:1.05fr .95fr;align-items:start}
  .cols.c7{grid-template-columns:1.15fr .85fr}}

.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:34px 0 0}
.kpi{border:1px solid rgba(255,255,255,.10);border-radius:16px;padding:20px 22px;
  background:linear-gradient(140deg,rgba(255,255,255,.045),ACENTO(.03))}
.kpi.on{border-color:BRILHO(.34);background:linear-gradient(140deg,BRILHO(.13),BRILHO(.03))}
.kpi .v{display:block;font:700 clamp(1.5rem,3vw,2.1rem)/1 var(--fonte-titulo);
  letter-spacing:-.025em;font-variant-numeric:tabular-nums}
.kpi.on .v{color:var(--accent)}
.kpi .r{display:block;margin-top:10px;font:300 14px/1.5 var(--fonte-texto);color:#9CA3AF}

table{width:100%;border-collapse:collapse;font-size:15px;font-variant-numeric:tabular-nums}
th{font:600 10px/1.3 "IBM Plex Mono",monospace;letter-spacing:.11em;text-transform:uppercase;
  color:#6B7280;text-align:left;padding:0 10px 11px 0;border-bottom:1px solid rgba(255,255,255,.12)}
th.hi{color:var(--accent)}
td{padding:10px 10px 10px 0;border-bottom:1px solid rgba(255,255,255,.06);color:#D1D5DB}
td.k{color:#9CA3AF;font:300 14px/1.45 var(--fonte-texto);width:34%}
td.v{color:#fff;font-weight:600}
td.hi{color:var(--accent);font-weight:700}

ul.lista{list-style:none;padding:0;margin:30px 0 0;display:grid;gap:10px}
ul.lista li{border:1px solid rgba(255,255,255,.09);border-radius:14px;padding:15px 19px;
  background:rgba(255,255,255,.022);font:300 15px/1.55 var(--fonte-texto);color:#9CA3AF}
ul.lista b{color:#fff;font-weight:600}
ul.lista li>b:first-child,ul.lista li>div>b:first-child{display:block;margin-bottom:4px;
  font:600 15.5px/1.35 var(--fonte-titulo);color:#fff}
ul.lista.num{counter-reset:l}
ul.lista.num li{display:flex;gap:16px;align-items:flex-start}
ul.lista.num li::before{counter-increment:l;content:counter(l,decimal-leading-zero);
  font:600 11px/1.5 "IBM Plex Mono",monospace;color:var(--accent);letter-spacing:.08em;flex:none}

pre.eq{margin:26px 0 0;font:500 13.5px/1.7 "IBM Plex Mono",monospace;color:#9CA3AF;
  border:1px solid rgba(255,255,255,.09);border-radius:14px;padding:20px 22px;
  background:rgba(255,255,255,.022);white-space:pre-wrap;overflow-wrap:anywhere}
pre.eq b{color:var(--accent);font-weight:600}
.fig{margin:30px 0 20px;border:1px solid rgba(255,255,255,.09);border-radius:16px;
  padding:20px 18px 10px;background:rgba(255,255,255,.022)}
svg.g{display:block;width:100%;height:auto}
svg .ax{font:500 11px/1 "IBM Plex Mono",monospace;fill:#6B7280;letter-spacing:.06em}
svg .lb{font:600 12px/1 "IBM Plex Mono",monospace;fill:#9CA3AF;letter-spacing:.06em}
svg .lb.on{fill:var(--accent)}

.nota{margin:28px 0 0;max-width:96ch;font:300 13.5px/1.62 var(--fonte-texto);color:#6B7280}
.nota b{color:#9CA3AF;font-weight:600}

/* camadas de fundo — grade, ruído, foto e skyline */
.slide>.grade,.slide>.ruido,.slide>.foto,.slide>.foto-veu,.slide>.skywrap{
  position:absolute;inset:0;pointer-events:none;z-index:0}
.slide>.grade{background-image:
  linear-gradient(to right,rgba(255,255,255,.045) 1px,transparent 1px),
  linear-gradient(to bottom,rgba(255,255,255,.045) 1px,transparent 1px);
  background-size:76px 76px;
  -webkit-mask-image:radial-gradient(ellipse 78% 58% at 50% 44%,#000 18%,transparent 78%);
  mask-image:radial-gradient(ellipse 78% 58% at 50% 44%,#000 18%,transparent 78%)}
.slide.g3>.grade{opacity:.45}
.slide>.ruido{opacity:.035;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.slide>.foto{background-size:cover;background-position:center;opacity:1}
/* Véu só onde o texto pousa. Ele tem de morrer antes do terço direito — é lá que
   está o sol na água, e escondê-lo era o que matava a imagem. */
.slide>.foto-veu{background:
  radial-gradient(ellipse 66% 84% at 19% 44%,rgba(0,0,0,.92),rgba(0,0,0,.64) 42%,
    rgba(0,0,0,0) 76%),
  linear-gradient(100deg,rgba(0,0,0,.70) 0%,rgba(0,0,0,.40) 30%,rgba(0,0,0,.10) 60%,
    rgba(0,0,0,0) 80%),
  linear-gradient(0deg,rgba(0,0,0,.38),rgba(0,0,0,0) 42%)}
.slide>.skywrap{top:auto;bottom:0;height:min(40vh,330px)}
.slide.capa>.skywrap{height:min(54vh,440px)}
svg.sky{width:100%;height:100%;display:block}
.inner{position:relative;z-index:1}
.slide.capa .inner{padding-bottom:clamp(150px,30vh,300px)}

/* cabeçalho de slide com ícone */
.cab{display:flex;align-items:center;gap:14px;margin:0}
.cab .eyebrow{margin:0}
.ico{display:inline-grid;place-items:center;width:38px;height:38px;border-radius:11px;flex:none;
  border:1px solid BRILHO(.28);background:BRILHO(.09);color:var(--accent)}
.ico svg{width:19px;height:19px}
ul.lista li>.ico{width:30px;height:30px;border-radius:9px;margin-bottom:9px}
ul.lista li>.ico svg{width:15px;height:15px}

/* faixa de duas colunas com marcação de sim/não */
.par{border:1px solid rgba(255,255,255,.09);border-radius:16px;padding:18px 20px;
  background:rgba(255,255,255,.022)}
/* Slide com foto de fundo: o que carrega texto vira caixa opaca, e o que é texto
   solto se contém na zona do véu. Sem isso a copy some sobre o sol na água. */
.slide:has(>.foto) .par,
.slide:has(>.foto) ul.lista li{background:rgba(10,10,10,.90);
  border-color:rgba(255,255,255,.14);backdrop-filter:blur(3px)}
.slide:has(>.foto) .par.nao{background:rgba(6,6,6,.90)}
.slide:has(>.foto) .sub{max-width:54ch}
.slide:has(>.foto) .nota{max-width:56ch}
.par.nao{border-color:rgba(255,255,255,.07);background:rgba(255,255,255,.012)}
/* Premissas do slide 14: eram uma nota de 12px com 1.286 caracteres presa em 39% da tela,
   19 linhas, e um terço do slide vazio. Viram caixa opaca — a mesma regra de todo texto
   que pousa sobre foto neste deck — em três blocos, que já eram três assuntos. A caixa
   para em 64% para o sol da foto continuar à direita. */
.premissas{margin:22px 0 0;max-width:min(64%,860px);display:grid;gap:12px;padding:20px 24px;
  border:1px solid rgba(255,255,255,.14);border-radius:16px;background:rgba(10,10,10,.90);
  backdrop-filter:blur(3px)}
.premissas p{margin:0;font:300 14.5px/1.62 var(--fonte-texto);color:#9CA3AF}
.premissas b{color:#E5E7EB;font-weight:600}
/* Slide 10 (TIR) é o único sem folga na tela alta — 2px em 1512×982. Fica com os tamanhos
   anteriores ali; nas telas baixas as regras de altura já cuidam dele. */
@media (min-height:961px){
  .slide.denso .sub{font-size:15.5px}.slide.denso pre.eq{font-size:12.5px}
  .slide.denso table{font-size:14px}.slide.denso td.k{font-size:12.5px}
  .slide.denso ul.lista li{font-size:13.5px}
  .slide.denso ul.lista li>b:first-child{font-size:14px}
}
.par h3{display:flex;align-items:center;gap:10px;margin:0 0 12px;
  font:600 11px/1 "IBM Plex Mono",monospace;letter-spacing:.13em;text-transform:uppercase;
  color:var(--accent)}
.par.nao h3{color:#9CA3AF}
.par h3 .ico{width:26px;height:26px;border-radius:8px}
.par h3 .ico svg{width:13px;height:13px}
.par.nao h3 .ico{border-color:rgba(255,255,255,.14);background:rgba(255,255,255,.04);color:#9CA3AF}
.par ul{list-style:none;padding:0;margin:0;display:grid;gap:11px}
.par li{font:300 14.5px/1.5 var(--fonte-texto);color:#9CA3AF;
  padding-bottom:11px;border-bottom:1px solid rgba(255,255,255,.055)}
.par li:last-child{border:0;padding-bottom:0}
.par li b{display:block;color:#fff;font:600 15px/1.35 var(--fonte-titulo);
  margin-bottom:3px}

.painel-foto{position:relative;border-radius:16px;overflow:hidden;min-height:clamp(300px,44vh,430px);
  background-size:cover;background-position:center;border:1px solid rgba(255,255,255,.10)}
.painel-veu{position:absolute;inset:0;
  background:linear-gradient(190deg,rgba(0,0,0,.10),rgba(0,0,0,.52));
  box-shadow:inset 0 0 70px rgba(0,0,0,.5)}
@media(min-width:900px){.cols.c6{grid-template-columns:1.9fr .92fr;align-items:stretch}
  .cols.c10{grid-template-columns:1.15fr .92fr .92fr;align-items:start;gap:26px}}

/* Tela baixa (notebook 1600×900, projetor 720p) — o deck se aperta em vez de rolar.
   Remedido em 04/09/2026, com 14 slides: cabem inteiros de 1366×768 a 2560×1440; em
   1280×720 três ainda passam (9, 10 e 12), por 4 a 19px. */
@media (max-height:960px){
  .inner{padding:56px clamp(24px,6vw,86px) 48px}
  h1{font-size:clamp(1.9rem,4.6vw,3.2rem);margin-top:20px}
  h2{font-size:clamp(1.45rem,2.9vw,2.05rem);margin-top:16px}
  .lead{margin-top:18px;font-size:clamp(.95rem,1.3vw,1.06rem)}
  .sub{margin-top:13px;font-size:15px}
  .kpis{margin-top:22px;gap:10px}
  .kpi{padding:15px 17px}
  .kpi .v{font-size:clamp(1.35rem,2.5vw,1.8rem)}
  .kpi .r{margin-top:7px;font-size:12.5px}
  .fig{margin:18px 0 14px;padding:14px 15px 6px}
  ul.lista{margin-top:20px;gap:8px}
  ul.lista li{padding:11px 16px;font-size:13.2px}
  ul.lista li>b:first-child,ul.lista li>div>b:first-child{font-size:13px;margin-bottom:2px}
  .par{padding:14px 17px}
  .par li{font-size:12.8px;padding-bottom:7px}
  .par li b{font-size:14px}
  .par ul{gap:9px}
  table{font-size:13.5px}
  td{padding:8px 10px 8px 0}
  td.k{font-size:13px}
  pre.eq{margin-top:16px;padding:15px 17px;font-size:11.4px;line-height:1.65}
  .nota{margin-top:9px;font-size:11.8px;line-height:1.46}
  .premissas{padding:15px 18px;gap:9px}.premissas p{font-size:12.6px;line-height:1.52}
  .cab .ico{width:32px;height:32px}
  .cab .ico svg{width:16px;height:16px}
}

@media (max-height:800px){
  .inner{padding:36px clamp(18px,4.5vw,66px) 30px}
  h2{font-size:clamp(1.3rem,2.5vw,1.75rem);margin-top:12px}
  .lead{margin-top:14px;font-size:14.5px}
  .sub{margin-top:9px;font-size:13px}
  .kpis{margin-top:16px}.kpi{padding:12px 14px}
  .fig{margin:14px 0 7px;padding:11px 12px 4px}
  ul.lista{margin-top:15px;gap:6px}
  ul.lista li{padding:9px 14px;font-size:12px}
  .par{padding:10px 12px}.par li{font-size:11.2px;line-height:1.38;padding-bottom:5px}
  .par ul{gap:5px}.par li b{font-size:11.8px}
  table{font-size:12.2px}td{padding:6px 9px 6px 0}td.k{font-size:12.2px}
  .kpi .r{font-size:11.5px}
  .premissas{padding:12px 15px;gap:7px;margin-top:14px}.premissas p{font-size:11.4px;line-height:1.45}
  pre.eq{margin-top:13px;padding:12px 14px;font-size:10.6px;line-height:1.6}
  .nota{margin-top:13px;font-size:10.8px}
  .cab{gap:10px}.cab .ico{width:28px;height:28px}.cab .ico svg{width:14px;height:14px}
  .eyebrow{font-size:10.5px}
  .par h3{margin-bottom:9px;font-size:10px}
  .par li b{font-size:12.3px;margin-bottom:2px}
  ul.lista li>b:first-child,ul.lista li>div>b:first-child{font-size:12.2px}
  .fig .cap{margin-bottom:8px}
  svg.g{max-height:29vh}
}

"""


def _css():
    """CSS com os tons do acento da config: ACENTO(a) e BRILHO(a) viram rgba do acento e do
    brilho de design.ESPELHO — nenhuma cor da marca escrita aqui."""
    tons = {"ACENTO": design.ESPELHO["accent-500"], "BRILHO": design.ESPELHO["accent-400"]}
    return re.sub(r"(ACENTO|BRILHO)\(([.\d]+)\)",
                  lambda m: design.rgba(tons[m.group(1)], m.group(2)), _CSS_BRUTO)


CSS = _css()


def cab(ic, texto, i=0):
    return (f'<div class="cab"{anim(i)}>{icone(ic)}'
            f'<p class="eyebrow">{esc(texto)}</p></div>')


def anim(i, css=""):
    """Atraso da animação + CSS extra do elemento. O `css` entra AQUI porque um
    segundo atributo `style=` no mesmo elemento é silenciosamente ignorado pelo
    navegador — foi assim que vários espaçamentos deste deck deixaram de valer."""
    return f' data-anim style="--i:{i}{";" + css if css else ""}"'

