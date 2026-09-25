---
name: follow-up
description: O próximo toque de um lead parado, no framework QIP — Quem (quem é / quem será), Impedimentos (o do cliente e o do consultor) e Próximo passo com ação, data e dono. Devolve a ficha por lead e o contrato de seis campos que a skill irmã crm-apollo grava no Apollo — ou que o consultor registra no próprio CRM, se não usar o Apollo. Invoque com /follow-up quando houver lead parado além do prazo do estágio, ou depois de uma varredura de conversas; não dispara sozinha, porque o toque vai a pessoa real.
---

# Skill — `follow-up`

> Existe porque a cadência tem de ser **sistêmica**: não pode depender do temperamento de quem
> vende nem da memória do dia.
> Framework **QIP**. Sem dado nominal aqui dentro: a ficha preenchida mora em `dados/`.

## Quando usar

Lead parado além do prazo do estágio · depois de uma varredura das listas do WhatsApp · ao fim de uma
reunião, para definir o toque seguinte · quando o consultor pede "o que eu faço com fulano".

## A régua que manda nesta skill

**Esta skill decide o quê; a `crm-apollo` sabe como escrever.** Ela não abre modal, não conhece
seletor do Apollo e não copia mecânica de lugar nenhum — entrega o contrato e a skill irmã executa.
É o mesmo desenho da `comparativo-credito`, que escolhe a comparação e pede a conta ao `calculista`.
Cópia de mecânica entre skills é o que apodrece: a cópia que ninguém abre envelhece e o erro
sobrevive nela.

**Vale para quem usa o CRM Apollo** (`administradora.crm.usa_apollo` em `config/consultor.json`).
Quem não usa recebe o mesmo contrato de seis campos e o registra onde registra o funil — o CRM que
usar ou uma planilha em `dados/` —, com a mesma regra de `mecanismo`.

## O framework QIP

### Q — Quem, em dois tempos

**Q1 · quem a pessoa é:** nome · idade · profissão · **faixa** de renda familiar.
**Q2 · quem ela será:** o sonho de conquista · **valor** da conquista · **prazo** para alcançar ·
**parcela mensal** disponível para investir nele · **quanto já tem guardado** para isso.

Os quatro números do Q2 são a lista de entrada do `calculista`. Quem preenche o Q2 consegue simular;
quem não preenche, não — e é por isso que o Q2 é o que a conversa persegue.

### I — Impedimentos, em dois lados

**I1 · o que impede o cliente** de realizar o sonho com consórcio hoje. Exemplos reais: a parcela não
cabe no orçamento; a necessidade é emergencial e não combina com a natureza do consórcio; a decisão
depende de terceiro (sócio, cônjuge, contador); o dinheiro já está comprometido em outra dívida.

**I2 · o que me impede, como consultor**, de apresentar a solução. Exemplos reais: falta o cenário Q
completo; áudio do lead não ouvido; material prometido e não enviado; pergunta minha que nunca foi
cobrada; indisponibilidade de agenda; diferença de idioma.

**O I2 é o campo que mais rende.** Na varredura que deu origem a esta skill, a maioria dos fios
parados estava travada em coisa do consultor, não do cliente.

### P — Próximo passo

**Uma ação, com data e dono.** Resolve **primeiro o meu impedimento, depois o do cliente** — não se
cobra de alguém o que ainda não foi entregue a ele.

## Regras de preenchimento

1. **Frase textual ou `— não sei`.** Onde o lead falou, o campo guarda **a frase dele entre aspas**;
   onde não falou, guarda **`— não sei`**. Não existe terceira opção: paráfrase que parece dado é o
   jeito de inventar sem perceber. Buraco declarado vale mais que suposição.
2. **Renda em faixa, nunca número exato**, e só em `dados/`, fora do Git. É dado sensível e quase
   nunca sai no primeiro contato — o campo pode entrar depois sem travar o resto da ficha.
3. **A ordem de coleta não é a ordem de apresentação.** Na conversa real o impedimento aparece antes
   do sonho: colete na ordem em que a pessoa falar, apresente na ordem Q → I → P. Forçar pergunta de
   sonho antes da hora é o que faz lead fugir.
4. **Impedimento meu nasce com data de hoje ou amanhã.** O do cliente pode esperar; o meu, não. Sem
   essa trava o I2 vira lista de desculpa.
5. **Toda ficha fecha com um estágio** do funil: *Em ligação · Agendado · Reunião · Negociação ·
   Removido*. Sem o veredito, a ficha descreve e não move nada.
6. **O memo é o histórico do cliente, não o diário do agente.** Erro de leitura se corrige no
   registro — editando ou apagando e relançando —, nunca se narra dentro dele. Nada de "eu tinha
   presumido X, mas é Y": quem lê o card seis meses depois precisa do fato, não do caminho até ele.
7. **O toque precisa acrescentar algo** — um número que não existia, uma ressalva honesta, um prazo
   real. "Passando para saber se viu" não é toque, é ruído.

## Encerramento — a regra do SAIR

Quando o lead **recusou** — "não temos interesse", "não tenho interesse agora", "já tenho
consórcio" dito como fecho —, o próximo passo é o encerramento, e ele segue esta regra:

1. **Uma última mensagem, e só uma.**
2. **Silêncio mantém o contato; SAIR é a única ação ativa.** A mensagem diz que o contato fica
   guardado para futuras oportunidades e que, para não receber mais nada, basta responder SAIR.
   **Nunca** pedir resposta para permanecer ("pode deixar"): a maioria não responde, e o silêncio
   ficaria sem autorização clara — é risco de denúncia.
3. **Só a resposta SAIR leva o card para Removidos.** A mecânica de remover é da `crm-apollo`
   (ou do CRM que o consultor usar).
4. **Nenhuma pergunta comercial.** Quem já disse não e recebe pitch escolhe sair mais rápido.
5. **Copia-se o tom, não a fórmula.** "Segunda opção" só cabe para quem já tem consórcio e
   consultor; para os outros, soa como argumento.
6. **Retroativo:** vale para recusa registrada antes da regra. **Número desativado não recebe
   mensagem** — o lead fica dormente, não removido.
7. **O texto parte do repertório da skill `roteirista`**, ajustado ao caso, e vai ao consultor
   antes do envio.

No contrato abaixo, o encerramento sai com `mecanismo: comentário` enquanto a resposta não chega;
com o SAIR recebido, a `crm-apollo` remove o card.

## O contrato com a `crm-apollo`

A skill devolve, **por lead**, seis campos — e nada mais:

```
{ lead, ação, data, dono, mecanismo: agendar | comentário, memo }
```

- **`memo`** é a ficha QIP em texto corrido, sem acento (o Apollo recusa caractere especial em
  alguns modais). Começa com `QIP.` e traz os campos na ordem QUEM é / QUEM será / IMPEDIMENTO do
  cliente / IMPEDIMENTO do consultor / PROXIMO PASSO / ESTAGIO.
- **`mecanismo`** decide onde o passo é gravado:
  - **`agendar`** — quando o próximo passo **envolve o cliente** (ligação, reunião, retorno
    marcado). No Apollo vira registro com `#agendar` e data futura, e **o card vai para *Agendado***.
  - **`comentário`** — quando o próximo passo é **só meu** (mandar material, ouvir áudio, levantar
    número). Vira lembrete com data **sem mover o card**.
  - Razão: card não pode estar em *Agendado* por causa de dever de casa do consultor, senão o funil
    mente sobre quantos compromissos existem.

Quem executa é a **`crm-apollo`**. Esta skill não abre o Apollo. Sem Apollo, o consultor registra os
seis campos no próprio CRM ou em `dados/`, respeitando a mesma separação agendar × comentário.

## Fronteiras com as outras peças

| Precisa de | Quem entrega |
|---|---|
| O texto que vai ao lead | skill `roteirista`, com o briefing desta |
| Número novo (parcela, lance, break-even) | agente `calculista`, com linha e origem declaradas |
| Escrever no Apollo | skill `crm-apollo`, pelo contrato de seis campos (sem Apollo: o consultor, no CRM dele) |
| Qualificar um lead novo | skill `diagnostico-de-lead` |

## Saída esperada

A ficha QIP de cada lead · o contrato de seis campos pronto para a `crm-apollo` · e, quando houver
toque, **o briefing para o `roteirista`** — nunca o texto improvisado aqui dentro.

## Limites

- **Não escreve no Apollo** e não guarda mecânica de CRM. Delega.
- **Não inventa texto que vai a pessoa real** — a fala é do `roteirista` e a aprovação é do consultor.
- **Não inventa dado do lead.** Campo sem fala do lead é `— não sei`.
- **Nada de promessa de contemplação**, nem por implicatura ("costuma sair em torno de…").
- **Número novo vem do `calculista`**, não da memória.
- **Nenhum dado nominal em arquivo versionado**: a ficha preenchida vive em `dados/`.
- **A peça sai com ⚠️ não revisado por compliance** enquanto nenhum revisor a passar pelo checklist
  de `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`.
