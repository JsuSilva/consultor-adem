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
2. A dor **na linguagem de quem ouve** — uma conta, dois vocabulários: o sócio no Simples ouve
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

**F2 · compromisso antes da conta.** Pede o "sim" condicional antes de gastar simulação.
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

### Sequência de prospecção — exemplo de um público (médicos investidores)

Os atalhos são respostas rápidas do WhatsApp Business. A etapa de cada texto na cadência está em
`conhecimento/maquina-de-vendas/05-cadencia-e-limites-do-whatsapp.md`.

**Etapa 1 — WhatsApp.** Entrada, e depois **uma** das três aberturas, alternadas entre os leads.
```
Boa tarde, tudo bem? Me chamo {consultor.nome}, eu falo com Dr(a). [Nome]?
```
Abertura, alternativa 0 — *só vale se o consultor de fato tiver uma carteira de médicos
investidores*:
```
Opa, [Nome]!

Estou entrando em contato porque trabalho com uma estratégia usando o consórcio para investimento
em imóveis, já tenho uma carteira de Médicos Investidores, gostaria de apresentar você também como
funciona, consegue falar comigo hoje?
```
Abertura, alternativa 1:
```
Opa! Me chamo {consultor.nome}.

Estou entrando em contato porque trabalho com uma estratégia usando o consórcio como ferramenta
para investimento em imóveis na planta. Você hoje investe em imóveis?
```
Abertura, alternativa 2:
```
Opa! Me chamo {consultor.nome}.

Estou entrando em contato porque trabalho com Investidores usando o consórcio como estratégia para
construção de patrimônio imobiliário, gostaria de apresentar você como funciona, consegue falar
comigo hoje?
```

**Etapa 2 — follow-up.** Atalho `followup`. A saudação segue a hora corrente.
```
Bom dia Dr(a). [Nome], tudo bem?
Te mandei mensagem, e percebi que não respondeu. Imagino que seja porque não teve tempo.
Podemos conversar hoje?
```
**O `[Nome]` só entra quando o nome está confirmado.** Lead de razão social institucional
— "Clinica X", "Y Servicos Medicos" — não tem nome de pessoa conhecido: esse vai pelo caminho da
secretária, não por este texto com um nome adivinhado.

**Etapa 3 — ligação.** Mantém a estrutura do modelo — silêncios, manhã ou tarde, dois horários — e
amarra a ligação à mensagem de WhatsApp que veio antes.
```
Olá, boa tarde! Com quem eu falo?
[espera]
Dr(a). [Nome]? Aqui é o {consultor.nome}, consultor da {administradora.nome}. Te mandei uma mensagem no WhatsApp esses dias.
[fica em silêncio, espera a resposta]
Eu trabalho com médicos que investem em imóveis, usando o consórcio como ferramenta para comprar imóvel na planta e construir patrimônio imobiliário.
Queria te mostrar em 20 minutos como funciona. Fica melhor no seu consultório ou por vídeo?
[fica em silêncio]
De manhã ou de tarde?
Tenho [dia] às 10h ou às 14h30, o que fica melhor?
Maravilha, Dr(a). [Nome]. Agendado [dia] às [hora]. Qual seu e-mail pra eu mandar o convite?
Até lá!
```
Se atender a secretária:
```
Eu falo com o(a) Dr(a). [Nome]? … Qual o melhor horário pra eu retornar?
```
Se pedir "manda pelo WhatsApp":
```
Mando sim. E já deixo reservado um horário de 20 minutos pra gente conversar: [dia] às [hora] fica bom?
```

**Etapa 4 — pega-ratão.** Atalho `fallowup5`. **Só sai com uma condição especial real do dia**,
confirmada na administradora — sem ela, a etapa não sai.
```
Boa tarde [Nome], tudo bem? Estou com uma condição especial hoje, posso te apresentar aqui?
```

**Etapa 5 — novo follow-up.**
```
Oi [Nome] recebeu minha última oportunidade, o que achou?
```

**Etapa 6 — encerramento.** Atalho `follow-up2`. Cumpre a regra do SAIR: silêncio mantém o contato,
SAIR remove.
```
Bom dia, tudo bem?
Te mandei essa mensagem e percebi que não respondeu. Imagino que seja porque não teve tempo.
Caso não me responda, vou colocar você numa lista de divulgação que faço através do número
{consultor.telefone}, salve esse contato por favor.
Caso não deseje continuar recebendo novidades e ofertas, basta responder SAIR
```

## Saída esperada

O roteiro no formato do canal · o próximo passo explícito · o bloco de origem dos números (linha e
fonte) · o carimbo **⚠️ não revisado por compliance** — obrigatório enquanto nenhum revisor passar a
peça pelo checklist de `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`. O
carimbo não corrige a fala: roteiro é lido para ser dito, e o que não pode ser dito não entra,
carimbo ou não.

## Limites

- **Não gera número.** Conta de produto é do `calculista`; sem número calculado, o roteiro usa o
  gatilho e a pergunta — não inventa.
- **Não inventa prova.** Credencial, carteira, tempo de casa e caso de cliente só entram se estiverem
  em `consultor.credenciais` ou forem informados pelo consultor.
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
