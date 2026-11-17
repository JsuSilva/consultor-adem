---
name: roteirista
description: Escreve a fala a partir da necessidade e do canal — primeiro contato, mensagem de ponte, retomada de lead frio, resposta a objeção, pauta de reunião, pedido de indicação, para qualquer público. Invoque com /roteirista quando quiser a peça; não dispara sozinha, porque produz fala que vai a cliente.
---

# Skill — `roteirista`

> A fala, para quem quer que seja. É skill, não agente: precisa da situação de venda, não de
> fronteira própria. Sem dado de cliente aqui dentro.

## Quando usar

Converter uma necessidade em conversa: primeiro contato, mensagem de ponte, retomada de lead frio,
resposta a objeção, pauta de reunião, texto de pedido de indicação — **para qualquer pessoa**.
A doméstica que quer sair do aluguel, a cabeleireira que quer a própria sala, o motorista que troca
de carro, a transportadora que renova frota, o casal da primeira casa, o empresário que pensa em
sucessão. O roteiro nasce da **necessidade e do canal**, não do cargo — muda a linguagem, o tamanho
e a prova; o método não muda.

## Entradas (briefing mínimo)

- quem é e o que se sabe — a ficha do `diagnostico-de-lead`, quando existir;
- a **necessidade ou o gatilho observado** — **sem isso a skill não escreve roteiro: devolve as
  perguntas de descoberta**;
- o canal, e o grau de intimidade (frio, indicado, conhecido);
- **o público declarado** — a mesma frase é certa para um público e destrutiva para outro:
  o corte tributário é revelação para o dono e primeiro dia de faculdade para o contador;
- os números já calculados pelo `calculista`, **com linha e origem declaradas**;
- **as provas e o ângulo do consultor** — `consultor.credenciais` em `config/consultor.json` e o que
  o consultor informar sobre a própria trajetória. A skill não atribui ao consultor credencial,
  carteira ou experiência que não esteja ali: prova que ele não tem é a primeira coisa que o
  cliente confere.

## Passos — o método, que não muda por público

1. Abrir pelo **fato observável**, nunca pelo produto.
2. A dor **na linguagem de quem ouve** — um cálculo, dois vocabulários: o sócio no Simples ouve
   *"você paga R$ 12 mil de aluguel e não deduz um centavo"*; a pessoa física ouve *"você paga
   aluguel há seis anos e a casa continua não sendo sua"*.
3. **Um número, não uma tabela** — e o número veio do `calculista`, na linha certa.
4. O **desqualificador dito em voz alta** — dizer onde o consórcio não serve é o que constrói
   credibilidade.
5. Próximo passo **pequeno e concreto**.

**O que se calibra por público** (e não é o método): vocabulário · tamanho — três linhas de WhatsApp
× pauta de 20 minutos · natureza da prova — dinheiro no bolso × dedutibilidade e balanço — e qual
das credenciais do consultor pesa para aquele público · ciclo de decisão — sozinho, com o cônjuge,
com o sócio, com o contador · o ticket, que muda o bem, não o argumento.

## De que altura se fala — postura e subtexto

O método acima diz **o que** entra na fala; esta seção diz **de que altura** ela é dita. A régua
nasceu em campo, depois de um consultor recusar duas versões seguidas da mesma mensagem. Sem ela, a
única régua de tom são os três textos de encerramento do Repertório, todos escritos para amaciar um
não — e quem copia a postura deles para uma mensagem de posicionamento escreve um pedido de esmola.

**A régua tem três estados, e dois deles estão errados:**

1. **A esmola.** Condicional de permissão: *"deixo meu site para o caso de você e o [cargo] querer
   em me conhecer"*. Na palavra do consultor que recusou: *"muito auto-estima baixa, cara, parece que
   tá pedindo esmola"*. O vício é a frase torcer para que o outro tenha vontade. Da mesma família:
   *"se um dia fizer sentido"*, *"caso tenha interesse"*, *"se puder dar uma olhada"*.
2. **O confronto.** A alfinetada promovida a frase própria: *"Trabalho com quem está em crescimento
   ou preparando expansão — é aí que eu entro"*. Anuncia o julgamento antes de ele ser percebido,
   some a aceitação e sobra ataque. Na palavra dele: *"você assume tudo alfinetando diretamente, aí
   passa um pouco do ponto da sutileza"*.
3. **O ponto certo — aceitar alfinetando.** A alfinetada mora **dentro da frase gentil**, nunca numa
   frase própria: *"Deixo o meu site para que você e o [cargo] conheçam o meu trabalho, e me chamem
   quando estiverem em crescimento ou em expansão"*. A superfície é cortesia; a implicação de que
   hoje não estão chega um segundo depois, e chega sozinha.

**Por que o terceiro funciona, no desenho de quem criou a régua:** *"Precisa doer neles me
dispensar, quero que eles respondam 'mas nós estamos em crescimento', e aí eu vire a mesa pra que
agente marque nossa reunião"*. A frase planta uma condição que o interlocutor quer desmentir, e o
desmentido é a abertura. Dizer o julgamento na cara não produz desmentido nenhum — produz silêncio.

**O que isso proíbe, em qualquer fala:**

- **Condicional de permissão.** Não se escreve para o caso de o outro querer; escreve-se para que
  ele conheça.
- **Agradecer por ser dispensado.** Agradece-se a resposta, não a recusa.
- **Reforçar a alfinetada.** Se a frase do consultor já carrega a condição, qualquer linha somada em
  cima estraga — corta-se o acréscimo, não a frase dele.
- **Pedir que o outro queira.** Quem define o critério é o consultor; o critério aparece como
  consequência, não como exigência.

### Quando o SAIR entra, e quando não entra

Na palavra do consultor que fixou a regra: *"o SAIR só entra quando houver um princípio de recusa,
ele entra como necessidade de deixar claro, caso não tenha mantemos sem"*.

**O gatilho é o princípio de recusa, não o tipo de mensagem.** Havendo recusa — mesmo gentil, mesmo
"no momento não" —, o contato fica guardado e a saída precisa estar escrita: é o que a regra do SAIR
(skill `follow-up`) protege. Sem recusa, o SAIR não entra, porque não há nada de que sair.

**Os três casos de campo que fixaram a régua:**

1. **Recusou → entra.** Quem respondeu "não, obrigado", "no momento não temos interesse" ou "não
   tenho recursos agora" recebe o link **e** a linha do SAIR. Um deles respondeu SAIR sete minutos
   depois: a régua funcionou, e o card foi para Removidos.
2. **Está carregando o recado → não entra.** A secretária que se apresentou e **pediu** a mensagem
   para adiantar ao médico recebeu o SAIR por engano, e o consultor mandou tirar: *"ela não precisava
   da opção sair, você leu a conversa?"* A mensagem foi editada dentro dos 15 minutos. Oferecer saída
   a quem está ajudando diz que a conversa acabou.
3. **Nunca respondeu → não entra.** Primeiro contato sem resposta não tem recusa, logo não tem SAIR.

**Erro a não repetir:** tratar o SAIR como item fixo de um modelo. Ele é consequência de uma leitura
do fio — por isso a leitura vem antes, sempre, e por isso o *"você leu a conversa?"* é a pergunta
certa quando ele aparece onde não devia.

**A alfinetada também se calibra pelo fio.** A condição que provoca — *"me chame quando estiver em
crescimento ou em expansão"* — pressupõe alguém que poderia estar e não está. Com quem acabou de
dizer que vive de bolsa de residência, a mesma frase vira deboche; ali a porta do futuro é
literal e sem custo: *"quando a residência virar consultório, me procure"*. Mesma função, mesma
estrutura, dose diferente.

**Como testar antes de enviar:** leia só a superfície. Se soar como cortesia e aceitação, passou o
primeiro filtro. Leia de novo procurando o que a frase presume sobre o interlocutor. Se não presumir
nada, é esmola. Se a presunção estiver escrita com todas as letras, é confronto. Ela tem de estar
**implícita e inevitável**.

## Repertório — textos usados em campo

Textos escritos e enviados em campo por um consultor. Servem de **régua de tom**: leia antes de
escrever fala do mesmo tipo. Nomes de terceiros trocados por colchetes; os dados do consultor
entram como `{consultor.*}` e `{administradora.nome}`, lidos de `config/consultor.json`.

### Encerramento de quem recusou (regra do SAIR, na skill `follow-up`)

**A — recusa vinda por assessora, com elogio e informação antes do aviso.** A pessoa respondeu SAIR
onze minutos depois — a mensagem cumpriu a função de fechar limpo.
```
Claro, dê os parabéns à [Nome], o espaço está muito bonito! Fale pra ela que o momento certo
para o planejamento é com 2 anos de antecedência, isso faz economizar muito e muda uma vida de
patrimônio! Seja para adquirir um veículo, um imóvel ou até outros bens de alto valor! Eu fico a
disposição, caso não queiram mais receber nenhum contato meu, basta responder "SAIR", caso
contrário ficarei com o contato salvo para futuras oportunidades!
```
É a **estrutura vigente**: silêncio mantém, SAIR remove.

**B — recusa direta, nomeando o não.**
```
E sobre o que te falei antes: seu não está respeitado, não vou insistir. Só queria acertar uma
coisa com você. Posso manter seu contato na minha lista, para te avisar caso apareça alguma
condição que faça sentido para a clínica — equipamento, imóvel ou veículo? Se preferir que eu
tire, tiro na hora e não te procuro mais. Me responde só "pode deixar" ou "sair", o que for
melhor pra você.
```
Vale **pelo tom** — "seu não está respeitado, não vou insistir". A mecânica foi superada pela regra
do SAIR: pedir "pode deixar" deixa o silêncio sem autorização.

**C — quem já tem consórcio.** Duas mensagens.
```
Muito obrigado pelo retorno, fico feliz em saber que já usa essa ferramenta! Fazer com que o
consórcio deixe de ser só uma prestação mensal, e vire de fato uma solução é papel do seu
consultor, que deve ter contato ativo! Caso ele não esteja correspondendo e você tiver nova
necessidade, fico a disposição como uma segunda opção, tudo bem?
```
```
Que ótimo, fico a disposição, sou consultor de negócios caso tenha interesse deixo meu site para
que possa me conhecer melhor: {consultor.site}
```
"Segunda opção" **só cabe aqui**. O que se leva para os outros casos é o tom leve e a porta passiva
do site, sem nada a responder.

### Follow-up — cinco opções de repertório

Para o toque de retomada de quem já conversou. **A escolha de qual usar é por caso** — as cinco não
servem para a mesma pessoa.

**F1 · pergunta direta sobre o projeto que já foi falado.** Para quem chegou a nomear o objetivo.
```
{Nome}, uma pergunta rápida:

Você ainda pretende realizar aquele projeto que conversamos ou acabou deixando para depois?

Te pergunto porque estou trabalhando algumas condições essa semana e talvez consiga montar uma
estratégia interessante para você.

Quer que eu veja?
```

**F2 · compromisso antes do cálculo.** Pede o "sim" condicional antes de gastar simulação.
```
{Nome}, lembrei da nossa conversa sobre o {objetivo}.

E vou ser bem objetivo: se eu conseguir estruturar uma opção que faça sentido para você hoje,
você estaria disposto(a) a avançar?

Se sim, eu faço uma simulação e te apresento.
```

**F3 · oportunidade com vaga reservada.** Escassez branda, ancorada na conversa anterior.
```
Olá, tudo bem {Nome}?

Estou passando porque estou com 2 oportunidades disponíveis esta semana para quem quer tirar um
projeto do papel ainda este ano.

Lembrei de você porque já conversamos sobre {assunto}.

Quer que eu reserve uma dessas oportunidades para você e te mostre como ficaria?
```

**F4 · oferta antes de abrir para os outros.** Para rede quente e indicador, onde a deferência vale.
```
{Nome}, vou abrir 2 oportunidades essa semana para clientes que querem comprar, investir ou
realizar um projeto sem precisar descapitalizar de imediato.

Antes de oferecer para outras pessoas, lembrei de você.

Quer que eu te explique?
```

**F5 · cota por desistência, com número.** É a única com valor na mensagem. Crédito, parcela e
reduzida vêm do contrato da cota real, nunca de exemplo.
```
Boa tarde, estou prestando consultoria agora e na gestão de capital estou utilizando o consórcio
como ferramenta em parceria com a {administradora.nome}, abaixo envio uma oportunidade única,
qualquer dúvida estou à disposição.
{consultor.site}

🏘️ OPORTUNIDADE POR DESISTÊNCIA

Tenho 1 vaga disponível em um grupo já em andamento:

💰 Crédito: R$ {crédito da cota}
💳 Parcela: R$ {parcela}
➡️ Reduzida: R$ {parcela reduzida} ({condição da reduzida})

📌 Grupo com {N} contemplações por mês, sendo {M} por lance embutido.

Como surgiu por desistência, tenho apenas 1 vaga disponível.

Quer que eu te passe os detalhes e veja se essa oportunidade faz sentido para você?
```

⚠️ **Ressalva de compliance na F5, e só nela.** A linha *"Grupo com {N} contemplações por mês,
sendo {M} por lance embutido"* é afirmação sobre o ritmo de contemplação do grupo, usada como
argumento de venda. É o terreno que os Limites desta skill fecham: **nenhuma promessa, data ou
probabilidade de contemplação, nem por implicatura**. Duas saídas, e a escolha é do consultor:
1. **manter o número e sustentá-lo** com a ata de assembleia do grupo, dita como histórico passado
   e sem projetar o futuro — *"nas últimas assembleias o grupo contemplou {N} por mês"*;
2. **cortar a linha** e deixar a mensagem com crédito, parcela e a vaga por desistência, que já são
   fatos verificáveis do contrato.
Crédito, parcela e reduzida **saem como estão**: são número de contrato, não previsão.

## Saída esperada

O roteiro no formato do canal · o próximo passo explícito · o bloco de origem dos números (linha e
fonte) · o carimbo **⚠️ não revisado por compliance** — obrigatório enquanto nenhum revisor passar a
peça pelo checklist de `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`. O
carimbo não corrige a fala: roteiro é lido para ser dito, e o que não pode ser dito não entra,
carimbo ou não.

## Limites

- **Não gera número.** Cálculo de produto é do `calculista`; sem número calculado, o roteiro usa o
  gatilho e a pergunta — não inventa.
- **Não inventa prova.** Credencial, carteira, tempo de casa e caso de cliente só entram se estiverem
  em `consultor.credenciais` ou forem informados pelo consultor. **Sem credencial em
  `consultor.credenciais`, a frase "sou …" sai inteira** — nunca fica placeholder que possa chegar
  literal ao cliente.
- **Horário proposto ao cliente é `[dia] às [hora]`**, preenchido pelo consultor — nunca dia e hora
  fixos no texto.
- **Compliance se lê pela semântica, não pela palavra.** O que o documento de compliance veda
  (`conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`, Regras 1.1 e 1.2) é
  **dizer que o consórcio é investimento** — chamar a cota de investimento, aplicação ou reserva que
  valoriza — e **prometer rendimento ou valorização da cota** como benefício.
  **Não é vedado:** falar de investimento em imóveis, porque o investimento é o imóvel e ele existe;
  falar com investidores; apresentar o consórcio como **ferramenta de crédito ou de poupança** que o
  investidor usa para construir patrimônio. **Teste antes de apontar risco: o que, na frase, é o
  investimento?** Se for o bem, a frase está limpa. Se for a cota, ela viola a 1.1.
  *"Consórcio não é investimento"* continua sendo o disclaimer-âncora quando o cliente puxa a
  comparação de rentabilidade.
- **Apontar risco exige a regra e o trecho exato.** Alerta por palavra-chave, sem mostrar qual
  frase afirma o quê, é falso positivo: trava a operação e não protege ninguém. Compliance aqui
  existe para a venda acontecer sem risco, não para impedir a venda. Na dúvida, a dúvida vai ao
  consultor como pergunta — não como veto.
- **Nenhuma promessa, data ou probabilidade de contemplação — nem por implicatura.** "Costuma sair
  em torno do mês X" é promessa disfarçada.
- Jargão que o interlocutor não usa.
- Custo de uma linha nunca aparece em fala sobre outra linha.
- A skill devolve texto. **Gravar em `conhecimento/maquina-de-vendas/` é com aval do consultor**
  (Regra nº 1).

## Teste de aceitação

Mesma tese, três briefings — cabeleireira autônoma, transportadora com sete caminhões, casal
assalariado no aluguel. Se os três roteiros forem o mesmo texto com sinônimos trocados, reprovou.
