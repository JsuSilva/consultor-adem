---
name: whatsapp-web
description: Roda uma rodada de ativação ativa no WhatsApp Web pelo Claude in Chrome — fila da lista de leads, poda de lead problemático, checagem de histórico antes do disparo, envio com intervalo variável, contato salvo e linha no log. Invoque com /whatsapp-web quando o consultor já tiver definido segmento, volume e abordagem; não dispara sozinha, porque manda mensagem a pessoa real.
---

# Skill — `whatsapp-web`

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

**A conversa se abre pelo telefone, nunca pelo nome.** Caso de campo: dois cadastros com a **mesma
razão social, o mesmo endereço e nomes quase iguais**, telefones diferentes. A sessão leu o fio da
pessoa errada, viu um **SAIR** e quase deixou de fora da rodada quem devia receber. Nome parecido não
é a mesma pessoa, e razão social igual não é a mesma pessoa: **o telefone é a chave**. Ao buscar pelo
nome e voltar mais de um resultado, resolva pelo número antes de escrever qualquer coisa.

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

### 2.0 Conversa não lida não se abre — a resposta do cliente é do consultor

> **Regra:** não ler conversa que esteja como não lida — quem dá continuidade à resposta do cliente
> é o consultor, pessoalmente.

**Abrir um fio marca a conversa como lida.** Em campo, a sessão reabriu fios de leads que tinham
respondido — para salvar contato, etiquetar e ler a resposta —, não avisou e não remarcou como não
lido. No dia seguinte o consultor encontrou pessoas que haviam respondido sem o sinal de não lida.

- **Antes de abrir qualquer fio que já existe**, olhar a linha dele na lista de conversas. Com selo
  de não lida, **não abrir**: nem para salvar contato, nem para etiquetar, nem para colher a entrada.
- **O que se faz no lugar:** avisar o consultor de quem respondeu, com a hora que a lista mostra.
  Contato salvo daquele lead fica pendente e é reportado como pendente.
- **Fio novo, aberto pelo link de envio com a conversa vazia, não é o caso** — ali não há resposta.
- **Se um fio com resposta for aberto por engano:** avisar na hora e marcar como não lido de volta.
- Quem muda esta regra é o consultor.

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

**Janela de horário:** a do doc de cadência, só em dia útil, sem feriado. Fora dela não se dispara
**frio** — abertura e cobrança —, nem para fechar o número do dia. **Resposta dentro de conversa
viva não tem janela:** lead que escreveu há pouco é respondido na hora, inclusive à noite. O que
define "conversa viva" é a última mensagem ser dele e ser recente — não é o fio existir; fio parado
há dias volta a ser disparo frio e obedece à janela. A saída fora da janela é registrada como tal
na `obs` do `ativacoes.csv`, com a hora da mensagem do lead ao lado, para o motivo ficar auditável.
A distinção protege em vez de afrouxar: o que a Meta pune é a razão entre conversas iniciadas e
conversas respondidas — responder quem escreveu melhora essa razão; iniciar conversa fora de hora
piora.

**Nunca improvisar texto.** A abordagem é a aprovada pelo consultor, uma por segmento — a mensagem
pronta de cada lead da lista, ou o texto que ele passou verbatim. Usar a da lista, não reescrever.

**Disparar sempre por este bloco, nunca clicando no pixel do botão.** Em campo, o clique por
coordenada falhou em **dois de cada três** envios — não é posição errada: a mesma coordenada
funciona e falha alternadamente. O clique por JS no elemento resolveu, com `tentativas: 1` em
treze envios seguidos. O bloco já traz a trava de contato e a prova de que saiu:

```js
const comp = () => (document.querySelector('#main footer [contenteditable="true"]')?.innerText || '').trim();
const quem = document.querySelector('#main header')?.innerText.split('\n')[0] || '';
if (/contador|contabilidade|escrit[óo]rio|suporte|atendimento|recep/i.test(quem)) throw new Error('ABORTA: o contato não é o lead — ' + quem);
const antes = comp();
if (!antes) throw new Error('ABORTA: composer vazio — número pode não estar no WhatsApp');
const btn = document.querySelector('#main footer button[aria-label="Send"]');
if (!btn) throw new Error('ABORTA: botão de enviar não encontrado');
let ok = false;
for (let i = 0; i < 4; i++) { btn.click(); await new Promise(r => setTimeout(r, 1200)); if (comp() === '') { ok = true; break; } }
({ quem, enviado: ok, texto: antes.slice(0, 50) })
```

**As travas existem porque todas falharam em campo:**

1. **`enviado: false` é mensagem perdida.** Em campo, dez mensagens foram dadas por enviadas e
   ficaram como rascunho na conversa — aparecendo como "Draft:" na lateral, parecendo enviadas.
2. **Composer vazio** quer dizer que o prefill não entrou, e quase sempre que o número não está no
   WhatsApp — o próprio WhatsApp já confirmou: *"the number isn't on WhatsApp"*.
3. **O nome salvo no contato diz de quem é o telefone, e muitas vezes não é o lead.** Dois casos de
   campo: um contato salvo como contador de médico, que respondeu com menu de escritório, e outro
   salvo como suporte de uma empresa, que estava na fila com nome de profissional. **A lista de
   leads não sabe o nome que está salvo no WhatsApp — essa trava só existe no momento do disparo.**
   O padrão cobre escritório, suporte, atendimento e recepção, e veio de rodadas com profissionais
   liberais; em rodada cujo alvo é o próprio escritório, tire o termo correspondente do padrão.
   Quando aparecer um caso novo, amplie aqui em vez de confiar no olho.
4. **Perfil duvidoso pula e vai para o consultor.** Perfil sem nome com foto que não bate com o
   lead — no caso de campo, foto de mulher no número de um "Dr." — não recebe a abertura: pular,
   registrar o motivo e listar para o consultor no fechamento. Quem decide se envia é ele.

**O botão de enviar muda de nome.** Já foi `span[data-icon="wds-ic-send-filled"]`; depois nenhum
`data-icon` existia no rodapé e o que funcionou foi `button[aria-label="Send"]`. Se o bloco abortar
com "botão não encontrado", listar os `aria-label` dos botões do `footer` antes de qualquer outra
coisa.

**Nenhum script pode passar de 45 segundos.** A extensão corta a execução em 45 s e devolve erro de
tempo esgotado, **mas o script continua rodando na página** — em campo, uma espera de 56 s "falhou"
e o envio saiu assim mesmo. Por isso a espera do intervalo é feita em pedaços de até 38 s, cada um
numa chamada, e o envio só vai num bloco cuja espera restante já é curta. Depois de um tempo
esgotado, **conferir o fio antes de repetir**: o envio pode já ter saído.

**"WhatsApp is open in another window"** quer dizer que o consultor abriu o WhatsApp em outro
lugar. Não clicar em *Use here* sem perguntar: isso derruba a sessão dele.

**E confira a saudação antes de abrir a rodada.** A saudação entra **gravada em cada mensagem** da
fila. Fila montada de manhã e disparada à tarde manda "bom dia" às 17h — já aconteceu, e foi preciso
editar a mensagem já enviada. Regerar a fila ou reescrever o campo `msg` antes do primeiro disparo.

### 4. Depois de cada disparo

1. **Salvar o contato** pelo cabeçalho do chat → Add → **nome da pessoa no campo "nome"; razão
   social + endereço no campo "sobrenome"** — é no próprio WhatsApp que o consultor vai saber com
   quem fala caso a pessoa responda.
2. **Abertura não leva etiqueta.** Quem só recebeu a abertura já está no log e no CRM; a lista do
   WhatsApp repetia isso e esgotou o limite de listas. As listas passam a dizer **a próxima ação do
   consultor dentro do WhatsApp**, não a origem do contato: *Responder* (conversa viva — a última
   mensagem é do lead), *Agendar*, *Reunião marcada*, *Negociação*, *Cliente*, *Morno*,
   *Indicação* e *Não chamar* (SAIR, recusa firme, número errado). A conversa entra numa lista
   quando muda de ação, e sai da anterior.
   Ao etiquetar, **isole a conversa pela busca antes do clique direito.** A lista de conversas se
   reordena sozinha a cada mensagem que chega — de qualquer contato, não só dos leads da rodada — e
   a linha que estava na posição certa no screenshot já é outra no instante do clique. Já aconteceu de o
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

### 4.1 O toque com link — abertura e estrutura

- **A abertura é "Obrigado pela atenção".** Ela serve a quem respondeu, seja para dizer que vai
  olhar, seja para recusar. **"Obrigado por ficar de olho" está proibida** — foi recusada em campo.
- **A mensagem é sempre customizada.** Não existe texto padrão para o toque com link; o que se
  repete é a estrutura de três partes:
  1. **agradecimento curto** pela atenção;
  2. **o link de rastreio** (`scripts/link-rastreio.py`), apresentado como a página para a pessoa
     conhecer o trabalho — nunca como material comercial;
  3. **um gancho tirado do que ela mesma disse**, ou do que o consultor falou no áudio para ela.
- **O gancho é o que muda em cada uma**, e é ele que faz a mensagem não parecer disparo. Em campo:
  para quem ficou de analisar, virou uma pergunta de qualificação; para quem recusou dizendo
  "outra oportunidade", virou a oferta de estar à disposição quando fizer sentido.
- **Sem número e sem pitch** neste toque.

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

### 6. Fechar no CRM — a rodada não acaba antes disto

> **Regra:** a rodada de ativação não termina sem o registro no CRM — fazer pela metade é o mesmo
> que não fazer.

O gatilho foi real: em dois dias seguidos a rodada foi executada, o log escrito, os contatos salvos
e as conversas etiquetadas — e **nada entrou no CRM**. Os dois dias de placar saíram como FALHA e a
carga virou dívida.

**O que fecha a rodada, na ordem:**

1. **Card para cada ativado** — por planilha, quando forem muitos, ou lead avulso. Para quem usa o
   CRM Apollo, a mecânica é da skill **`crm-apollo`**, e é ela que se invoca aqui; o que muda é que
   **chamá-la faz parte desta rodada**, não é um passo opcional que fica para depois. Quem usa outro
   CRM faz a carga nele, na mesma rodada.
2. **Registro da ação** em cada card, com o que foi dito.
3. **Print do dia** com o filtro fechado na data, e o JSON da contagem — sem ele o placar do dia
   sai marcado FALHA.
4. Só então o fechamento curto da Saída esperada.

**Se faltar tempo ou a sessão do CRM cair**, isso não vira silêncio: a rodada é reportada como
**incompleta**, com o que ficou pendente escrito em `dados/crm-pendencias.md`, e o consultor decide
se fecha depois ou no dia seguinte.

## Saída esperada

Ao fim da rodada, um fechamento curto: **quantos ativados** · **quem foi pulado e por quê** (número
indisponível, contato divergente, responsável pessoa jurídica, perfil duvidoso) · **o caminho do
log** em `dados/` · e o **estado da carga no CRM**: feita, ou pendente com o que falta.

## Limites

- **Não dar a rodada por encerrada sem o CRM** — carga, registro da ação e print são parte dela
  (Passos, 6). Rodada pela metade conta como rodada não feita.
- **Não dar a rodada por encerrada sem contato salvo** — feito na mesma rodada do disparo (Passos,
  4), junto com log e CRM; não fica para depois. A abertura não leva etiqueta (Passos, 4). A única
  exceção é o lead cuja conversa está como não lida (Passos, 2.0), que é reportado como pendente.
- **Não abrir conversa que esteja como não lida** — a continuidade da resposta do cliente é do
  consultor; a sessão só avisa quem respondeu (Passos, 2.0).
- **Não enviar mensagem sobre suposição de contexto** — sem saber quem é o interlocutor,
  pergunta-se antes (Passos, 2.1).
- **Não enviar texto que o consultor não aprovou** — a fala vai a pessoa real e não tem revisão de
  compliance no caminho.
- **Intervalo mínimo de 70 s, sempre variável** — cadência fixa é o que o WhatsApp penaliza.
- **Teto diário de primeiros contatos: o do doc de cadência.** O agente **não sobe esse número por
  conta própria**: rampa de volume proposta pelo agente já terminou em conta restrita pela Meta.
  Volume só sobe com aval explícito do consultor e depois de aparecer resposta humana.
  **Alerta de suspensão:** no caso de campo que originou esta régua, a conta foi **suspensa** — o
  WhatsApp Web deslogou sozinho no meio de uma onda — depois de cerca de 200 mensagens em cinco dias
  úteis, sem ter caído nos dias em que passou de 50. O teto adotado ali, como referência, foi **40
  mensagens por dia e 200 em cinco dias**; dentro dele, até 30 por dia e 150 em cinco dias entre
  aberturas frias e cobranças (15 primeiros contatos e 15 cobranças por dia). **As mensagens que o
  consultor manda à mão entram na contagem** — o log da rodada não as vê, e o total real da conta é
  maior que o do log. Não há limite publicado pela Meta.
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
