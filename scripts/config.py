"""
Carrega a configuração do consultor — o único ponto em que os scripts leem dado pessoal
ou número da administradora.

    from config import carregar, exigir
    cfg = carregar()
    nome = exigir(cfg, "consultor.nome")

Lê config/consultor.json (fora do Git). Sem ele, cai no modelo config/consultor.exemplo.json,
em que tudo é null — e `exigir` para com aviso em vez de inventar.

Quem preenche o arquivo é a skill `configuracao`.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RAIZ, "config", "consultor.json")
EXEMPLO = os.path.join(RAIZ, "config", "consultor.exemplo.json")


def carregar():
    caminho = CONFIG if os.path.exists(CONFIG) else EXEMPLO
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def valor(cfg, chave, padrao=None):
    """Lê `a.b.c`. Devolve `padrao` quando o caminho não existe ou está null."""
    atual = cfg
    for parte in chave.split("."):
        if not isinstance(atual, dict) or atual.get(parte) is None:
            return padrao
        atual = atual[parte]
    return atual


def exigir(cfg, chave):
    """Como `valor`, mas para o script quando o campo não foi preenchido."""
    v = valor(cfg, chave)
    if v is None:
        sys.exit(f"ERRO: `{chave}` não preenchido em config/consultor.json.\n"
                 f"Rode a skill `configuracao` (ou preencha o campo) antes de gerar esta peça.")
    return v
