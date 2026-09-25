# scripts/google-ads/

Integração própria de escrita com o Google Ads, pela biblioteca oficial `google-ads` (33.0.0,
API v25). O MCP oficial do Google só lê; criar campanha, conversão, ativar e mudar orçamento passam
por aqui. Guia do zero, acesso e travas: [`skills/anuncios-google/SKILL.md`](../../skills/anuncios-google/SKILL.md).

## Instalar

Única pasta de `scripts/` com dependência. Instale num ambiente virtual **fora do repositório**
(o `.gitignore` não cobre `.venv/`), com Python 3.9–3.14:

```bash
pip install -r scripts/google-ads/requirements.txt
```

## Subcomandos

Da raiz do repositório: `python3 scripts/google-ads/gads.py <subcomando> --help`.

| Subcomando | Natureza | O que faz |
|---|---|---|
| `autenticar --client-secret <json>` | credencial | OAuth "Desktop app" → refresh token em `~/.config/consultor-adem/google-ads.yaml` (600). `--developer-token` e `--login-customer-id` opcionais |
| `contas` | leitura | contas acessíveis; marca a da config |
| `relatorio [--periodo 7d \| --de AAAA-MM-DD --ate AAAA-MM-DD]` | leitura | desempenho por campanha: impressões, cliques, CTR, CPC, custo, conversões |
| `criar-campanha <json> [--aplicar]` | escrita, sem gasto | Pesquisa, **sempre PAUSADA**; padrão é simular (`validate_only`) |
| `criar-conversao --nome --tipo formulario\|whatsapp\|site [--aplicar] [--gravar-principal]` | escrita, sem gasto | ação de conversão de site; `--gravar-principal` grava o id na config, só a pedido do consultor |
| `ativar --campanha-id` | **gasto** | pausada → ativa |
| `orcamento --campanha-id --novo-brl` | **gasto** | muda o orçamento diário |

## Travas

1. `customer_id` vem de `anuncios.google.customer_id`; sem ele, tudo para (menos `autenticar` e
   `contas`). Sem MCC: `login_customer_id` só entra se o consultor passar em `autenticar`.
2. Orçamento nunca passa de `anuncios.teto_diario_brl`. Sem teto na config, `criar-campanha`,
   `ativar` e `orcamento` recusam. Conta fora de BRL é recusada.
3. `ativar` e `orcamento` mostram teto, orçamento atual e novo, e exigem o **nome exato da
   campanha digitado num terminal interativo** — entrada por pipe é recusada. Quem roda é o
   consultor, no terminal dele.
4. Credenciais nunca no repositório nem em `config/consultor.json`.

## Arquivo da campanha (`dados/campanha-<nome>.json`)

```json
{
  "nome": "Pesquisa — consórcio de imóvel",
  "orcamento_diario_brl": 20,
  "estrategia_lance": "cpc_manual",
  "cpc_max_brl": 2.5,
  "geo_ids": [2076],
  "idioma_ids": [1014],
  "parceiros_de_pesquisa": false,
  "grupo_nome": "Imóvel",
  "palavras_chave": [
    {"texto": "consórcio de imóvel", "correspondencia": "frase"},
    {"texto": "consórcio imobiliário", "correspondencia": "exata"}
  ],
  "anuncio": {
    "url_final": "https://seusite.com.br/imovel",
    "titulos": ["Título 1 (até 30)", "Título 2", "Título 3"],
    "descricoes": ["Descrição 1 (até 90 caracteres).", "Descrição 2."],
    "caminho1": "imovel",
    "caminho2": ""
  }
}
```

- `estrategia_lance`: `cpc_manual` (exige `cpc_max_brl`) ou `maximizar_conversoes`.
- `geo_ids` e `idioma_ids` são obrigatórios — sem eles a campanha miraria qualquer lugar e idioma.
  ⚠️ `2076` (Brasil) e `1014` (português) acima são ilustrativos: confira os IDs nas tabelas de
  segmentação geográfica e de idiomas da documentação da API antes de usar; cidade/estado têm ID
  próprio.
- Limites checados antes de chamar a API: 3–15 títulos (≤ 30 caracteres), 2–4 descrições (≤ 90),
  caminhos ≤ 15, palavra-chave ≤ 80 caracteres e 10 palavras.
- Rede de Display sempre desligada; parceiros de pesquisa só se `true`.
- Os textos passam pela régua de
  `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md` **antes** do arquivo
  existir — o script não julga discurso.

## Arquivos

`gads.py` (CLI) · `auth.py` (OAuth e credenciais; o docstring explica o `developer_token`) ·
`operacoes.py` (chamadas à API) · `travas.py` (teto, moeda, confirmação) · `requirements.txt`.
