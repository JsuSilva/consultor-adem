#!/usr/bin/env python3
"""
Servidor estático local — igual ao http.server, mas declarando UTF-8.

    python3 scripts/servidor.py [porta]

Dois consertos sobre o http.server padrão:
  1. charset — ele manda "text/html" sem charset e o navegador cai no latin-1, quebrando os acentos.
  2. concorrência — ele é single-thread, e o navegador segura a conexão aberta: uma requisição
     trava as seguintes, e a página carrega sem CSS nem fonte. Aqui roda com threads.
Escuta só em 127.0.0.1 — a raiz servida inclui dados/, que tem dado de cliente.
Grava também as edições dos roteiros: POST /api/roteiros troca o bloco JSON de
saida/roteiros.html pelo corpo recebido. Só aceita de 127.0.0.1, valida o JSON e
guarda a versão anterior em .bak antes de escrever.
Grava também a cadência de ativos: POST /api/cadencia recebe {"base": sha256, "csv": texto} e troca
dados/cadencia.csv — recusa com 409 se o arquivo mudou desde que a página leu
(base diferente do sha atual), para uma edição nunca apagar outra.
"""
import http.server, sys, os, json, tempfile, shutil, hashlib, threading

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEXTUAIS = ("text/", "application/json", "application/javascript",
            "application/xml", "image/svg+xml")

ROTEIROS = os.path.join(RAIZ, "saida", "roteiros.html")
ABRE = '<script type="application/json" id="dados">'
FECHA = "</script>"
LIMITE = 4 * 1024 * 1024


def gravar_roteiros(corpo):
    """Troca o bloco JSON do roteiros.html. Devolve (status, mensagem)."""
    try:
        dados = json.loads(corpo.decode("utf-8"))
    except Exception as e:
        return 400, f"JSON inválido: {e}"
    if not isinstance(dados, dict) or not isinstance(dados.get("roteiros"), list) \
            or not dados["roteiros"]:
        return 400, "esperado {'roteiros': [...]} não vazio"

    with open(ROTEIROS, encoding="utf-8") as f:
        html = f.read()
    i = html.find(ABRE)
    if i < 0:
        return 500, "bloco de dados não encontrado no roteiros.html"
    j = html.find(FECHA, i)
    if j < 0:
        return 500, "bloco de dados sem fechamento"

    novo = (html[:i + len(ABRE)] + "\n"
            + json.dumps(dados, ensure_ascii=False, indent=1) + "\n"
            + html[j:])
    shutil.copy2(ROTEIROS, ROTEIROS + ".bak")
    modo = os.stat(ROTEIROS).st_mode & 0o777
    d = os.path.dirname(ROTEIROS)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(novo)
        os.chmod(tmp, modo)          # mkstemp cria 0600; mantém a permissão do original
        os.replace(tmp, ROTEIROS)
    except BaseException:
        os.path.exists(tmp) and os.unlink(tmp)
        raise
    return 200, f"{len(dados['roteiros'])} roteiros gravados"

CADENCIA = os.path.join(RAIZ, "dados", "cadencia.csv")
CAB_CADENCIA = ("telefone,nome,segmento,abordagem,entrada,etapa,data_etapa,proxima,data_proxima,"
                "status,id_crm,obs,historico")
TRAVA = threading.Lock()


def gravar_cadencia(corpo):
    """Troca o cadencia.csv inteiro, se ninguém mexeu nele desde a leitura. Devolve (status, json)."""
    try:
        dados = json.loads(corpo.decode("utf-8"))
    except Exception as e:
        return 400, json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False)
    txt, base = dados.get("csv"), dados.get("base", "")
    if not isinstance(txt, str) or not txt.startswith(CAB_CADENCIA + "\n"):
        return 400, json.dumps({"erro": "cabeçalho do CSV inesperado"}, ensure_ascii=False)
    atual = b""
    if os.path.exists(CADENCIA):
        with open(CADENCIA, "rb") as f:
            atual = f.read()
    sha_atual = hashlib.sha256(atual).hexdigest() if atual else ""
    if base != sha_atual:
        return 409, json.dumps({"erro": "o arquivo mudou desde que a página carregou — recarregue",
                                "sha": sha_atual}, ensure_ascii=False)
    novo = txt.encode("utf-8")
    d = os.path.dirname(CADENCIA)
    os.makedirs(d, exist_ok=True)
    if atual:
        shutil.copy2(CADENCIA, CADENCIA + ".bak")
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(novo)
        os.chmod(tmp, 0o644)
        os.replace(tmp, CADENCIA)
    except BaseException:
        os.path.exists(tmp) and os.unlink(tmp)
        raise
    return 200, json.dumps({"ok": True, "sha": hashlib.sha256(novo).hexdigest(),
                            "leads": txt.count("\n") - 1}, ensure_ascii=False)

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".md": "text/plain", ".csv": "text/plain", ".jsonl": "text/plain"}

    def guess_type(self, path):
        t = super().guess_type(path)
        base = t.split(";")[0].strip() if t else ""
        if any(base.startswith(p) for p in TEXTUAIS) and "charset=" not in (t or ""):
            return f"{base}; charset=utf-8"
        return t

    def do_POST(self):
        rota = self.path.split("?")[0]
        rotas = {"/api/roteiros": (gravar_roteiros, "text/plain"),
                 "/api/cadencia": (gravar_cadencia, "application/json")}
        if rota not in rotas:
            self.send_error(404, "rota inexistente")
            return
        if self.client_address[0] not in ("127.0.0.1", "::1"):
            self.send_error(403, "só de localhost")
            return
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        if not 0 < n <= LIMITE:
            self.send_error(413, "corpo vazio ou grande demais")
            return
        fn, tipo = rotas[rota]
        try:
            with TRAVA:
                status, msg = fn(self.rfile.read(n))
        except Exception as e:
            status, msg = 500, f"erro ao gravar: {e}"
        corpo = msg.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)
        sys.stderr.write(f"  {status}  POST {rota} — {msg[:120]}\n")

    def log_message(self, fmt, *args):
        if "404" in (fmt % args):
            sys.stderr.write("  404  %s\n" % (args[0] if args else ""))

def main():
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 9797
    os.chdir(RAIZ)
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    http.server.ThreadingHTTPServer.daemon_threads = True
    with http.server.ThreadingHTTPServer(("127.0.0.1", porta), Handler) as s:
        print(f"  →  http://localhost:{porta}/saida/")
        print("     (ctrl+c para parar)\n")
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("\n  parado.")

if __name__ == "__main__":
    main()
