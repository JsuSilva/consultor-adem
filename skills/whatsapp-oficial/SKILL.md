---
name: whatsapp-oficial
description: BETA — conecta o agente ao WhatsApp Business Tools MCP oficial da Meta (Cloud API) para listar a conta, registrar número, criar templates, configurar webhooks e enviar mensagem por template ou dentro da janela de 24h, com trava de "sim" por rodada. Invoque com /whatsapp-oficial quando o consultor quiser montar ou testar o WhatsApp oficial da empresa; não dispara sozinha, porque manda mensagem a pessoa real.
---

# Skill — `whatsapp-oficial` (beta)

> **⚠️ Aviso — leia antes de usar.**
> 1. Nas palavras da própria Meta: *"This release is built for development and testing workflows,
>    not production sending at scale."* — é para **desenvolver e testar**, não para disparo em escala.
> 2. Esta skill é **beta** no repositório: nasceu em 2026-09-24, sem uso de campo.
> 3. **Disponibilidade no Brasil: INCERTA.** A Meta não publicou lista de países; só se sabe
>    conectando. Limite de uso por usuário e por ferramenta existe, **sem números publicados**.
>
> Prospecção ativa do dia a dia continua na skill **`whatsapp-web`** (ver o fim deste documento).
> IDs vão em `config/consultor.json` → `anuncios.whatsapp_oficial.*` (fora do Git). **Credenciais
> nunca ali:** token fica em `.env` ou `~/.config/consultor-adem/`.

Fontes (conferidas em 2026-09-24): doc https://developers.facebook.com/documentation/mcp/whatsapp-business-tools-mcp ·
anúncio de 15/09/2026 https://developers.facebook.com/blog/post/2026/09/15/whatsapp-business-messaging-mcp-ai-agent/

## Regras

1. **Envio só com o "sim" do consultor naquela rodada** — para aquele texto, aquele(s)
   destinatário(s), aquele momento. "Sim" de rodada anterior não vale.
2. **Todo template passa pela régua** de
   `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md` antes de ser criado ou
   editado: consórcio não é investimento, nenhuma promessa de contemplação, data ou chance.
3. **Cadência:** respeitar `conhecimento/maquina-de-vendas/05-cadencia-e-limites-do-whatsapp.md` —
   teto diário, janela de horário, regra de parada por falta de resposta humana. A skill não mexe
   nesses números.
4. **Não é canal de disparo em massa.** O próprio aviso da Meta exclui isso; volume sobe só com
   aval do consultor, e nunca além do doc de cadência.
5. **LGPD:** telefone e nome de lead ficam em `dados/`, fora do Git; nunca em template, arquivo
   versionado ou no chat além do necessário para o envio aprovado.
6. **Não decide pelo consultor** (Regra nº 1 do `AGENTS.md`): número, texto de template, público e
   momento do envio são dele.

## Requisitos (conferir antes de conectar)

1. O consultor é **admin (permissão MANAGE)** do portfólio empresarial da Meta.
2. Existe um **app com o produto WhatsApp** em developers.facebook.com, do qual ele é **admin**.
3. **Termos da Cloud API aceitos** — pelo consultor, na tela da Meta; o agente não aceita termo.
4. **Forma de pagamento** cadastrada na conta do WhatsApp Business.
5. **Verificação da empresa** concluída (passo 4 da Parte (a) da skill `anuncios-meta`).

Faltando qualquer um: parar, dizer qual falta e o link; não seguir.

## Passo a passo de conexão

1. **Adicionar o servidor no Claude Code:**

   ```bash
   claude mcp add --transport http whatsapp_business_tools https://mcp.facebook.com/whatsapp_business_tools
   ```

2. **Autenticar:** `/mcp` no Claude Code → escolher `whatsapp_business_tools` → login OAuth da
   Meta, feito pelo consultor. Escopos pedidos: `business_management`,
   `whatsapp_business_management`, `whatsapp_business_messaging`.
3. **Teste de leitura** (nada envia): listar negócios, contas do WhatsApp Business (WABA) e números.
   Erro de acesso ou ferramenta ausente = não liberado para a conta (ver aviso sobre Brasil);
   registrar o erro exato e parar.
4. **Gravar os IDs** — mostrar ao consultor, esperar o "ok" e gravar:

   ```json
   "whatsapp_oficial": {
     "waba_id": "<id da conta do WhatsApp Business>",
     "numero_id": "<id do número de telefone>"
   }
   ```

   Validar o JSON e confirmar com `git status` que `config/consultor.json` não aparece.
5. **Número novo** (se o consultor ainda não tem um na Cloud API): adicionar o número, verificar por
   código (OTP — o consultor recebe e informa) e registrar na Cloud API. ⚠️ Não conferido aqui se um
   número em uso no aplicativo do WhatsApp pode ir para a Cloud API ao mesmo tempo — **não usar o
   número pessoal da prospecção** sem o consultor confirmar isso na documentação; perder o número
   do dia a dia seria pior que não ter o canal oficial.
6. **Token de usuário do sistema**, se o consultor quiser um para scripts: a ferramenta gera; o
   consultor cola em `.env` (fora do Git), na variável `WHATSAPP_TOKEN`. O agente não repete o token no
   chat nem o grava em outro lugar.

## O que faz

| Grupo | O que | Risco |
|---|---|---|
| Conta | listar negócios, WABA e números | leitura — livre |
| Número | adicionar, verificar por OTP, registrar na Cloud API | escreve — aval do consultor por passo |
| Templates | criar, editar, apagar | escreve — régua de compliance + aval; apagar pede "sim" explícito |
| Webhooks | configurar | escreve — aval do consultor; a URL de destino é dele |
| Token | gerar token de usuário do sistema | credencial — vai direto para `.env` |
| **Mensagem** | **enviar por template, ou texto livre dentro da janela de 24h** | **vai a pessoa real — protocolo de envio** |

## Protocolo de envio — a cada rodada

1. Ler o doc de cadência e checar: dia útil, janela de horário, teto do dia, regra de parada.
2. Confirmar que o texto é um **template aprovado pela régua** ou resposta **dentro da janela de
   24h** aberta pela pessoa. Fora disso, não envia.
3. Mostrar ao consultor: template (ou texto), variáveis preenchidas, destinatário(s), quantidade.
4. Esperar o **"sim"** daquela rodada. Sem ele, nada sai.
5. Enviar e ler de volta o status de cada mensagem; relatar falhas sem reenviar por conta própria.
6. **Registrar cada envio em `dados/ativacoes.csv`**, no mesmo formato da skill `whatsapp-web`
   (mesmas colunas — `data_hora, telefone, nome, segmento, abordagem, status`, mais a `obs` — e
   mesma regra de `status`), com o canal indicado na `obs`: `canal: whatsapp-oficial`. É o que faz
   o placar do dia e o `--pular` da próxima fila enxergarem o contato. Envio sem linha some do
   histórico.

## WhatsApp Web × Cloud API oficial — quando usar cada uma

| | `whatsapp-web` | `whatsapp-oficial` |
|---|---|---|
| Canal | o WhatsApp do consultor, no navegador, pelo Claude in Chrome | Cloud API da Meta, número da empresa, pelo MCP oficial |
| Estado | em uso de campo | **beta**, feito para desenvolvimento e teste |
| Primeiro contato | texto aprovado pelo consultor, 1 a 1, com intervalo variável | só por **template** |
| Resposta | conversa livre | texto livre só **dentro da janela de 24h** |
| Histórico | lê a conversa antes de cada envio | não substitui a leitura do fio — sem histórico, perguntar antes |
| Cadência | doc de cadência | o mesmo doc de cadência |
| Uso indicado | prospecção ativa e conversa do dia a dia | montar e testar o canal oficial: templates, webhooks, número da empresa |

- **Uma pessoa, um canal por vez.** O mesmo lead não recebe mensagem pelos dois WhatsApps (Web e
  oficial) na mesma cadência — o toque conta uma vez só e a pessoa não deve ver dois remetentes.
- Migrar a prospecção para a Cloud API é **decisão do consultor**; hoje o aviso da Meta exclui envio
  em escala.

## Saída esperada

- **Conexão:** requisitos conferidos, resultado do teste de leitura, IDs gravados em
  `anuncios.whatsapp_oficial`.
- **Rodada:** quantas mensagens saíram, quais falharam e por quê, e a linha em `dados/ativacoes.csv`.

## Limites

- Não envia nada sem o "sim" da rodada; não cria template que não passou pela régua.
- Não aceita termos, não cadastra pagamento, não cria conta nem faz login pelo consultor.
- Não usa o canal para disparo em escala; não passa do teto do doc de cadência.
- Não afirma que o serviço está disponível no Brasil nem que saiu do beta.
- Não mexe no número da prospecção do consultor sem ele confirmar o efeito.
