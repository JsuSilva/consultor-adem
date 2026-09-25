#!/usr/bin/env python3
"""
Verifica quais domínios de uma lista respondem como site, para virarem link na lista.

    python3 scripts/verificar-sites.py --lista dados/dominios.csv [--forcar]

Entrada: CSV do consultor em dados/ (fora do Git), com a coluna `dominio` — um domínio
corporativo por linha, sem `https://` (ex.: `escritorioexemplo.com.br`). Linha com `@` (e-mail,
free-mail) é ignorada.

Faz um HEAD/GET curto por domínio — não baixa conteúdo, não raspa nada.
Resultado em dados/sites-cache.json, reaproveitado entre execuções.
"""
import argparse, csv, json, os, ssl, socket, sys
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RAIZ, "dados", "sites-cache.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

def testa(dom):
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    for url in (f"https://{dom}", f"https://www.{dom}", f"http://{dom}"):
        try:
            r = Request(url, method="GET", headers={"User-Agent": UA, "Accept": "text/html"})
            with urlopen(r, timeout=6, context=ctx) as resp:
                if 200 <= resp.status < 400:
                    return {"ok": True, "url": resp.geturl(), "status": resp.status}
        except HTTPError as e:
            if e.code in (401, 403, 405):        # existe, só não deixa entrar assim
                return {"ok": True, "url": url, "status": e.code}
        except (URLError, socket.timeout, ssl.SSLError, socket.gaierror, OSError, ValueError):
            continue
    return {"ok": False}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", default=os.path.join(RAIZ, "dados", "dominios.csv"),
                    help="CSV com a coluna `dominio` (padrão: dados/dominios.csv)")
    ap.add_argument("--forcar", action="store_true"); a = ap.parse_args()
    if not os.path.exists(a.lista):
        sys.exit(f"ERRO: lista não encontrada: {a.lista}\n"
                 "Monte um CSV em dados/ com a coluna `dominio` e passe com --lista.")
    cache = {} if a.forcar or not os.path.exists(CACHE) else json.load(open(CACHE))

    with open(a.lista, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        if "dominio" not in (leitor.fieldnames or []):
            sys.exit("ERRO: a lista não tem a coluna `dominio`.")
        doms = sorted({(r["dominio"] or "").strip().lower() for r in leitor
                       if (r["dominio"] or "").strip() and "@" not in r["dominio"]})
    if not doms:
        sys.exit("ERRO: nenhum domínio na lista.")
    faltam = [d for d in doms if d not in cache]
    print(f"{len(doms)} domínios corporativos · {len(faltam)} a verificar "
          f"({len(doms)-len(faltam)} já em cache)")
    if faltam:
        with ThreadPoolExecutor(max_workers=12) as ex:
            for d, res in zip(faltam, ex.map(testa, faltam)):
                cache[d] = res
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(cache, open(CACHE, "w"), indent=1)
    viv = sum(1 for d in doms if cache.get(d, {}).get("ok"))
    print(f"  respondem: {viv} ({viv/len(doms)*100:.0f}%) · mortos ou sem site: {len(doms)-viv}")
    print(f"→ {os.path.relpath(CACHE, RAIZ)}")

if __name__ == "__main__":
    main()
