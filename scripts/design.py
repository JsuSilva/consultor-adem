"""
Design system — a identidade visual do consultor, lida de config/consultor.json.

Fonte: config/consultor.json → `identidade_visual`
  acento          cor primária da marca, em hexadecimal (#RRGGBB)
  acento_brilho   a versão clara do acento, usada sobre fundo escuro
  fundo_padrao    "escuro" ou "claro" — o tema de quem não declara preferência
  fonte_titulo    família do Google Fonts para títulos
  fonte_texto     família do Google Fonts para texto

**Campo vazio cai no padrão NEUTRO deste arquivo** — cinzas, um azul sóbrio e Inter. O neutro é
só o ponto de partida para a peça sair; não é a identidade de ninguém. Quem quer a sua marca
preenche `identidade_visual` pela skill `configuracao`.

Único ponto de verdade: os geradores importam daqui. Mudou aqui (ou na config), muda em todo
artefato.

    from design import FONTES, TOKENS          # ou: import design; design.ESPELHO["accent-400"]

Nomes públicos: FONTES, TOKENS, ESPELHO (a escala, degrau por degrau), rgba(hexa, alfa) e
TEMA_PADRAO ("dark"/"light", para o `data-theme` de quem quiser fixar o tema da config).

A escala do acento (accent-100…900) é DERIVADA do acento e do brilho: tons claros misturando com
branco, tons escuros misturando com preto. Sem `acento_brilho`, o brilho também é derivado. As
fontes precisam existir no Google Fonts com os pesos pedidos em FONTES; fonte que não existir lá
cai em system-ui.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import carregar, valor

# ── padrão neutro — só vale para campo vazio ────────────────────────────────
NEUTRO = {
    "acento": "#2F6690",          # azul sóbrio
    "acento_brilho": "#6FA8DC",   # 8,4:1 sobre preto
    "fundo_padrao": "escuro",
    "fonte_titulo": "Inter",
    "fonte_texto": "Inter",
}

_cfg = carregar()


def _campo(nome):
    v = valor(_cfg, f"identidade_visual.{nome}")
    if isinstance(v, str):
        v = v.strip()
    return v or NEUTRO[nome]


def _hexa(nome):
    v = _campo(nome)
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", v):
        sys.exit(f"ERRO: `identidade_visual.{nome}` = {v!r} não é cor #RRGGBB em config/consultor.json.")
    return v.upper()


def _rgb(hexa):
    return tuple(int(hexa[i:i + 2], 16) for i in (1, 3, 5))


def _misturar(hexa, com, t):
    """Mistura `hexa` com `com` (#FFFFFF ou #000000) na proporção t (0 = hexa, 1 = com)."""
    a, b = _rgb(hexa), _rgb(com)
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def rgba(hexa, alfa):
    """`rgba(r,g,b,alfa)` de um hexadecimal — para sombra, véu e brilho no tom do acento."""
    r, g, b = _rgb(hexa)
    return f"rgba({r},{g},{b},{alfa})"


ACENTO = _hexa("acento")
BRILHO = (_hexa("acento_brilho") if valor(_cfg, "identidade_visual.acento_brilho")
          or not valor(_cfg, "identidade_visual.acento")
          else _misturar(ACENTO, "#FFFFFF", .25))
FUNDO = _campo("fundo_padrao")
if FUNDO not in ("escuro", "claro"):
    sys.exit(f"ERRO: `identidade_visual.fundo_padrao` = {FUNDO!r}; use \"escuro\" ou \"claro\".")
TEMA_PADRAO = "dark" if FUNDO == "escuro" else "light"
TITULO, TEXTO = _campo("fonte_titulo"), _campo("fonte_texto")

# A escala, degrau por degrau (nome do degrau → hex). `accent-*` sai do acento; `dark-*` é a
# escala neutra de cinzas, a mesma para todo consultor.
ESPELHO = {
    "accent-100": _misturar(ACENTO, "#FFFFFF", .85), "accent-200": _misturar(ACENTO, "#FFFFFF", .65),
    "accent-400": BRILHO, "accent-500": ACENTO, "accent-600": _misturar(ACENTO, "#000000", .20),
    "accent-700": _misturar(ACENTO, "#000000", .40), "accent-900": _misturar(ACENTO, "#000000", .76),
    "dark-50": "#F9FAFB", "dark-100": "#F3F4F6", "dark-200": "#E5E7EB",
    "dark-400": "#9CA3AF", "dark-500": "#6B7280", "dark-600": "#4B5563",
    "dark-800": "#1F2937", "dark-900": "#0F1419",
}
E = ESPELHO
_MORNO_BG_ESCURO = _misturar(ACENTO, "#000000", .82)


def _familia(nome):
    return nome.replace(" ", "+")


_familias = [f"family={_familia(TITULO)}:wght@400;500;600;700;800"]
if TEXTO != TITULO:
    _familias.append(f"family={_familia(TEXTO)}:wght@300;400;500;600;700")
else:
    _familias[0] = f"family={_familia(TITULO)}:wght@300;400;500;600;700;800"
_familias.append("family=IBM+Plex+Mono:wght@400;500;600")

FONTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
          + "&".join(_familias) + '&display=swap">')

_CLARO = f"""
  --ground:{E['dark-50']}; --surface:#FFFFFF; --surface-2:{E['dark-100']};
  --ink:{E['dark-900']}; --ink-2:{E['dark-600']}; --ink-3:{E['dark-500']};
  --rule:{E['dark-200']}; --rule-2:{E['dark-100']};
  --accent:{E['accent-600']}; --accent-2:{E['accent-500']}; --accent-soft:{E['accent-100']};
  --quente:{E['accent-600']}; --quente-bg:{E['accent-100']};
  --morno:{E['accent-700']};  --morno-bg:{E['accent-200']};
  --frio:{E['dark-600']};   --frio-bg:{E['dark-200']};
  --good:#1F7A4C;   --good-soft:#E7F3EC;
  --shadow:0 1px 2px rgba(15,20,25,.05), 0 10px 15px -3px rgba(15,20,25,.10);
"""
_ESCURO = f"""
  --ground:#000000; --surface:{E['dark-900']}; --surface-2:#0A0D11;
  --ink:#FFFFFF; --ink-2:#A0A0A0; --ink-3:{E['dark-500']};
  --rule:{E['dark-800']}; --rule-2:#151B23;
  --accent:{E['accent-400']}; --accent-2:{E['accent-500']}; --accent-soft:{E['accent-900']};
  --quente:{E['accent-400']}; --quente-bg:{E['accent-900']};
  --morno:{E['accent-500']};  --morno-bg:{_MORNO_BG_ESCURO};
  --frio:{E['dark-400']};   --frio-bg:#151B23;
  --good:#5CC08C;   --good-soft:#0E1F17;
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 8px 32px 0 {rgba(ACENTO, .10)};
"""
_BASE, _OUTRO = (_ESCURO, _CLARO) if TEMA_PADRAO == "dark" else (_CLARO, _ESCURO)
_OUTRO_TEMA = "light" if TEMA_PADRAO == "dark" else "dark"


def _css_fonte(nome):
    return '"' + nome.replace('"', "") + '"'


# `fundo_padrao` é o tema de :root. O outro entra pela preferência do leitor — artefato herda o
# tema de quem lê — ou por `data-theme` fixado na página.
TOKENS = f"""
:root{{{_BASE}
  --radius:.5rem; --radius-sm:.25rem;
  --fonte-titulo:{_css_fonte(TITULO)},system-ui,sans-serif;
  --fonte-texto:{_css_fonte(TEXTO)},system-ui,-apple-system,sans-serif;
}}
@media (prefers-color-scheme:{_OUTRO_TEMA}){{ :root:not([data-theme="{TEMA_PADRAO}"]){{{_OUTRO}}}}}
:root[data-theme="{_OUTRO_TEMA}"]{{{_OUTRO}}}
:root[data-theme="{TEMA_PADRAO}"]{{{_BASE}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font:400 15px/1.6 var(--fonte-texto);-webkit-font-smoothing:antialiased}}
h1,h2,h3,h4{{font-family:var(--fonte-titulo)}}
::selection{{background:{rgba(ACENTO, .3)};color:var(--accent)}}
a{{color:var(--accent)}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
"""
