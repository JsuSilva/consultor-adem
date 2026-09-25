"""
Credenciais do Google Ads — onde ficam, como nascem e como viram cliente da API.

Onde ficam
    ~/.config/consultor-adem/google-ads.yaml, permissão 600, pasta 700. NUNCA no repositório nem
    em config/consultor.json (lá só vão IDs: customer_id, projeto_cloud, conversao_principal).

Como nascem — `gads.py autenticar`
    1. O consultor cria, no projeto do Google Cloud dele, um cliente OAuth do tipo "Desktop app"
       e baixa o JSON (client_secret_....json). Guarde FORA do repositório.
    2. Este módulo abre o navegador, o consultor entra com a conta Google que acessa o Google Ads
       e autoriza o escopo https://www.googleapis.com/auth/adwords.
    3. O refresh token volta para uma porta local e é gravado no YAML, junto com client_id e
       client_secret.

developer_token — por que é OPCIONAL aqui
    O Google desativou o developer token em 09/09/2026: o nível de acesso à API passou a vir do
    projeto do Google Cloud (pedido no Cloud Console, página "Google Ads API Overview" →
    "Apply for access"), sem conta de administrador (MCC).
    Fontes: developers.google.com/google-ads/api/docs/api-policy/developer-token e
    .../api-policy/access-levels (consultadas em 24/09/2026).
    Só que a documentação ainda está incoerente: páginas antigas, o modelo de google-ads.yaml e o
    README do MCP oficial continuam pedindo `developer_token`. A biblioteca `google-ads` 33.0.0
    trata o campo como opcional. Por isso: sem token, o arquivo sai sem o campo; se o consultor
    tiver um (ou a API recusar a chamada pedindo um), `autenticar --developer-token` o grava.

login_customer_id
    Só existe para quem opera por uma conta de administrador (MCC). Operar a própria conta não
    exige MCC, então o campo fica fora — mas é aceito com `autenticar --login-customer-id`.
"""
import json
import os
import stat
import sys

ESCOPO = "https://www.googleapis.com/auth/adwords"
VERSAO_API = "v25"
PASTA = os.path.join(os.path.expanduser("~"), ".config", "consultor-adem")
ARQUIVO = os.path.join(PASTA, "google-ads.yaml")
RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTALAR = "pip install -r scripts/google-ads/requirements.txt"


def _parar(msg):
    sys.exit(f"ERRO: {msg}")


def so_digitos(cid, campo):
    """'123-456-7890' → '1234567890'. Para com aviso se não tiver 10 dígitos."""
    d = "".join(c for c in str(cid) if c.isdigit())
    if len(d) != 10:
        _parar(f"`{campo}` deve ter 10 dígitos (ex.: 123-456-7890); veio {cid!r}.")
    return d


def _dentro_do_repo(caminho):
    alvo = os.path.realpath(caminho)
    return alvo == RAIZ_REPO or alvo.startswith(RAIZ_REPO + os.sep)


def _ler_client_secret(caminho):
    if not os.path.isfile(caminho):
        _parar(f"arquivo do cliente OAuth não encontrado: {caminho}")
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    if "installed" not in dados:
        tipo = ", ".join(dados.keys()) or "vazio"
        _parar(f"o JSON não é de um cliente OAuth \"Desktop app\" (chave encontrada: {tipo}).\n"
               "No Google Cloud: APIs e serviços → Credenciais → Criar credenciais → "
               "ID do cliente OAuth → Tipo: App para computador.")
    inst = dados["installed"]
    if not inst.get("client_id") or not inst.get("client_secret"):
        _parar("o JSON não traz client_id e client_secret.")
    return inst["client_id"], inst["client_secret"]


def _yaml_escalar(v):
    # Aspas simples em YAML: só o apóstrofo precisa ser dobrado.
    return "'" + str(v).replace("'", "''") + "'"


def _gravar(campos):
    os.makedirs(PASTA, mode=0o700, exist_ok=True)
    os.chmod(PASTA, 0o700)
    linhas = ["# Credenciais do Google Ads do consultor — NUNCA copiar para o repositório.",
              "# Gerado por scripts/google-ads/gads.py autenticar."]
    for k, v in campos.items():
        if v is None:
            continue
        linhas.append(f"{k}: {'True' if v is True else _yaml_escalar(v)}")
    conteudo = "\n".join(linhas) + "\n"
    fd = os.open(ARQUIVO, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(conteudo)
    os.chmod(ARQUIVO, 0o600)


def autenticar(client_secret, developer_token=None, login_customer_id=None):
    """Fluxo OAuth Desktop app → refresh token → ~/.config/consultor-adem/google-ads.yaml."""
    if _dentro_do_repo(client_secret):
        print("AVISO: o JSON do cliente OAuth está dentro do repositório. Mova-o para fora "
              "(ex.: ~/.config/consultor-adem/) — o .gitignore não cobre client_secret_*.json.")
    client_id, secret = _ler_client_secret(client_secret)
    if login_customer_id:
        login_customer_id = so_digitos(login_customer_id, "--login-customer-id")

    if os.path.exists(ARQUIVO):
        resp = input(f"Já existe {ARQUIVO}. Sobrescrever? Digite 'sim': ").strip().lower()
        if resp != "sim":
            sys.exit("Nada foi alterado.")

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        _parar(f"biblioteca ausente. Instale com: {INSTALAR}")

    flow = InstalledAppFlow.from_client_secrets_file(client_secret, scopes=[ESCOPO])
    print("Abrindo o navegador para você autorizar o acesso ao Google Ads...")
    cred = flow.run_local_server(port=0, prompt="consent", access_type="offline")
    if not cred.refresh_token:
        _parar("o Google não devolveu refresh token. Revogue o acesso do app em "
               "myaccount.google.com/permissions e rode `autenticar` de novo.")

    _gravar({
        "client_id": client_id,
        "client_secret": secret,
        "refresh_token": cred.refresh_token,
        "developer_token": developer_token,
        "login_customer_id": login_customer_id,
        "use_proto_plus": True,
    })
    print(f"OK: credenciais gravadas em {ARQUIVO} (permissão 600).")
    if not developer_token:
        print("Sem developer_token (desativado pelo Google em 09/09/2026). Se a API recusar "
              "pedindo o campo, rode de novo com --developer-token.")


def cliente():
    """GoogleAdsClient a partir do YAML. Para com aviso limpo se faltar arquivo ou biblioteca."""
    if not os.path.exists(ARQUIVO):
        _parar(f"credenciais não encontradas em {ARQUIVO}.\n"
               "Rode antes: python3 scripts/google-ads/gads.py autenticar --client-secret <json>")
    modo = stat.S_IMODE(os.stat(ARQUIVO).st_mode)
    if modo & 0o077:
        print(f"AVISO: {ARQUIVO} está com permissão {oct(modo)}; o certo é 600 "
              f"(chmod 600 {ARQUIVO}).")
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        _parar(f"biblioteca `google-ads` ausente. Instale com: {INSTALAR}")
    return GoogleAdsClient.load_from_storage(path=ARQUIVO, version=VERSAO_API)
