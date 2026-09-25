#!/usr/bin/env python3
"""Monta e renderiza um card: preenche a identidade do consultor, embute as fotos do molde e tira
o PNG no Chrome headless.

    python3 .agents/skills/reproduzir-card/montar-card.py molde.tpl.html saida/cards/NN-card-slug [1080x1350]

Grava <destino>.html (autocontido) e <destino>.png no dobro do quadro (2160×2700 no padrão).

No molde há três tipos de marcação:
- `{{chave.da.config}}` — lida de config/consultor.json via scripts/config.py (`consultor.*`,
  `identidade_visual.*`). Campo vazio para o script com aviso, nunca é inventado — exceto cores e
  fontes (abaixo).
- `{{card.*}}` e `{{cor.*}}` — derivados da config aqui mesmo (nome em caixa alta, iniciais ou
  logo, cargo, site, fontes para o Google Fonts, tons do acento). Ver `identidade.md`.
- `[[descrição]]` — valor do card (grupo, crédito, parcela, foto), preenchido na cópia do molde
  antes de renderizar. Sobrou um, o script para.

Cores e fontes de `identidade_visual` vazias caem no tema neutro de scripts/design.py (os mesmos
valores, importados de lá), com aviso de que o card saiu no neutro.

Cada foto entra como __FOTO:caminho__, e o caminho aceita ~.
"""
import base64, pathlib, re, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "scripts"))
from config import carregar, exigir, valor  # noqa: E402
import design  # noqa: E402  — tema neutro e resolução das cores e fontes da config

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TIPOS = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".svg": "image/svg+xml"}

# Tons derivados do acento. Fator < 1 escurece a cor em direção ao preto; os de `_claro` clareiam
# o acento de brilho em direção ao branco. São a mesma escala dos moldes de origem, agora em
# função da cor do consultor.
ESCALA = {
    "acento_medio": 0.93, "acento_escuro": 0.80, "acento_profundo": 0.62, "acento_faixa": 0.47,
    "acento_sombra": 0.33, "acento_noite": 0.19, "acento_breu": 0.12,
}
CLARO = 0.41


def rgb(hexa, chave):
    h = hexa.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        sys.exit(f"ERRO: `{chave}` precisa ser uma cor #RRGGBB em config/consultor.json (veio {hexa!r}).")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexa(c):
    return "#" + "".join(f"{max(0, min(255, round(v))):02X}" for v in c)


def avisar_neutro(cfg):
    """Cores e fontes vazias na config: o card sai no neutro de scripts/design.py, com aviso."""
    vazios = [c for c in ("acento", "acento_brilho", "fonte_titulo", "fonte_texto")
              if not valor(cfg, f"identidade_visual.{c}")]
    if not vazios:
        return
    linhas = []
    for c in vazios:
        if c == "acento_brilho" and valor(cfg, "identidade_visual.acento"):
            linhas.append(f"  - identidade_visual.{c}: derivado do acento ({design.BRILHO})")
        else:
            linhas.append(f"  - identidade_visual.{c}: neutro ({design.NEUTRO[c]})")
    print("AVISO: identidade visual incompleta em config/consultor.json — o card usa o tema neutro"
          " de scripts/design.py nestes campos:\n" + "\n".join(linhas), file=sys.stderr)


def paleta():
    a = rgb(design.ACENTO, "identidade_visual.acento")
    b = rgb(design.BRILHO, "identidade_visual.acento_brilho")
    tons = {"acento": a, "acento_brilho": b,
            "acento_claro": tuple(v + (255 - v) * CLARO for v in b)}
    for nome, f in ESCALA.items():
        tons[nome] = tuple(v * f for v in a)
    cores = {}
    for nome, c in tons.items():
        cores[nome] = hexa(c)
        cores[nome + "_rgb"] = ",".join(str(max(0, min(255, round(v)))) for v in c)
    return cores


def derivado(cfg, chave):
    """Os `{{card.*}}`: cada um só exige o campo da config de que depende."""
    if chave == "nome_caixa_alta":
        return exigir(cfg, "consultor.nome").upper()
    if chave == "iniciais":
        partes = exigir(cfg, "consultor.nome").split()
        return (partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")).upper()
    if chave == "monograma":
        return monograma(cfg)
    if chave == "cargo_caixa_alta":
        return exigir(cfg, "consultor.cargo").upper()
    site = lambda: re.sub(r"^(https?://)?", "", exigir(cfg, "consultor.site")).rstrip("/")
    if chave == "site_caixa_alta":
        return site().upper()
    if chave == "site_nome_caixa_alta":
        return re.sub(r"^www\.", "", site(), flags=re.I).split(".", 1)[0].upper()
    if chave == "site_sufixo":
        resto = re.sub(r"^www\.", "", site(), flags=re.I).split(".", 1)
        return "." + resto[1] if len(resto) > 1 else ""
    if chave == "fonte_titulo_url":
        return design.TITULO.replace(" ", "+")
    if chave == "fonte_texto_url":
        return design.TEXTO.replace(" ", "+")
    sys.exit(f"ERRO: marcação desconhecida no molde: {{{{card.{chave}}}}}")


def monograma(cfg):
    """Com `identidade_visual.logo` (caminho de arquivo), o logo embutido na altura da letra do
    monograma; sem logo, as iniciais."""
    logo = valor(cfg, "identidade_visual.logo")
    if isinstance(logo, str) and logo.strip():
        return (f'<img src="{embutir_arquivo(logo.strip(), "logo")}" alt="" '
                'style="height:1em;width:auto;max-width:1.5em;object-fit:contain;display:block;margin:0 auto">')
    return derivado(cfg, "iniciais")


def preencher(texto, cfg):
    cores = {}

    def troca(m):
        chave = m.group(1)
        if chave.startswith("cor."):
            if not cores:
                cores.update(paleta())
            nome = chave[4:]
            if nome not in cores:
                sys.exit(f"ERRO: tom desconhecido no molde: {{{{{chave}}}}}")
            return cores[nome]
        if chave.startswith("card."):
            return derivado(cfg, chave[5:])
        if chave == "identidade_visual.fonte_titulo":
            return design.TITULO
        if chave == "identidade_visual.fonte_texto":
            return design.TEXTO
        return str(exigir(cfg, chave))

    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", troca, texto)


def embutir_arquivo(caminho, o_que="foto"):
    arq = pathlib.Path(caminho).expanduser()
    if not arq.is_absolute():
        arq = RAIZ / arq
    if not arq.exists():
        sys.exit(f"ERRO: {o_que} não encontrado(a): {arq}")
    tipo = TIPOS.get(arq.suffix.lower())
    if not tipo:
        sys.exit(f"ERRO: {o_que} em formato não suportado ({arq.suffix}); use " + ", ".join(TIPOS))
    return f"data:{tipo};base64," + base64.b64encode(arq.read_bytes()).decode()


def embutir(m):
    return embutir_arquivo(m.group(1))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    molde, destino = pathlib.Path(sys.argv[1]).expanduser(), pathlib.Path(sys.argv[2]).expanduser()
    largura, altura = sys.argv[3].split("x") if len(sys.argv) > 3 else ("1080", "1350")

    cfg = carregar()
    avisar_neutro(cfg)
    texto = molde.read_text()
    faltam = sorted(set(re.findall(r"\[\[(.+?)\]\]", texto)))
    if faltam:
        sys.exit("ERRO: o molde ainda tem valores do card por preencher:\n  - " + "\n  - ".join(faltam))

    texto = preencher(texto, cfg)
    destino.parent.mkdir(parents=True, exist_ok=True)
    html = destino.with_suffix(".html")
    png = destino.with_suffix(".png")
    html.write_text(re.sub(r"__FOTO:(.+?)__", embutir, texto))
    png.unlink(missing_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={largura},{altura}",
                    "--virtual-time-budget=10000", f"--screenshot={png}", html.as_uri()],
                   capture_output=True)
    if not png.exists():
        sys.exit("Chrome não gerou o PNG")
    print(html)
    print(png)


if __name__ == "__main__":
    main()
