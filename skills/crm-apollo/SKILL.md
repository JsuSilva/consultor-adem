---
name: crm-apollo
description: Opera o CRM Apollo (crmapollo.com.br) pelo Claude in Chrome — importa leads por planilha, registra ação (conversa, ligação, reunião), cria lead avulso e lança proposta com valor, sempre verificando o resultado no pipeline. Só se aplica se administradora.crm.usa_apollo for true na config. Invoque com /crm-apollo quando o consultor quiser carga ou registro no CRM; não dispara sozinha, porque escreve no sistema de produção da carteira.
---

# Skill — `crm-apollo`

> **Esta skill só se aplica se `administradora.crm.usa_apollo` for `true` em
> `config/consultor.json`.** Com `false` ou vazio, ela não roda: o consultor usa outro CRM, e o
> procedimento de tela abaixo não vale para ele.

> A operação do CRM, na mão da sessão principal via Claude in Chrome
> (`mcp__claude-in-chrome__*`, com `browser_batch` para encadear passos). É skill e não agente
> porque precisa da situação de campo, não de fronteira própria — não lê a lista de leads em
> `dados/` além do log da rodada, não roda base de dados, não escreve em `conhecimento/`.
> Procedimento **verificado em campo**, muito dele à custa de erro.
> Sem dado nominal aqui dentro: dado de lead só em `dados/`, fora do Git.

O CRM é o **Apollo**, `crmapollo.com.br` (plataforma AVAPRO). A URL da unidade do consultor vem de
`administradora.crm.url_unidade` na config — nunca a de outra unidade. **Não é o `apollo.io`.** A
sessão fica logada no Chrome do consultor.

## Quando usar

Quando o consultor pede carga ou registro no CRM. Seis operações:

1. **importar leads** por planilha;
2. **registrar ação** — conversa, ligação ou reunião — num card, e **corrigir registro já gravado**;
3. **criar lead avulso**;
4. **lançar proposta com valor**;
5. **fechar o dia para o placar** — filtro do dia, print e contagem (Passos, 7);
6. **executar o contrato da skill `follow-up`** — o próximo passo de cada lead, no mecanismo certo
   (Passos, 8).

Duas skills irmãs alimentam esta: a **`whatsapp-web`** produz a fila e o log que viram
importação e registro de conversa; a **`follow-up`** decide o próximo passo e entrega o contrato de
seis campos. **Esta skill é a única dona da mecânica do Apollo** — seletor, armadilha de modal e
sequência de clique moram aqui e em lugar nenhum mais. Quem precisa escrever no CRM delega para cá,
em vez de copiar o procedimento.

## Entradas

- a operação pedida e **quais leads** — nomes, telefones, ou o log da rodada em `dados/`;
- para registro de ação: **o que aconteceu, quando e o texto do memo**;
- para proposta: **tipo de consórcio, grupo, crédito, plano de venda e estado da negociação** —
  os cinco vêm do consultor, a skill não escolhe nenhum (ver Limites).

## As telas

Os caminhos abaixo são relativos à URL da unidade (`administradora.crm.url_unidade`).

- **Pipeline**: `app/views/pipeline/index.php`. Colunas, nesta ordem:
  **Leads · Em ligação · Agendado · Reuniões · Negociações · Clientes · Removidos**. Há filtro de
  período no topo (Início/Fim) que muda o que aparece — conferir antes de concluir que um card
  sumiu.
- **Importação**: `app/views/clientes/importacao.php`.
- **Leads**: `app/views/clientes/indexLeads.php`.

## A regra central do funil

**O card não muda de coluna por arrastar.** Arrastar, "mover para coluna" e seleção múltipla não
funcionam. **O funil move quando se registra uma ação no card.** O registro de ligação vale também para a conversa no WhatsApp.

**"Ligação" leia-se "conversa"** — telefonema, áudio e WhatsApp entram no mesmo botão 📞; o contador
mede contatos feitos, não chamadas.

Botões do card, identificados pelo atributo `title`:

| `title` do botão | O que faz | Para onde move |
|---|---|---|
| "Agende ou adicione uma ligação ou conversa" | abre `#modal-log`, tipo `L` | registro simples → **Em ligação**; com `#agendar` marcado e data futura → **Agendado** |
| "Agende ou adicione uma reunião já realizada" | mesmo modal, tipo `R` | reunião **agendada** (futura) → **Agendado**; reunião **já realizada** (data passada) → **não move** |
| "Adicione um comentário ou follow-up com lembrete futuro" | o **balão amarelo**, terceiro ícone do card; abre `#modal-comentarios` | — |
| "Classifique seu lead com etiquetas…" | o botão Classificar | — |
| "Negociações" | abre `#modal-propostas` | ver Proposta |
| "Acesse o Simulador direto para este cliente" | simulador do cliente | — |

**A coluna "Reuniões" nunca recebe ninguém** nesta configuração: reunião agendada vai para Agendado,
reunião realizada não move.

**A exceção à regra do funil é *Removidos*, e ela funciona** (verificada em campo). No menu
suspenso do card — o que abre pelo nome do lead — existe o item **"Coluna de removidos"**, classe
`.remover_pipeline`, com `id_cliente` próprio. Clicar abre a confirmação *"Deseja mover este lead
para a coluna de Removidos? Você pode reverter isso no cadastro do cliente"* e o card vai para
*Removidos* **sem precisar de ação registrada**, preservando as ligações que já tinha. É o caminho
para lead que recusou. Não confundir com o "Enviar para coluna" do topo do pipeline, que continua
não funcionando.

**Etiquetas — o "Salvar que não persiste" era método, não bug.** Os três
campos do Classificar são inputs de texto livre: `#flag1`, `#flag2`, `#flag3`. Preencher por
JavaScript deixa o texto na tela e **o Salvar grava o valor antigo**. O que funciona é digitação
real: clicar no campo, `cmd+a`, `Delete`, digitar a etiqueta pelo teclado, então Salvar. Sempre
recarregar e conferir no card. Campo pode ficar vazio, mas etiqueta contraditória confunde — ao
trocar um estágio, apague o antigo em vez de acrescentar ao lado.

## Passos

### 1. Registrar ação (`#modal-log`)

Campos: `#data_hora_log` (datetime-local) · `#agendar` (checkbox) · `#memo_log` (textarea) ·
`#id_destinatario` (convidados) · botão `#add_log` (atributo `tipo`: `L` ligação, `R` reunião).

**Armadilha verificada: `#add_log` fica invisível até haver digitação real de teclado no textarea.**
Preencher o memo por JavaScript não revela o botão. O caminho que funciona:

1. preencher `#data_hora_log` e `#memo_log` por JS;
2. **clicar no textarea e digitar um caractere de verdade** (um espaço);
3. o botão aparece — então clicar.

**Exceção, verificada em campo:** quando o modal abre com `#agendar` **já marcado**, o
`#add_log` continua com `display:none` mesmo depois de digitação real — inclusive apagando o campo
e redigitando o memo inteiro pelo teclado. Nesse caso o que grava é chamar `click()` por JavaScript
no botão oculto. Confirme sempre pelo contador do card depois de recarregar: é a única prova.

**Apagar um registro já gravado** (apagar registro exige pedido explícito do consultor, ver
Limites). O próprio `#modal-log` lista os registros do card numa tabela;
cada linha traz um `a.apagar_log` com o atributo **`id_apagar_log`** daquele log. Clicar abre a
confirmação *"Tem certeza que deseja apagar? Você não poderá reverter isso posteriormente!"* →
"Sim, apagar!". A tabela **não se atualiza sozinha**: feche e reabra o modal, ou recarregue o
pipeline e olhe o contador do card. Ao limpar duplicata, **só apague quando a tabela mostrar
exatamente o número de registros que você espera** — conferir antes é o que impede apagar o único
registro que existia.

### 2. Criar lead avulso

Botão `#novo-lead` → `#modal-novo-lead`. Obrigatórios: `#nome`, `#id_origem` (lista fechada:
Indicação, Lista fria, Network, Whatsapp, Telefonema, Já é cliente etc.) e `#celular`.
O botão `#adicionar-novo-lead` nasce com `display:none` e só aparece quando o celular é validado —
surge a confirmação **"Celular único, liberado!"**.

**Armadilha verificada: a máscara do celular exige 11 dígitos e embaralha a digitação rápida** —
digitar os dez primeiros dígitos em sequência rápida devolveu o DDD e o número trocados de posição. Dois caminhos funcionam:

1. setar os **10 primeiros dígitos por JS, um a um**, disparando `input` e `keyup` a cada dígito;
   clicar no campo, teclar **End**, digitar **o último dígito pelo teclado real**;
2. mais curto e mais confiável quando o clique não acerta o campo: setar **os 11 dígitos por JS** e
   então pressionar **uma tecla real que não altera o texto** (`shift` serve). O `keyup` de verdade
   é o que dispara a validação; a confirmação "Celular único, liberado!" aparece e o botão surge.

O número vindo do WhatsApp pode aparecer **sem o nono dígito** (`+55 DD NNNN-NNNN`). Antes de
cadastrar, confirme abrindo `web.whatsapp.com/send?phone=55<11 dígitos>`: se cair no mesmo chat, o
número com o 9 é o certo. Nada é enviado nessa checagem.

#### Lead que chegou por indicação — ligar o indicado ao indicador

Verificado em campo, com indicados salvos e o vínculo conferido no pipeline.

1. **O indicador tem de existir como lead antes.** O campo de indicação só aceita quem já está no
   CRM. Se ele não existir, cadastre-o primeiro — com a origem da relação real dele com o
   consultor (rede quente é *Network*, não *Indicação*) — e só depois o indicado.
2. **Conferir duplicata do indicador e do indicado sem usar a tela.** O endpoint da busca responde
   direto, com a sessão do navegador:
   ```js
   await fetch('../../common/pesquisarClientePorNome.php?term=' + encodeURIComponent('<sobrenome>'),
               {credentials: 'include'}).then(r => r.text())
   // → [{"id":"<id>","nome":"<NOME>","text":"<NOME> +55(DD) NNNNN-NNNN"}]
   // corpo vazio = nenhum resultado. Mínimo de 4 caracteres.
   ```
   Busque pelo sobrenome e por um pedaço do telefone, não só pelo primeiro nome — um primeiro nome comum
   devolve homônimos que não têm nada a ver.
3. **No `#modal-novo-lead`:** `#nome`, `#id_origem` = **7 (Indicação)** — conferir na sua unidade: o id interno pode variar —, e o campo
   **`#id_cliente_indicacao`** ("Clientes de indicação"), que é um select2 com busca por ajax.
   **Não use a caixa de busca do select2 por script:** em aba de segundo plano o atraso interno dele
   é estrangulado pelo Chrome e a busca não volta. Preencha com o `id` e o `text` que o endpoint
   devolveu:
   ```js
   const $s = $('#id_cliente_indicacao');
   $s.empty();
   $s.append(new Option('<text devolvido>', '<id devolvido>', true, true)).trigger('change');
   ```
4. **Armadilha: mexer no select2 tira o foco do celular**, e a primeira tecla real não valida o
   número — o botão `#adicionar-novo-lead` não aparece. Zere o `#celular`, sete de novo os 11
   dígitos, dê `focus()` e tecle `shift` outra vez: aí vem *"Celular único, liberado!"*.
5. **Só clique em `#adicionar-novo-lead` se `$('#id_cliente_indicacao').val()` for o id esperado.**
6. **A prova é o card:** recarregado o pipeline, o card do indicado mostra **o nome do indicador
   logo abaixo do nome dele**. Sem essa linha, o vínculo não gravou.

### 3. Lançar proposta (`#modal-propostas` → "Nova proposta" → form `#form-modal-vendas`)

Cadeia de selects **dependentes**, nesta ordem obrigatória:

1. `#id_tipo_consorcio` — Consórcio de Imóveis / de Veículos / de Serviços / de Outros Bens Móveis;
2. `#grupo` — carrega depois do tipo; são dezenas a centenas de grupos;
3. `#valor_vendido` — é o **Crédito**, e **é um select, não campo livre**: só existem as cartas
   daquele grupo;
4. `#id_loja` — a unidade do consultor (`administradora.unidade`);
5. `#id_plano_venda` — também dependente; num grupo de imóveis vieram 16 planos, **todos variando
   comissão**.

Radios de estado: `estado_negociacao_n` = Em negociação (marcado por padrão) · `_p` = Possível
fechamento · `_f` = Fechamento cancelado. Salvar é o `input[type=submit]` do form.

**Mecânica:** disparar cada carregamento com jQuery — `jQuery(sel).val(v).trigger('change')` — e
**esperar de 5 a 9 segundos entre um select e o próximo**. Ao casar o texto do crédito,
**normalizar espaços**: `R$ 72.000,00` pode vir com espaço não-quebrável.

**A proposta manda na coluna.** Assim que existe proposta, o card vai para **Negociações**, e
nenhuma ação posterior — nem reunião registrada, nem ligação — o tira de lá. Consequência prática, e
é para dizer com todas as letras ao consultor: **no Apollo não dá para ter valor e escolher a coluna ao
mesmo tempo.** Se ele quiser o card em outra coluna, a proposta não pode existir ainda.

### 4. O feedback da reunião vai no balão amarelo

Os três ícones do card têm papéis distintos, e trocá-los faz o histórico mentir:

- **telefone azul** — o contato aconteceu: ligação, áudio, conversa de WhatsApp. É o que move para
  *Em ligação*;
- **agenda verde** — a reunião em si: quando foi ou quando será;
- **balão amarelo** — **o feedback do que saiu dali**: o que o cliente disse, o que ficou pendente,
  qual o próximo passo. É onde se registra o desdobramento depois da reunião ou da ligação.

Por que separado: o balão **não move o card de coluna**. Um lead com reunião marcada para hoje
continua em *Agendado* depois do comentário — é assim que o registro do dia da reunião entra sem
tirar o card da coluna. Registrar o mesmo texto como ligação teria movido o card e escondido a
reunião do dia.

**O balão amarelo cria tarefa na agenda Google do consultor** (verificado em campo). Dentro do
`#modal-comentarios`: `#memo_comentario` recebe o texto, a caixa **`#gerar_lembrete`** revela
**`#data_lembrete`** (datetime-local) e **`#id_usuario_atribuido`** escolhe o dono; o botão é
**`#addComentario`**. A confirmação é literal — *"Lembrete adicionado no CRM e em sua agenda
Google!"*. **É este o caminho de "tarefa para mim na agenda"** quando o próximo passo é do consultor,
porque cria o compromisso sem mover o card de coluna. O `#agendar` do `#modal-log` também escreve na
agenda Google, mas **move o card** — por isso é só para passo que envolve o cliente.

**Reunião futura já move o card sem `#agendar`** (verificado em campo): lançar no botão de
reunião (`[id_visitas_reunioes]`) com `#data_hora_log` no futuro e `#agendar` **desmarcado** leva o
card para *Agendado* e **não cria evento na agenda Google**. Use esse caminho quando o próprio consultor
já mandou o convite da reunião pelo calendário — marcar `#agendar` por cima duplica o compromisso na
agenda dele.

Cuidado com o texto: esse modal recusa mais caracteres que os outros (ver Mecânica de clique).

### 5. Apagar proposta ou registro

Só quando o consultor pedir — é irreversível, e o próprio CRM avisa "Você não poderá reverter isso
posteriormente". Caso típico: registro lançado no card errado, que precisa ser recriado no card
certo. **Recrie primeiro no destino, apague depois**; se a ordem inverter e algo falhar, o dado
some.

**Clique por coordenada não funciona aqui.** Nem no "Apagar" da lista, nem no diálogo de
confirmação. O que grava:

1. `click()` por JavaScript no elemento cujo texto é "Apagar";
2. `click()` por JavaScript em `.swal2-confirm` (o botão "Sim, apagar!" do diálogo);
3. recarregar e conferir o contador do card — sem isso não há prova.

### 6. Importar por planilha

`importacao.php` aceita **XLSX** com as colunas `nome, celular, classificacao, obs`:

- `celular` com 10 ou 11 dígitos;
- `classificacao` no máximo **90 caracteres**, etiquetas separadas por `;` — padrão usado:
  `<Segmento>;Abordagem 1;Sem Resposta`;
- `obs` no máximo **1000 caracteres**.

O ambiente **não tem openpyxl** — a planilha é montada com `zipfile` e inline strings. Para isso
existe `scripts/crm-xlsx.py`.

### 7. Fechar o dia para o placar

O placar diário **sai com o print do CRM anexado**, e sai marcado como **falha** quando a rodada
não fecha — é o aviso de que ficou algo pendente. O horário do placar está em
`operacao.placar.horario` na config: o print tem o dia inteiro para ser batido, mas tem de estar no
lugar antes desse horário.

Ao terminar a carga e os registros do dia:

1. **Deixar o pipeline no filtro do dia** — `Início` e `Fim` na mesma data e, obrigatoriamente, o
   botão **"Forçar filtro entre as datas" em "Sim"**. Com ele em "Não" as datas não valem e a
   coluna mostra o período inteiro. Depois clicar em **Pesquisar**.
2. **O print é da skill, e sai sem roubar o foco do consultor.** Capturar a
   tela inteira falha na prática: se ele estiver digitando em outro app, o `screencapture` pega a
   janela errada, e forçar o Chrome para a frente atrapalha quem está trabalhando. O caminho certo é
   **capturar a janela do Chrome pelo id**, que funciona com a janela atrás de tudo:
   ```bash
   # 1. selecionar a aba do pipeline sem trazer o Chrome para a frente
   osascript -e 'tell application "Google Chrome" to repeat with w in windows' \
             -e 'set i to 0' -e 'repeat with t in tabs of w' -e 'set i to i + 1' \
             -e 'if URL of t contains "pipeline/index.php" then set active tab index of w to i' \
             -e 'end repeat' -e 'end repeat'
   # 2. descobrir o id da janela (CGWindowID) com um swift de três linhas, e capturar
   screencapture -x -o -l <CGWindowID> placar-crm-AAAA-MM-DD.png
   ```
   O `-l` captura **aquela janela**, composta, mesmo em segundo plano; o `-o` tira a sombra.
   **Armadilha verificada em campo: o consultor costuma ter a própria aba do CRM aberta na mesma
   janela.** Selecionar "a aba cuja URL contém `crmapollo`" pega a dele — sem filtro do dia — e o
   print sai errado. O jeito seguro: marcar a aba de trabalho pelo título
   (`document.title = 'CRM Apollo - PRINT-DO-DIA'`), selecionar no AppleScript pela aba cujo
   `title` contém essa marca, **guardar o `active tab index` que estava antes**, capturar, e
   **devolver a aba que ele estava usando** e o título original logo em seguida. Salvar
   em `dados/placar-crm-AAAA-MM-DD.png` e **abrir o arquivo para conferir** que
   é o pipeline com o filtro do dia, e não outro app. A permissão de Gravação de Tela continua sendo
   do binário aninhado `~/Library/Application Support/Claude/claude-code/<versão>/claude.app`, e o
   caminho muda a cada atualização do Claude Code.
3. **A skill grava a contagem** em `dados/placar-crm-AAAA-MM-DD.json`:
   ```json
   {"ligacoes_no_dia": 30, "ativos_do_dia": 30, "filtro": "..."}
   ```
4. **O que é "bater".** A definição de partida é que a contagem de ativos no dia precisa ser
   igual à de ligações registradas no dia no print, comparando **os leads criados no dia**. Na prática isso quebra, porque o recorte do pipeline não
   é só de criação. **A comparação vale sobre os registros criados no dia**, não sobre os cards que
   o filtro mostra: conte quantas ações você lançou hoje e confronte com os ativos do dia. Card que
   aparece no recorte por agendamento antigo **não entra na conta** — e, se aparecer, o certo é
   abrir e conferir a data dos registros dele antes de concluir qualquer coisa.
5. **Atenção ao dia de recuperação:** o filtro do pipeline agrupa pelo **dia em que o registro foi
   feito**, não pela data digitada no memo. Num dia de recuperação, a coluna com o filtro do dia
   mostrou a rodada somada à leva de dois dias anteriores, que só entrou no CRM naquele dia. Por
   isso a contagem do JSON é a da rodada, não a da coluna.
6. **O "Forçar filtro entre as datas" não recorta só criação — pega agendamento e movimentação do
   dia** (verificado em campo). Um card criado semanas antes apareceu no recorte do dia porque
   tinha uma reunião gravada com data daquele dia. **Antes de concluir que a contagem não bate,
   abra os cards estranhos ao recorte e olhe a data dos registros deles**: card antigo com
   agendamento para hoje é comportamento normal do filtro, não erro da carga. No caso verificado a
   causa era mais simples e pior — a data da reunião tinha sido lançada com um dia de erro; corrigida
   a data, o card saiu do recorte e a contagem passou a bater sozinha.

Quem lê isso é `scripts/placar-dia.py`: sem PNG, ou sem o JSON, ou com contagem diferente, o assunto
do e-mail vira **`FALHA no placar — DD/MM/AAAA`** e o corpo diz o que faltou. Os números do placar
continuam saindo, porque vêm do CSV de ativações e do calendário.

### 8. Receber o contrato da skill `follow-up`

A `follow-up` decide **o quê**; esta skill sabe **como escrever**. Ela entrega, por lead, seis campos
— `{ lead, ação, data, dono, mecanismo, memo }` — e nada mais. É o mesmo padrão em que a `comparativo-credito` pede a conta ao `calculista`.

**O `mecanismo` diz onde o passo é gravado, e são coisas diferentes:**

| `mecanismo` | Quando a `follow-up` manda | O que esta skill faz | Efeito no funil |
|---|---|---|---|
| `agendar` | o próximo passo **envolve o cliente** — ligação, reunião, retorno marcado | `#modal-log` com **`#agendar` marcado** e `#data_hora_log` no futuro | card vai para **Agendado** |
| `comentário` | o próximo passo é **só do consultor** — mandar material, ouvir áudio, levantar número | balão amarelo (`#modal-comentarios`), com lembrete na data | **não move o card** |

Razão da separação: **card não pode estar em *Agendado* por causa de dever de casa do
consultor**, senão o funil mente sobre quantos compromissos existem de verdade.

**O `memo` chega pronto** — texto corrido, sem acento, começando em `QIP.` e com os campos na ordem
QUEM é / QUEM será / IMPEDIMENTO do cliente / IMPEDIMENTO do consultor / PROXIMO PASSO / ESTAGIO.
Esta skill **não reescreve o memo** e não preenche campo que a `follow-up` deixou como `nao informado`.

**Corrigir um memo já gravado** é `[id_editar_log]` na linha da tabela do `#modal-log`: o clique
carrega o registro no próprio formulário, o botão que salva passa a ser **`#editar_log`** (não o
`#add_log`), e a confirmação é *"Visita/reunião atualizada com sucesso"*. **A data permanece a que
estava** se você não mexer nela — confira antes de salvar. Editar é o caminho certo para trocar
texto ou consertar data; apagar e relançar perde o histórico.

**Erro no histórico se corrige, não se narra.** O histórico do CRM não pode virar uma conversa sem
pé nem cabeça, com uma presunção errada registrada e depois outra linha dizendo que não era aquilo.
O que for erro precisa ser editado ou apagado para não gerar confusão. O memo é o histórico **do cliente**, não o
diário do agente: nada de "eu tinha presumido X, mas na verdade é Y", nada de anotação sobre a
própria correção. Registro errado se **edita** até ficar só com o fato, ou se **apaga** e se relança
limpo. O que explica a correção vai para a resposta ao consultor, nunca para o card.

**O comentário do balão amarelo não aceita edição por script** — o `#atualizarComentario` recusa com
*"Selecione uma data para o lembrete!"* mesmo com `#gerar_lembrete` marcado e `#data_lembrete`
preenchido por JS. Para corrigir um comentário: **apagar pelo `[id_apagar_comentario]`** (a
confirmação é a mesma "Sim, apagar!", e o atributo `id_apagar_google_event` no mesmo botão indica que
o evento da agenda vai junto) **e lançar de novo** com `#addComentario`. Registro de ligação e de
reunião, esses sim, se editam por `[id_editar_log]`.

**A tabela do `#modal-log` é servida de um cache e engana** (confirmado em campo): depois de
gravar num card, abrir o modal de **outro** card pode mostrar as linhas do card anterior. Duas vezes
seguidas isso produziu leitura errada — uma tarefa apareceu como se estivesse no card errado, e uma
edição devolveu "linha não achada" num card que tinha a linha. **Antes de ler ou editar linha de um
card diferente do último em que você escreveu, recarregue a página.** Confiar na tabela sem recarregar
é como concluir sobre o pipeline sem recarregar: o CRM mostra o que já tinha em mãos.

## Mecânica de clique — o que evita retrabalho

- **Medir a posição do elemento com `javascript_tool` no instante anterior ao clique** e converter
  CSS → tela. **O fator não é constante: calcule-o na hora**, com `largura_do_frame_do_screenshot /
  window.innerWidth` — já apareceu 0,81667 (frame 1568) e 0,7875 (frame 1512) na mesma operação, e
  usar o fator velho erra o alvo por dezenas de pixels. Screenshot envelhece; coordenada
  reaproveitada de outro card foi a causa de registros que pareciam salvos e não estavam.
- **Modal cujo título ocupa duas linhas empurra os campos para baixo** — nome longo de razão social
  faz isso. Quando a medição por JS divergir do que o screenshot mostra, **confie no screenshot**.
- **Converter do screenshot para o frame de clique**: divida a largura do frame que o resultado
  declara pela largura da imagem devolvida. Um screenshot pedido em `scale: 0.5` já voltou como
  imagem de 1008 px para um frame de 1512 — fator **1,5**, não 2. Errar isso põe o clique dezenas de
  pixels fora, e o sintoma é o alvo "não responder".
- **Card fora da viewport**: `scrollIntoView({block:'center'})` antes de medir e clicar.
- **Conferir a aba antes de cada escrita**: `tabs_context`, a URL, e **o nome do lead no título do
  modal**. Houve erro real de registrar no WhatsApp acreditando estar no CRM: muito cuidado para trabalhar
  na aba certa, no sistema correto.
- **Verificar depois**: recarregar o pipeline e conferir **os contadores das colunas** e **os
  contadores do próprio card** (ligações / reuniões / comentários). Só isso prova que salvou.
- **Campos de texto do CRM engolem a barra `/`** — escrever datas como "03 de setembro" e horas
  como "16h21". O modal de comentário é mais estrito e devolve "Alguns caracteres especiais não são
  permitidos": os dois-pontos foram recusados. Escreva em prosa simples, sem pontuação decorativa.
- **O CRM não é filtro confiável de "já contatei essa pessoa"**: buscar por telefone devolveu zero
  para quem havia sido abordado dias antes. Quem confirma é o histórico do WhatsApp.

## Saída esperada

Fechamento curto: **o que foi registrado** (leads, ações, propostas, com o card de cada um) · **a
contagem das colunas antes e depois** · **o que ficou pendente ou quebrado**, com a linha
correspondente gravada em `dados/crm-pendencias.md`.

## Limites

- **Não escolher tipo de consórcio, grupo, crédito, plano de venda nem estado da negociação.** São
  decisões comerciais do consultor — **mudam comissão e prazo**. Perguntar sempre (Regra nº 1 do
  `AGENTS.md`).
- **Não apagar proposta, lead ou registro** sem pedido explícito.
- **Nenhum dado nominal em arquivo versionado:** planilhas e logs só em `dados/`.
- **Registrar o que quebrou** em `dados/crm-pendencias.md` — pendência não
  anotada volta como retrabalho.
- **Não dar por salvo o que não foi verificado no pipeline recarregado.**
- **Aba que degrada, aba nova.** Depois de muitos recarregamentos seguidos, o pipeline entra num
  estado em que nenhum modal abre e o screenshot devolve "Script injection timed out" — em qualquer
  card, não só no que falhou. Não insista nem conclua que o card está quebrado: feche a aba, abra
  outra e refaça o filtro de período.
- **Modal que para de abrir no meio do lote é aba em segundo plano, não saturação do CRM**
  (recarregar parece resolver, mas resolve por acidente, porque limpa o popup preso).
  Depois de cada registro o CRM mostra um SweetAlert *"Ligação adicionada com sucesso"*. Se a aba
  está em segundo plano, o Chrome congela a animação de fechamento: o popup fica com a classe
  `swal2-hide` e **nunca é removido**, e o `.swal2-container` — `z-index: 1060`, `pointer-events:
  auto`, cobrindo a viewport inteira — engole o clique seguinte. O card parece quebrado e não está.
  Sintomas colaterais: `document.body` fica com `swal2-shown` e sobra um `.modal-backdrop` órfão sem
  o `modal-open` correspondente.
  **O que fazer:** trazer a aba do CRM para a frente antes do lote —
  `osascript -e 'tell application "Google Chrome" to activate'` e ativar a aba do pipeline — e
  conferir `document.visibilityState === 'visible'`. Com a aba visível o popup fecha sozinho e cada
  registro leva cerca de 3 segundos. **Não arrancar o `.swal2-container` por JS**: já foi tentado, e
  deixa o Bootstrap e o SweetAlert em estado inconsistente, aí nenhum modal abre mesmo.
  Vale limpar `.modal-backdrop` órfão entre um card e outro, só quando o `body` não tem `modal-open`.
- **O `Swal.close()` não resolve, nem Escape, nem clique no confirm** — nessa tela o popup de sucesso
  não tem botão visível (`.swal2-confirm` fica com `display: none`) e o fechamento depende do
  `animationend`, que não dispara em aba oculta. A trava é de renderização, não de API.
- **Rodada em lote continua se fazendo em blocos**, e o lote sempre relê no pipeline recarregado quem
  já está feito, em vez de confiar no contador do próprio laço.
