#!/usr/bin/env python3
"""Monta e renderiza um card: preenche a identidade do consultor, embute as fotos do molde e tira
o PNG no Chrome headless.

    python3 skills/reproduzir-card/montar-card.py molde.tpl.html saida/cards/NN-card-slug [1080x1350]

Grava <destino>.html (autocontido) e <destino>.png no dobro do quadro (2160×2700 no padrão).

No molde há três tipos de marcação:
- `{{chave.da.config}}` — lida de config/consultor.json via scripts/config.py (`consultor.*`,
  `identidade_visual.*`). Campo vazio para o script com aviso, nunca é inventado.
- `{{card.*}}` e `{{cor.*}}` — derivados da config aqui mesmo (nome em caixa alta, iniciais,
  site, fontes para o Google Fonts, tons do acento). Ver `identidade.md`.
- `[[descrição]]` — valor do card (grupo, crédito, parcela, foto), preenchido na cópia do molde
  antes de renderizar. Sobrou um, o script para.

Cada foto entra como __FOTO:caminho__, e o caminho aceita ~.
"""
import base64, pathlib, re, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from config import carregar, exigir  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TIPOS = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}

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


def paleta(cfg):
    a = rgb(exigir(cfg, "identidade_visual.acento"), "identidade_visual.acento")
    b = rgb(exigir(cfg, "identidade_visual.acento_brilho"), "identidade_visual.acento_brilho")
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
    if chave == "assinatura_caixa_alta":
        return exigir(cfg, "consultor.assinatura").upper()
    site = lambda: re.sub(r"^(https?://)?", "", exigir(cfg, "consultor.site")).rstrip("/")
    if chave == "site_caixa_alta":
        return site().upper()
    if chave == "site_nome_caixa_alta":
        return re.sub(r"^www\.", "", site(), flags=re.I).split(".", 1)[0].upper()
    if chave == "site_sufixo":
        resto = re.sub(r"^www\.", "", site(), flags=re.I).split(".", 1)
        return "." + resto[1] if len(resto) > 1 else ""
    if chave == "fonte_titulo_url":
        return exigir(cfg, "identidade_visual.fonte_titulo").replace(" ", "+")
    if chave == "fonte_texto_url":
        return exigir(cfg, "identidade_visual.fonte_texto").replace(" ", "+")
    sys.exit(f"ERRO: marcação desconhecida no molde: {{{{card.{chave}}}}}")


def preencher(texto, cfg):
    cores = {}

    def troca(m):
        chave = m.group(1)
        if chave.startswith("cor."):
            if not cores:
                cores.update(paleta(cfg))
            nome = chave[4:]
            if nome not in cores:
                sys.exit(f"ERRO: tom desconhecido no molde: {{{{{chave}}}}}")
            return cores[nome]
        if chave.startswith("card."):
            return derivado(cfg, chave[5:])
        return str(exigir(cfg, chave))

    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", troca, texto)


def embutir(m):
    foto = pathlib.Path(m.group(1)).expanduser()
    if not foto.is_absolute():
        foto = RAIZ / foto
    if not foto.exists():
        sys.exit(f"ERRO: foto não encontrada: {foto}")
    tipo = TIPOS[foto.suffix.lower()]
    return f"data:{tipo};base64," + base64.b64encode(foto.read_bytes()).decode()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    molde, destino = pathlib.Path(sys.argv[1]).expanduser(), pathlib.Path(sys.argv[2]).expanduser()
    largura, altura = sys.argv[3].split("x") if len(sys.argv) > 3 else ("1080", "1350")

    texto = molde.read_text()
    faltam = sorted(set(re.findall(r"\[\[(.+?)\]\]", texto)))
    if faltam:
        sys.exit("ERRO: o molde ainda tem valores do card por preencher:\n  - " + "\n  - ".join(faltam))

    texto = preencher(texto, carregar())
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
