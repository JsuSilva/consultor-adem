---
name: ativacao-whatsapp
description: Roda uma rodada de ativação ativa no WhatsApp Web pelo Claude in Chrome — fila da lista de leads, poda de lead problemático, checagem de histórico antes do disparo, envio com intervalo variável, contato salvo, conversa etiquetada na lista do segmento e linha no log. Invoque com /ativacao-whatsapp quando o consultor já tiver definido segmento, volume e abordagem; não dispara sozinha, porque manda mensagem a pessoa real.
---

# Skill — `ativacao-whatsapp`

> A rodada de prospecção ativa, operada na mão pela sessão principal via Claude in Chrome
> (`mcp__claude-in-chrome__*`, com `browser_batch` para encadear passos). É skill e não agente
> porque precisa da situação de campo, não de fronteira própria.
> A lista de leads vive em `dados/`, mas **a skill não a abre**: quem lê a lista é o script
> `scripts/fila-ativacao.py` — script processa dado nominal, agente não. Sem dado nominal aqui
> dentro: fila, log e planilhas só em `dados/`, fora do Git.

## Limites de cadência

**Os limites de cadência estão em
`conhecimento/maquina-de-vendas/05-cadencia-e-limites-do-whatsapp.md`** — teto diário de primeiros
contatos, janela de horário, regra de parada por envios sem resposta humana e alternância entre
versões de texto aprovadas. Ler antes de toda rodada; esta skill cumpre o que está lá e não mexe nos
números.

Texto único repetido em volume é um dos gatilhos de restrição da conta pela Meta — sem versões
aprovadas pelo consultor, pergunte antes de disparar.

## Quando usar

Quando o consultor já decidiu **segmento, volume, abordagem e faixa de intervalo**, e quer a rodada
executada. Rodada típica: as ativações de um segmento com uma abordagem. A skill não escolhe
nenhuma dessas quatro coisas — ver Limites.

## Entradas

- o **segmento** e a **fila já montada** por `scripts/fila-ativacao.py`, que lê a lista de leads do
  consultor em `dados/`, poda o que não serve e grava o JSON da rodada em `dados/`. Cada lead da
  lista traz nome (ou razão social/nome fantasia), responsável, documento, endereço, telefone e a
  **mensagem pronta** — é dela que sai a mensagem, já com a saudação corrigida pela hora;
- o **volume**, por aproximação — o número pedido quer dizer perto dele, não exatamente ele, e
  nunca acima do teto do doc de cadência. Enviado não é o mesmo que tentado: em campo, cerca de
  **metade dos números de uma lista fria não está no WhatsApp**, então a fila nasce com cerca do
  dobro do alvo. Subir volume em rampa rápida foi o que levou a uma restrição da conta pela Meta;
- a **abordagem aprovada** (ver Passos, 3);
- a **faixa de intervalo** entre envios;
- quem já foi feito em rodadas anteriores, para não repetir.

## Passos

### 1. Fila e poda

Rodar `scripts/fila-ativacao.py` (`--lista`, `--segmento`, `--limite`, `--saudacao`, `--pular`) e
trabalhar o JSON que ele grava. **A ordem na lista não importa** e não se refaz quem já foi feito.
A poda abaixo é a que o script aplica — confira as contagens que ele imprime antes de disparar.
Atenção a uma delas: o script poda número fixo por padrão, e em lista de escritório isso pode ser
quase tudo. Fixo com WhatsApp Business existe; rodar com `--incluir-fixo` e aceitar o número que
não responde é decisão do consultor.

**Pular sem insistir, indo para o próximo:**

- número indisponível;
- contato divergente do cadastro;
- lead cujo campo de responsável traz **nome de empresa em vez de pessoa** — a saudação é montada
  com o primeiro nome do responsável, então um responsável "Hospital Xyz Ltda" produziria
  *"Hospital, bom dia"*.

A regra: se o número não estiver disponível ou houver diferença de contato ou informação, o lead é
pulado e se vai para o próximo, sem se apegar no problema. O foco é atingir o volume o quanto
antes, sem descuidar do intervalo mínimo entre envios, para não levar penalização do WhatsApp.

### 2. Antes de cada disparo — ler a conversa, não só conferir se ela existe

Abrir o chat e **olhar a última mensagem antes de qualquer coisa**. O que se procura não é só "já
falei com essa pessoa": é **se a abordagem planejada ainda faz sentido diante do que já foi dito**.

**O gatilho, e o que fazer com ele:**

1. **Conversa vazia** → seguir com a abordagem.
2. **Conversa com qualquer coisa antes, numa abordagem inicial** → **alerta**. Abordagem inicial
   pressupõe primeiro contato; se já existe mensagem, a premissa caiu.
3. Disparado o alerta, **ler mais atrás** — o suficiente para entender o que aconteceu ali: quem
   falou por último, o que foi pedido, o que foi respondido, em que pé ficou.
4. **Avaliar se a abordagem que ia ser enviada é adequada a esse histórico.** Mandar um primeiro
   contato para quem já recusou, já respondeu, já está em negociação ou já pediu para não ser
   procurado é pior que não mandar nada.
5. **Adequada** → seguir. **Inadequada, ou dúvida** → **parar e perguntar ao consultor**, dizendo o
   que o histórico mostra e qual seria a abordagem certa para aquele contexto. Não improvisar outra
   mensagem no lugar (Regra nº 1 do `AGENTS.md`).

Casos que já apareceram em campo e caem no passo 4: lead que **recusou** ("não temos interesse"),
lead que **respondeu e ficou de retornar em data marcada**, e lead cuja conversa era com **um bot**,
não com a pessoa.

**Por que a checagem é no WhatsApp e não no CRM:** o CRM **não é filtro confiável de "já falei com
essa pessoa"** — teste de controle com um telefone real retornou zero registros embora a pessoa
tivesse sido abordada dias antes. A leitura do chat já evitou disparos repetidos em campo.

**O `--pular` cobre o volume, não o julgamento:** `dados/telefones-trabalhados.txt` tira da fila
quem já foi abordado, mas quem decide se a abordagem cabe naquele histórico é a leitura do chat,
feita lead a lead.

### 2.1 Certeza do contexto — nenhuma mensagem sai sobre suposição

> **Regra:** toda mensagem enviada precisa estar certa do contexto.

**Antes de qualquer envio é preciso saber com quem se está falando.** Não basta o cadastro, não
basta o nome no perfil, e não basta uma resposta que apenas nega.

- **Resposta que só nega não diz quem é a pessoa.** "Não", "não é ela", "número errado", "aqui não
  é" — nenhuma dessas frases informa se quem escreveu é secretária, cônjuge, sócio, ex-dono do
  número ou um desconhecido. **Preencher esse vazio com hipótese é inventar contexto.**
- **A pergunta vem antes do próximo texto**, e é curta:
  *"Desculpe a confusão! Com quem eu falo, por favor?"* — e, se couber, *"você trabalha com o(a)
  Dr(a). [Nome]?"*. Só com a resposta se escolhe qual abordagem usar.
- **Vale nos dois sentidos:** nem tratar pessoa física como recepção, nem tratar recepção como se
  fosse o profissional.
- **Na dúvida, não envia.** Perguntar custa uma linha; mensagem errada queima o contato e a régua.
- **A abertura continua a mesma** — perguntar pelo nome do profissional é o que expõe o erro de
  cadastro. O que muda é o que se faz com o "não": **o número pode ter trocado de dono, ou o dado
  do cadastro pode estar errado**, e nenhuma das duas hipóteses se confirma sem perguntar.

**Erro real que originou a regra.** Um número cadastrado no CNPJ de uma médica respondeu apenas
*"Bom dia, não"*. O agente concluiu sozinho que era a recepção da clínica e disparou a mensagem de
encaminhamento tratando a pessoa como secretária — **ela nunca disse isso**. O certo era perguntar
quem era e entender a situação antes de escrever qualquer coisa.

### 3. Disparo

URL: `https://web.whatsapp.com/send?phone=55<DDD><NUMERO>&text=<texto url-encoded>`.

**Saudação pela hora corrente:** "bom dia" até as 12h, "boa tarde" depois — mesmo que a mensagem
pronta da lista traga outra.

**Intervalo variável de 70 a 180 segundos** entre envios, para não levar penalização do WhatsApp.
Em lote de mídia pesada, **2 a 4 minutos**, com a rodada quebrada em dois blocos e uma pausa no
meio.

**Janela de horário:** a do doc de cadência, só em dia útil, sem feriado. Fora dela não se dispara,
nem para fechar o número do dia.

**Nunca improvisar texto.** A abordagem é a aprovada pelo consultor, uma por segmento — a mensagem
pronta de cada lead da lista, ou o texto que ele passou verbatim. Usar a da lista, não reescrever.

### 4. Depois de cada disparo

1. **Salvar o contato** pelo cabeçalho do chat → Add → **nome da pessoa no campo "nome"; razão
   social + endereço no campo "sobrenome"** — é no próprio WhatsApp que o consultor vai saber com
   quem fala caso a pessoa responda.
2. **Etiquetar a conversa** na lista do segmento — clique direito na linha da conversa → *Add to
   list*, na lista com o nome do segmento e da abordagem (por exemplo, "Estética Abordagem 1").
   **Antes do clique direito, isole a conversa pela busca.** A lista de conversas se reordena
   sozinha a cada mensagem que chega — de qualquer contato, não só dos leads da rodada — e a linha
   que estava na posição certa no screenshot já é outra no instante do clique. Já aconteceu de o
   menu abrir sobre o vizinho. O caminho seguro: digitar o nome recém-salvo no campo *Search*,
   esperar o resultado único, e clicar com o botão direito nele — resultado de busca não se
   reordena. Depois limpar a busca no × antes do próximo lead.
   Continua valendo conferir o ✓ por zoom antes de sair do submenu: clicar numa lista já marcada
   **remove** a etiqueta.
3. **Registrar a linha em `dados/ativacoes.csv`** — arquivo único e append-only, colunas
   `data_hora, telefone, nome, segmento, abordagem, status`. Não é log solto de rodada: é a fonte do
   `--pular` da próxima fila (`telefones-trabalhados.txt` é derivado dele) e da contagem de novos
   contatos do placar do dia (`scripts/placar-dia.py`). Rodada que não escreve aqui some do histórico.
   **Contato que chega por indicação também entra aqui:** `segmento` = `Indicacao`, `abordagem`
   vazia, `status` = `enviado`, e na `obs` quem indicou e o próximo passo. É o que faz a contagem do
   dia enxergar o contato. O telefone vai também para `telefones-trabalhados.txt`, para o indicado
   nunca cair numa fila fria.

   **`status = enviado` só na linha que cria card no CRM.** A contagem do dia soma `enviado` e `ok`;
   o CRM conta **card criado no dia**. Se as duas réguas forem a mesma, todo dia com segunda
   mensagem sai desencontrado. Então:
   - **primeiro contato**, e contato de network ou indicação que vira card novo → `enviado`;
   - **segunda mensagem para quem já foi contado** — encaminhamento, encerramento, follow-up com
     link, resposta no mesmo dia → **`followup`**, que a contagem ignora;
   - **follow-up de lead antiga**, que já tem card de outro dia → **`followup`**, mesmo que o
     telefone nunca tenha aparecido no CSV.
   `sair` e `bloqueio` continuam como estão: já ficam fora da contagem pelo próprio status.

### 5. Triagem de respostas

- **Resposta automática não conta como resposta.** Só conta a resposta humana. Já apareceram em
  campo assistente virtual de clínica, bot de escritório de contabilidade e autorresposta de
  agenda. Só entra como respondente quem escreveu de próprio punho.
- **Ler o fio inteiro antes de classificar.** Erro real: uma lead foi reportada como interessada
  depois de ter recusado — *"não temos interesse"* —, porque a pergunta seguinte no fio era do
  próprio consultor.
- **Lead que recusou não vai direto para Removidos.** O encerramento segue a regra do SAIR, que mora
  na skill `follow-up`: uma última mensagem, silêncio mantém o contato, e só a resposta SAIR remove.

## Limite técnico conhecido

**Vídeo-bolinha (video note / PTV) não pode ser encaminhado pelo WhatsApp Web** — não existe
"Forward" no menu da mensagem. Encaminhamento desse formato é manual, pelo celular.

## Saída esperada

Ao fim da rodada, um fechamento curto: **quantos ativados** · **quem foi pulado e por quê** (número
indisponível, contato divergente, responsável pessoa jurídica) · **o caminho do log** em `dados/` ·
e o **gancho para a carga no CRM**, que não é desta skill: é da skill irmã **`crm-apollo`**, para
quem usa o CRM Apollo.

## Limites

- **Não enviar mensagem sobre suposição de contexto** — sem saber quem é o interlocutor,
  pergunta-se antes (Passos, 2.1).
- **Não enviar texto que o consultor não aprovou** — a fala vai a pessoa real e não tem revisão de
  compliance no caminho.
- **Intervalo mínimo de 70 s, sempre variável** — cadência fixa é o que o WhatsApp penaliza.
- **Teto diário de primeiros contatos: o do doc de cadência.** O agente **não sobe esse número por
  conta própria**: rampa de volume proposta pelo agente já terminou em conta restrita pela Meta.
  Volume só sobe com aval explícito do consultor e depois de aparecer resposta humana.
- **Só na janela de horário do doc de cadência, em dia útil.**
- **Regra de parada do doc de cadência:** atingido o número de envios sem nenhuma resposta humana,
  a rodada para. Antes de continuar, a abordagem é revista com o consultor.
- **Alternar entre as versões aprovadas da abordagem** — texto idêntico repetido é assinatura de
  disparo em massa. As versões são aprovadas uma a uma pelo consultor; enquanto não existirem, roda
  a abordagem única e o teto de volume é a única proteção.
- **Não insistir em lead problemático** — o custo do problema é maior que o do lead; o foco é o
  volume.
- **Resposta automática não conta** — respondente é quem escreveu de próprio punho.
- **Nenhum dado nominal em arquivo versionado:** fila, log e planilhas só em `dados/`.
- **Conferir em qual aba se está agindo antes de qualquer escrita** — já houve erro real de operar
  na aba errada.
- **A skill não decide segmento, volume, abordagem nem faixa de intervalo.** Isso é do consultor
  (Regra nº 1 do `AGENTS.md`); sem essas quatro definições, a skill pergunta em vez de supor.
