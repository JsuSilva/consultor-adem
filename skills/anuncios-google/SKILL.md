---
name: anuncios-google
description: Configura do zero e opera anúncios no Google Ads — conta em modo especialista, faturamento no Brasil, verificação do anunciante e de serviços financeiros, tag do Google e conversões; conecta o agente pela integração própria (scripts/google-ads/gads.py, leitura e escrita) e pelo MCP oficial (só leitura); e opera campanhas com travas de verba (teto diário da config e confirmação por rodada). Invoque com /anuncios-google quando o consultor quiser montar a conta, conectar o agente, ler resultados ou subir campanha; não dispara sozinha, porque gasta dinheiro e publica peça.
---

# Skill — `anuncios-google`

> Três partes: **(a)** a conta do Google Ads configurada do zero, **(b)** o acesso do agente e
> **(c)** a operação com travas. Fatos verificados em **2026-09-24**; o que está marcado
> **INCERTO** não tem fonte oficial conclusiva e deve ser dito assim ao consultor.
> IDs vão em `config/consultor.json` → `anuncios.google.*` (fora do Git). **Credenciais nunca ali:**
> client secret e refresh token ficam em `~/.config/consultor-adem/google-ads.yaml` (permissão 600).
> A ferramenta de escrita é `scripts/google-ads/gads.py` — detalhes em `scripts/google-ads/README.md`.

## Regras

1. **Nada que gasta verba sem o "sim" do consultor naquela rodada.** Ativar campanha e mudar
   orçamento pedem, cada um, o seu "sim". "Sim" de rodada anterior, de outra campanha ou deste
   documento não vale.
2. **Teto diário é trava dura.** `anuncios.teto_diario_brl` vazio = nada com orçamento roda
   (`gads.py` recusa). Orçamento acima do teto = recusa; o agente não sobe o teto, só o consultor,
   editando a configuração.
3. **Toda peça passa pela régua** de `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`
   antes de virar arquivo de campanha: consórcio não é investimento, nenhuma promessa de
   contemplação, data ou chance.
4. **Não decide pelo consultor** (Regra nº 1 do `AGENTS.md`): palavra-chave, local, lance, verba,
   peça, conversão principal e categoria na verificação financeira são dele. A skill apresenta
   opções e espera.
5. **Credencial nunca em arquivo versionado** — nem o JSON do cliente OAuth (o `.gitignore` não
   cobre `client_secret_*.json`; guardar em `~/.config/consultor-adem/`).
6. **Uma escrita por vez e conferida:** simular antes (`gads.py` simula por padrão), aplicar com
   aval, ler de volta (`relatorio` ou a consulta do MCP) e mostrar o estado real.

---

## Parte (a) — Configuração da conta, do zero

O consultor faz estes passos **na própria mão**, logado na conta Google dele; o agente orienta e
não cria conta, não faz login, não aceita termo, não cadastra pagamento. Os passos são o
procedimento geral; havendo diferença na tela, **vale o link** da ajuda oficial.

1. **Criar a conta do Google Ads SEM campanha inteligente (modo especialista).** Em
   ads.google.com, o fluxo de criação empurra uma campanha inteligente; procurar a opção de mudar
   para o **modo especialista** e, nele, **criar a conta sem campanha**. Campanha inteligente tira
   do consultor o controle de palavra-chave e lance — e a integração desta skill cria campanha de
   Pesquisa comum.
   Criar conta: https://support.google.com/google-ads/answer/6366720?hl=pt-BR ·
   inteligente × especialista: https://support.google.com/google-ads/answer/9367181?hl=pt-BR
2. **País Brasil, fuso e moeda BRL.** O teto da config é em reais: `gads.py` recusa conta em outra
   moeda. ⚠️ Moeda e fuso em geral não se trocam depois (não conferido nos links) — conferir antes
   de confirmar. Anotar o ID da conta (123-456-7890, canto superior direito) →
   `anuncios.google.customer_id`.
3. **Faturamento no Brasil** — perfil de pagamentos e forma de pagamento. Pessoa física (CPF) ou
   jurídica (CNPJ) é escolha do consultor; atenção ao passo 5: o **nome** que for para a
   verificação financeira tem de bater com o registro no regulador.
   Pagamentos: https://support.google.com/google-ads/answer/2375433?hl=pt-BR ·
   adicionar pagamento: https://support.google.com/google-ads/answer/2375375?hl=pt-BR ·
   perfil de pagamentos: https://support.google.com/google-ads/answer/7268503?hl=pt-BR
4. **Verificação do anunciante** — identidade e documentos, quando o Google pedir.
   https://support.google.com/adspolicy/answer/15577076?hl=pt-br ·
   documentos aceitos no Brasil: https://support.google.com/adspolicy/answer/9872280?co=GENIE.CountryCode%3DBR
5. **Verificação de serviços financeiros — obrigatória no Brasil.**
   https://support.google.com/adspolicy/answer/15332527?hl=pt-BR&co=GENIE.CountryCode%3DBR
   - Pedido feito por **administrador da conta do Google Ads ou do perfil de pagamentos**. O nome
     tem de bater com o registro do regulador. Lista de reguladores:
     https://support.google.com/adspolicy/answer/12390454
   - Três categorias:
     1. **Anunciante autorizado** — prova a autorização do regulador (via G2RS);
     2. **Terceiro aprovado** — agente/revendedor com aprovação de um anunciante autorizado; pede
        direto ao Google;
     3. **Não financeiro** — o único exemplo com "consórcio" na página é o de setor automotivo que
        promove consórcios.
   - **Enquadramento do consultor: INCERTO.** A skill **não assume** categoria nenhuma. Orientar o
     consultor a **confirmar com a administradora, por escrito**, antes de pedir:
     1. em qual categoria o consultor (ou a unidade) deve se verificar;
     2. se a administradora é anunciante autorizada e se concede aprovação a terceiros — e como
        se pede;
     3. em nome de quem (pessoa, unidade, CNPJ) o pedido deve sair, para o nome bater;
     4. que regras a administradora impõe a anúncio que usa a marca dela.
   - A resposta da administradora e a categoria escolhida são registradas pelo consultor; o agente
     não preenche o pedido no lugar dele.
6. **Tag do Google e conversões.** Instalar a tag do Google no site (código no `<head>` ou
   integração da plataforma do site) e criar as ações de conversão — pelo painel ou por
   `gads.py criar-conversao` (Parte c). Qual ação é a **principal** é decisão do consultor; o id só
   vai para `anuncios.google.conversao_principal` se ele pedir (`--gravar-principal`).
   Tag do Google: https://support.google.com/google-ads/answer/7548399?hl=pt-BR ·
   conversões: https://support.google.com/google-ads/answer/15464305?hl=pt-BR ·
   conversões de site: https://support.google.com/google-ads/answer/12216226?hl=pt-BR

---

## Parte (b) — O acesso do agente

Dois caminhos, complementares:

| Caminho | Faz | Credencial | Quando |
|---|---|---|---|
| `scripts/google-ads/gads.py` (integração própria, biblioteca oficial `google-ads` 33.0.0, API v25) | lê **e escreve**: contas, relatório, campanha pausada, conversão, ativar, orçamento | `~/.config/consultor-adem/google-ads.yaml` | toda escrita; relatório em tabela |
| MCP oficial do Google Ads | **só lê**: `list_accessible_customers`, `search` (GAQL), `get_resource_metadata` | conforme o README do MCP | consulta livre de dados pelo agente |

Criar a **conta** de anúncio pela API exige MCC, gasto acima de US$ 1.000 e não é permitido no
nível Explorer — por isso a conta nasce à mão (Parte a). Operar a própria conta **não exige MCC**.

### 1. Projeto no Google Cloud

1. Em console.cloud.google.com, criar um projeto (ou usar um do consultor). Anotar o ID →
   `anuncios.google.projeto_cloud`.
2. Em APIs e serviços → Biblioteca, **habilitar a Google Ads API** no projeto.

### 2. Nível de acesso à API

O **developer token foi desativado em 09/09/2026**: o nível de acesso passou a vir do **projeto do
Google Cloud**, pedido no Cloud Console, página **"Google Ads API Overview" → "Apply for access"**,
sem MCC.
https://developers.google.com/google-ads/api/docs/api-policy/developer-token ·
https://developers.google.com/google-ads/api/docs/api-policy/access-levels (atualizada em 23/09/2026)

| Nível | Contas | Limite | Observação |
|---|---|---|---|
| Test | só contas de teste | 15.000 operações/dia | não serve para a conta real |
| Explorer | produção | 2.880 operações/dia | não cria contas, não gerencia usuários, sem planejamento nem faturamento |
| Basic | produção | 15.000 operações/dia | exige verificação de marca do projeto Cloud |
| Standard | produção | ilimitado | auditoria manual, ~10 dias úteis |

- Upgrade automático de nível é "pode", não garantia.
- **INCERTO:** se pessoa física é elegível ao Basic.
- **INCERTO:** se o Explorer cria campanha e ação de conversão — não está entre as restrições
  listadas, mas a página não diz explicitamente. Testar com `--simular` antes de contar com isso.
- **Documentação incoerente:** páginas antigas, o modelo `google-ads.yaml` e o README do MCP ainda
  pedem `developer_token`. `gads.py` funciona sem ele e aceita um em `autenticar --developer-token`
  se a API recusar a chamada pedindo o campo.

### 3. Cliente OAuth "Desktop app"

1. ⚠️ Procedimento geral, não conferido nas fontes desta skill: em APIs e serviços → Tela de
   consentimento OAuth, configurar o app e incluir o e-mail do consultor como usuário de teste.
   ⚠️ Em app externo com status "em teste", o refresh token pode expirar em poucos dias — se
   `gads.py` começar a acusar erro de autenticação, rodar `autenticar` de novo e revisar o status
   de publicação do app com o consultor.
2. Em APIs e serviços → Credenciais → Criar credenciais → **ID do cliente OAuth → App para
   computador (Desktop app)**. Baixar o JSON e guardar **fora do repositório**, por exemplo em
   `~/.config/consultor-adem/`.
   https://developers.google.com/google-ads/api/docs/client-libs/python/oauth-desktop

### 4. Integração própria — `gads.py autenticar`

1. Instalar a dependência num ambiente virtual fora do repositório (Python 3.9–3.14):
   `pip install -r scripts/google-ads/requirements.txt`.
2. **O consultor roda, no terminal dele** (abre o navegador para o login — o agente não faz login):

   ```bash
   python3 scripts/google-ads/gads.py autenticar --client-secret ~/.config/consultor-adem/client_secret_XXXX.json
   ```

   Escopo pedido: `https://www.googleapis.com/auth/adwords`. Resultado:
   `~/.config/consultor-adem/google-ads.yaml` (600). Sem MCC não se passa `--login-customer-id`
   (https://developers.google.com/google-ads/api/docs/get-started/make-first-call).
3. **Testar (só leitura):** `python3 scripts/google-ads/gads.py contas` → deve listar a conta. Com
   o ID confirmado pelo consultor, preencher `anuncios.google.customer_id`.

### 5. MCP oficial (só leitura) no Claude Code

Doc: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server. Configuração
publicada (exige `pipx` instalado):

```json
{"mcpServers": {"google-ads-mcp": {
  "command": "pipx",
  "args": ["run", "--spec", "git+https://github.com/googleads/google-ads-mcp.git", "google-ads-mcp"],
  "env": {"GOOGLE_PROJECT_ID": "<projeto>"}
}}}
```

Equivalente no Claude Code, no escopo local (fora do Git):

```bash
claude mcp add google-ads-mcp -e GOOGLE_PROJECT_ID=<projeto> -- \
  pipx run --spec git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp
```

- `<projeto>` é o de `anuncios.google.projeto_cloud`.
- Pôr num `.mcp.json` do repositório versiona a configuração: só se o consultor quiser, e nunca
  com credencial dentro.
- ⚠️ A autenticação do MCP segue o README do repositório `googleads/google-ads-mcp` — não
  detalhada aqui; o README ainda pede developer token (incoerente com a desativação).
- Depois, `/mcp` no Claude Code para conferir que o servidor subiu; testar com
  `list_accessible_customers`.

---

## Parte (c) — Operação com travas

### O que é leitura, escrita e gasto

| Risco | MCP oficial | `gads.py` | O que o agente pode fazer |
|---|---|---|---|
| **Leitura** | `list_accessible_customers`, `search`, `get_resource_metadata` | `contas`, `relatorio` | livre, quando o consultor pedir |
| **Escreve, sem gasto** | — | `criar-campanha` (nasce **PAUSADA**), `criar-conversao` — ambos simulam por padrão; `--aplicar` executa | simular livre; `--aplicar` com o aval do consultor ao plano da campanha / à conversão |
| **GASTA / muda verba** | — | `ativar`, `orcamento` | **só pelo protocolo abaixo**; quem digita a confirmação é o consultor |

### Campanha nova

1. Plano da campanha (palavras-chave, correspondência, locais, idioma, lance, orçamento, textos) é
   decisão do consultor; o agente propõe e espera.
2. Textos conferidos pela régua (abaixo) **antes** de gravar o arquivo.
3. Gravar o JSON em `dados/campanha-<nome>.json` (formato em `scripts/google-ads/README.md`).
4. `gads.py criar-campanha dados/campanha-<nome>.json` → simulação; mostrar a saída ao consultor.
5. Com o aval: `--aplicar`. A campanha nasce **PAUSADA** e não gasta até o protocolo de ativação.

### Protocolo de ativação — a cada vez

Vale para `ativar` e `orcamento`.

1. **Ler o teto** em `anuncios.teto_diario_brl`. Vazio → parar: "sem teto definido, não ativo nada;
   defina o teto pela skill `configuracao`".
2. **Ler o estado:** `gads.py relatorio` (orçamento e status de cada campanha).
3. **Conferir as pré-condições:** verificação de serviços financeiros concluída (Parte a, passo 5);
   peça aprovada na régua; conversão instalada, se o consultor a quer medindo desde o início.
4. **Mostrar ao consultor, lado a lado:**
   ```
   Teto diário:              R$ <teto>
   Orçamento atual:          R$ <x>/dia  (<campanha>)
   Orçamento novo/ativado:   R$ <y>/dia
   Outras campanhas ativas:  R$ <z>/dia
   Peça passou na régua:     sim/não
   ```
   ⚠️ O Google pode gastar num dia acima do orçamento diário, compensando no mês (não conferido
   nas fontes desta skill) — dizer isso ao consultor ao mostrar o quadro.
5. **Pedir o "sim"** do consultor para **esta** ação. Silêncio, "acho que sim", "pode ver" não são
   "sim".
6. **O consultor roda o comando no terminal dele** — `gads.py` exige terminal interativo e o nome
   exato da campanha digitado, e recusa orçamento acima do teto:

   ```bash
   python3 scripts/google-ads/gads.py ativar --campanha-id <id>
   python3 scripts/google-ads/gads.py orcamento --campanha-id <id> --novo-brl <valor>
   ```

7. **Ler de volta** (`relatorio` ou `search` no MCP) e mostrar status e orçamento reais.

### A peça passa pela régua

Títulos, descrições e página de destino são conferidos contra
`conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md` (e o checklist
`04-checklist-de-bolso.md`) antes de irem para o arquivo da campanha. Quem escreveu a peça não é
quem a julga — se foi o agente, apontar isso e pedir a revisão do consultor. Reprovada → não sobe.
`gads.py` só checa limites de caracteres; não julga discurso.

## Saída esperada

- **Configuração:** `anuncios.google` preenchido (`customer_id`, `projeto_cloud`) e os passos da
  Parte (a) pendentes, com o link de cada um — a verificação financeira com as perguntas à
  administradora.
- **Acesso:** nível de acesso do projeto, resultado de `gads.py contas` e do teste do MCP.
- **Operação:** saída da simulação, o que foi criado (pausado), o quadro teto × orçamento de cada
  ativação e o estado lido de volta.

## Limites

- Não cria conta, não faz login, não aceita termos nem cadastra pagamento — isso é do consultor.
- Não ativa nem muda orçamento sem o "sim" da rodada; não digita a confirmação no lugar do
  consultor.
- Não roda nada com orçamento com `teto_diario_brl` vazio, nem acima dele.
- Não escolhe palavra-chave, local, lance, verba, peça, conversão principal nem categoria da
  verificação financeira.
- Não afirma nível de acesso, elegibilidade ao Basic nem enquadramento na verificação financeira —
  são fatos com data (2026-09-24) ou incertos.
