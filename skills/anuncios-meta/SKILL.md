---
name: anuncios-meta
description: Configura do zero e opera anúncios na Meta (Facebook e Instagram) — portfólio empresarial, conta de anúncio, página, Instagram, verificação, pixel e Conversions API; conecta o agente pelo MCP oficial, pela CLI oficial ou pelo Pipeboard; e opera campanhas com travas de verba (teto diário e "sim" por rodada). Invoque com /anuncios-meta quando o consultor quiser montar a conta, conectar o agente, ler resultados ou subir campanha; não dispara sozinha, porque gasta dinheiro e publica peça.
---

# Skill — `anuncios-meta`

> Três partes: **(a)** a conta da Meta configurada do zero, **(b)** o acesso do agente, gravado em
> `anuncios.meta.acesso`, e **(c)** a operação com travas. Fatos verificados em **2026-09-24**; o que
> está marcado **INCERTO** não tem fonte oficial e deve ser dito assim ao consultor.
> IDs vão em `config/consultor.json` → `anuncios.meta.*` (fora do Git). **Credenciais nunca ali:**
> token, app secret e afins ficam em `.env` (no `.gitignore`) ou em `~/.config/consultor-adem/`.

## Regras

1. **Nada que gasta verba ou mexe em gente real sem o "sim" do consultor naquela rodada.** Ativar
   anúncio, mudar orçamento, impulsionar post e subir público com dado pessoal — cada um pede o seu
   "sim". "Sim" de rodada anterior, de outra campanha ou deste documento não vale.
2. **Teto diário é trava dura.** `anuncios.teto_diario_brl` vazio = nenhuma ativação. Pedido acima
   do teto = recusa; o agente não sobe o teto, só o consultor, editando a configuração.
3. **Toda peça passa pela régua** de `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`
   antes de subir: consórcio não é investimento, nenhuma promessa de contemplação, data ou chance.
4. **Não decide pelo consultor** (Regra nº 1 do `AGENTS.md`): objetivo da campanha, público, verba,
   peça e caminho de acesso são dele. A skill apresenta opções e espera.
5. **Nunca pôr token em arquivo versionado**, nem em URL gravada em arquivo versionado.
6. **Uma escrita por vez e conferida:** depois de criar ou alterar, ler de volta a entidade e mostrar
   o estado real (status, orçamento, público).

---

## Parte (a) — Configuração da conta, do zero

O consultor faz estes passos **na própria mão**, logado na Meta; o agente orienta e não cria conta,
não faz login, não aceita termo. Os links são a ajuda oficial — os passos abaixo são o procedimento
geral; havendo diferença na tela, **vale o link**.

1. **Portfólio empresarial** (antigo Gerenciador de Negócios) — em business.facebook.com, criar o
   portfólio com nome do negócio, nome e e-mail comercial do consultor.
   https://www.facebook.com/business/help/1710077379203657
   Anotar o ID do portfólio → `anuncios.meta.business_id`.
2. **Conta de anúncio** — dentro do portfólio, em Configurações do Negócio > Contas de anúncio,
   criar uma nova. **Moeda BRL e fuso de São Paulo (ou o do consultor):** ⚠️ moeda e fuso em geral
   não se trocam depois (não conferido no link) — conferir antes de confirmar. Atribuir o consultor como administrador e
   cadastrar a forma de pagamento.
   https://www.facebook.com/business/help/910137316041095
   Anotar o ID (`act_...`) → `anuncios.meta.ad_account_id`.
3. **Página do Facebook e Instagram** — adicionar ao portfólio a página existente (ou criar uma) e
   conectar a conta profissional do Instagram (Configurações do Negócio > Contas > Páginas / Contas
   do Instagram). Anotar os IDs → `anuncios.meta.pagina_id` e `anuncios.meta.instagram_id`.
4. **Verificação da empresa** — Central de Segurança do portfólio, com os documentos do negócio
   (CNPJ, comprovante com nome e endereço iguais ao cadastro). É pré-requisito do WhatsApp oficial
   (skill `whatsapp-oficial`) e ajuda na política de serviços financeiros.
   https://pt-br.facebook.com/business/help/1095661473946872 ·
   https://www.facebook.com/business/help/2058515294227817
5. **Pixel / dataset e Conversions API** — no Gerenciador de Eventos, criar o dataset (pixel),
   instalar no site (código base ou integração da plataforma do site) e, quando houver servidor,
   ligar a Conversions API para mandar os eventos também pelo servidor. Anotar o ID →
   `anuncios.meta.pixel_id`.
   Pixel/dataset: https://www.facebook.com/business/help/952192354843755 ·
   Conversions API: https://www.facebook.com/business/help/AboutConversionsAPI ·
   opções de configuração: https://www.facebook.com/business/help/433493041367251 ·
   para desenvolvedor: https://developers.facebook.com/documentation/ads-commerce/conversions-api/get-started
   Formulário de lead no site que alimenta o pixel coleta dado pessoal: ver LGPD na Parte (c).
6. **Política de serviços financeiros** — consórcio é serviço financeiro para a Meta.
   - Vale **sempre**, em qualquer país: público **18+** e a Meta **pode exigir verificação e
     autorização do regulador local** para veicular.
     https://transparency.meta.com/policies/ad-standards/restricted-goods-services/financial-services/
   - **Categoria especial de anúncio (crédito/serviços financeiros): hoje obrigatória só em EUA,
     Canadá e Europa — o Brasil não está listado** (conferido em 2026-09-24; pode mudar, conferir
     antes de cada campanha).
     https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category ·
     ajuda: https://www.facebook.com/business/help/298000447747885
   - Se a Meta pedir autorização do regulador, o consultor confirma com a administradora qual
     documento apresentar — o agente não presume que o consultor está ou não autorizado.
7. **Gravar os IDs** — mostrar o bloco `anuncios.meta` ao consultor, esperar o "ok" e gravar em
   `config/consultor.json`. Validar o JSON e confirmar com `git status` que o arquivo não aparece.

---

## Parte (b) — O acesso do agente → `anuncios.meta.acesso`

Três caminhos. **A escolha é do consultor**; a skill apresenta, ele decide, e só então grava
`anuncios.meta.acesso` com `"mcp_oficial"`, `"cli"` ou `"pipeboard"`.

| Caminho | Quem opera | Dado passa por | Custo | Quando |
|---|---|---|---|---|
| `mcp_oficial` | servidor MCP da Meta | só Meta | sem custo de acesso | **principal** |
| `cli` | CLI oficial `meta-ads`, rodada pelo agente no terminal | só Meta | sem custo de acesso | quando o consultor prefere comando e token próprio, ou para lote |
| `pipeboard` | servidor MCP de terceiro | **servidores da Pipeboard** | plano grátis limitado; pagos acima | **alternativa** quando o MCP oficial não estiver liberado para a conta |

### `mcp_oficial` — Meta Ads MCP (principal)

- Endereço: `https://mcp.facebook.com/ads`. **Beta aberto desde 29/04/2026.**
  Visão geral: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-overview ·
  começar: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started ·
  ajuda: https://www.facebook.com/business/help/1456422242197840
- **Disponibilidade no Brasil: INCERTA.** Não há restrição oficial por país; terceiros relatam
  liberação gradual. Só se sabe conectando e testando (abaixo).

**Conectar sem app próprio** — conector personalizado do Claude apontando para
`https://mcp.facebook.com/ads`, com login OAuth (Facebook Login for Business). O consultor faz o
login e escolhe o portfólio e a conta de anúncio que o agente enxerga.

**Conectar com app próprio** — o app (em developers.facebook.com) precisa da permissão
`ads_mcp_management` (disponível desde 16/07/2026:
https://developers.facebook.com/blog/post/2026/07/16/meta-ads-mcp-server/). No Claude Code:

```bash
claude mcp add --transport http --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads
```

Depois, `/mcp` no Claude Code para autenticar. O App ID não é segredo, mas o app secret é — se
algum passo pedir, vai para `.env`, nunca para `config/consultor.json`.

**Testar se está liberado para a conta** — só leitura, nada gasta:
1. `ads_get_ad_entities` na conta de `anuncios.meta.ad_account_id` → deve listar campanhas (ou
   lista vazia, em conta nova).
2. `ads_get_errors` / `ads_account_get_activity_logs` → confirmam que a conta responde.
3. Erro de permissão, conta não encontrada ou ferramenta ausente = não liberado para essa conta.
   Registrar o erro exato e apresentar ao consultor a alternativa `pipeboard` ou `cli`.

**"Regras" do portfólio que limitam o agente** — a Meta anunciou controles para limitar o que o
agente pode fazer (https://www.facebook.com/business/news/meta-ads-ai-connectors). **O caminho de
configuração é INCERTO:** só um blog de terceiro aponta *Configurações do Negócio > Integrações >
Ads MCP Server*. Indício de terceiro: **escrita liberada por padrão**. Orientar o consultor a
procurar esse painel e, se existir, restringir o que ele quiser; a trava desta skill (Parte c)
vale com ou sem ele.

### `cli` — Meta Ads CLI oficial

- Pacote: `meta-ads` **v1.1.0** (17/06/2026), **Python ≥ 3.12**, licença proprietária.
  Doc: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started.md ·
  PyPI: https://pypi.org/project/meta-ads/
- **Instalação** — num ambiente virtual do projeto, não global:

  ```bash
  python3.12 -m venv .venv && source .venv/bin/activate
  pip install meta-ads
  ```

- **Usuário do sistema** — em Configurações do Negócio > Usuários > Usuários do sistema, criar um
  usuário do sistema **admin**, **atribuir a ele os ativos** (conta de anúncio, página, pixel,
  catálogo) e gerar o token com os escopos:
  `business_management`, `ads_management`, `pages_show_list`, `pages_read_engagement`,
  `pages_manage_ads`, `catalog_management`, `read_insights`.
- **`.env`** (fora do Git) — o consultor cola o token; o agente não pede o token no chat:

  ```bash
  ACCESS_TOKEN=...          # token do usuário do sistema
  AD_ACCOUNT_ID=act_...     # o mesmo de anuncios.meta.ad_account_id
  BUSINESS_ID=...           # opcional
  ```

  ⚠️ Não verificado se a CLI lê o `.env` sozinha; se não ler, carregar antes com
  `set -a; source .env; set +a`.
- **Comandos** — `meta auth` para conferir a autenticação; depois
  `meta ads <campaign|adset|ad|creative|insights|catalog|dataset|page> <list|get|create|update|delete>`,
  com `-o table|json|plain` (o agente usa `-o json` para ler de volta).
- **Sempre `--status PAUSED` em todo `create`.** INCERTO (fonte de terceiro): a CLI cria **ATIVO**
  por padrão — um `create` sem a flag pode começar a gastar na hora. Sem exceção.
- Ativar ou mudar orçamento pela CLI (`update`) segue o mesmo protocolo da Parte (c).

### `pipeboard` — alternativa de terceiro

- Repositório: https://github.com/pipeboard-co/meta-ads-mcp (licença BSL 1.1) · servidor remoto
  `https://meta-ads.mcp.pipeboard.co/` · planos: https://pipeboard.co/pricing (Free: 30 execuções
  por semana e 2 contas; planos pagos acima).
- **Avisar o consultor antes de escolher:** é **empresa terceira**, não a Meta — **os dados da
  conta de anúncio passam pelos servidores dela** — e o uso além do plano grátis é **pago**.
- Conectar no Claude Code como servidor HTTP remoto (`claude mcp add --transport http pipeboard
  https://meta-ads.mcp.pipeboard.co/`); ⚠️ o método de autenticação deve seguir o README do
  repositório — não verificado aqui.
- **Nunca gravar token na URL** em arquivo versionado (`.mcp.json` do repo incluso). Se o método
  exigir token na URL, a configuração fica no escopo do usuário do Claude Code, não no projeto.
- As ferramentas têm outros nomes; a classificação por risco da Parte (c) vale pelo efeito
  (lê / escreve / gasta), não pelo nome. Na dúvida sobre o efeito, tratar como **gasta**.

---

## Parte (c) — Operação com travas

### Ferramentas por risco (MCP oficial)

Doc: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-tools-ad-creation-and-management

| Risco | Ferramentas | O que o agente pode fazer |
|---|---|---|
| **Leitura** | `ads_get_ad_entities`, `ads_insights_*`, `ads_get_dataset_*`, `ads_get_errors`, `ads_library_search`, `ads_account_get_activity_logs` | livre, quando o consultor pedir |
| **Escreve, nasce pausado** | `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad` | com o aval do consultor ao plano da campanha; nasce **PAUSADA** — conferir o status ao ler de volta |
| **Escreve sem gastar** | `ads_create_creative`, `ads_create_custom_audience`, `ads_delete_custom_audience`, catálogo, pixel (`ads_pixel_event_create/update/delete`), experimentos | com aval do consultor por item; apagar pede "sim" explícito |
| **Escreve com dado pessoal** | `ads_update_custom_audience_users` (sobe lista com hash) | **só com "sim" da rodada + base legal registrada** (ver LGPD) |
| **GASTA / muda verba** | `ads_activate_entity` (pausado → ativo), `ads_update_entity` (inclui orçamento), `ads_boost_ig_post` | **só pelo protocolo de ativação abaixo** |

Na CLI, o equivalente: `list`/`get`/`insights` = leitura; `create` com `--status PAUSED` = escreve
pausado; `update` que muda status para ativo ou mexe em orçamento = **gasta**; `delete` = pede "sim".

### Protocolo de ativação — a cada vez

Vale para ativar campanha, conjunto ou anúncio, mudar orçamento e impulsionar post.

1. **Ler o teto** em `config/consultor.json` → `anuncios.teto_diario_brl`.
   Vazio → parar: "sem teto definido, não ativo nada; defina o teto pela skill `configuracao`".
2. **Somar a verba diária** que ficará ativa na conta depois da ação: o que já está rodando
   (ler com `ads_get_ad_entities`) **mais** o orçamento pedido. ⚠️ Orçamento vitalício: convenção
   proposta, a confirmar com o consultor — total ÷ dias do período. Mostrar a conta.
3. **Mostrar ao consultor, lado a lado:**
   ```
   Teto diário:           R$ <teto>
   Já ativo na conta:     R$ <x>/dia
   Pedido nesta ação:     R$ <y>/dia  (<entidade>, <nome>, <período>)
   Total após ativar:     R$ <x+y>/dia
   Peça passou na régua de compliance: sim/não
   ```
4. **Total acima do teto → recusa.** Dizer quanto excede e as saídas (reduzir o orçamento, pausar
   outra campanha, ou o consultor subir o teto na configuração). O agente não sobe o teto.
5. **Dentro do teto → pedir o "sim"** do consultor para **esta** ação. Sem "sim" explícito na
   rodada, nada acontece. Silêncio, "acho que sim", "pode ver" não são "sim".
6. **Executar uma ação** e **ler de volta**: status real e orçamento real. Mostrar ao consultor.

### A peça passa pela régua

Antes de `ads_create_creative` ou `ads_boost_ig_post`, o texto e a arte são conferidos contra
`conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md` (e o checklist
`04-checklist-de-bolso.md`). Quem escreveu a peça não é quem a julga — se foi o agente, apontar isso
e pedir ao consultor a revisão. Reprovada → não sobe. Post a impulsionar também é peça.

### Público com dado pessoal — LGPD

- Subir lista de clientes ou leads (`ads_update_custom_audience_users`, ou upload na CLI) é
  tratamento de dado pessoal, mesmo com hash.
- Só com **"sim" do consultor naquela rodada** e **base legal registrada** por ele (consentimento,
  legítimo interesse etc.). Fontes: `conhecimento/fontes-publicas/04-lgpd-legitimo-interesse-prospeccao-b2b.md`
  e `06-lgpd-dado-publico-e-abordagem-como-fornecedor.md`. O agente não escolhe a base legal.
- A lista vem de `dados/` (fora do Git) e é lida por script, não colada no chat; nunca vai para
  arquivo versionado.

## Saída esperada

- **Configuração:** o bloco `anuncios.meta` preenchido e os passos da Parte (a) que ficaram
  pendentes, com o link de cada um.
- **Acesso:** o valor gravado em `anuncios.meta.acesso` e o resultado do teste de leitura.
- **Operação:** o que foi criado (pausado), o que foi ativado com o quadro teto × orçamento, e o
  estado lido de volta.

## Limites

- Não cria conta, não faz login, não aceita termos nem cadastra pagamento — isso é do consultor.
- Não ativa, não muda orçamento, não impulsiona e não sobe público sem o "sim" da rodada.
- Não ativa nada com `teto_diario_brl` vazio, nem acima dele.
- Não escolhe objetivo, público, verba, peça, base legal nem caminho de acesso.
- Não afirma que o MCP oficial está disponível no Brasil nem que a categoria especial é
  dispensada para sempre — são fatos com data, conferidos em 2026-09-24.
