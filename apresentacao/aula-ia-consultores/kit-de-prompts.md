---
marp: true
theme: latao
size: a4
class: folha
paginate: false
lang: pt-BR
title: Kit de prompts
---

# Kit de prompts

### O gênio e o escritório · IA para a prospecção do consultor de consórcio · Josué Silva

## Um bom pedido tem 5 partes

1. **Contexto**: o que o gênio precisa saber (quem é o cliente, onde a conversa parou).
2. **Intenção**: o que você quer que aconteça.
3. **Papel** (ou persona): quem o gênio deve ser.
4. **Objetivos**: como saber que deu certo.
5. **O que é, e o que não é**: inclusive o que ele não pode prometer.

## Prompt 1 · Configurar o escritório

*No Antigravity, dentro do projeto `Consultor-Ademicon`.*

```
Sou consultor de consórcio da Ademicon. Esta pasta é o meu escritório.

Crie as regras em .agents/rules/, todas Always On:
1. quem-sou-eu.md — quem sou, para quem vendo, como escrevo.
2. limites.md — nunca prometer contemplação, sorteio
   ou rendimento; nunca chamar consórcio de investimento;
   nunca dizer que devolve tudo.
3. como-trabalhar.md — não decidir por mim; fazer só
   o que eu pedir; responder em tópicos curtos;
   não guardar nome nem telefone de cliente.

Antes de escrever, me faça 5 perguntas, uma por vez.
```

## Prompt 2 · Receber a calculadora

<div class="duas-colunas">

```
Crie a skill calculadora em
.agents/skills/calculadora/SKILL.md.
Ela faz as contas de consórcio comigo,
sempre abertas. Me mostre antes de salvar.

PARÂMETROS
- Taxa de administração, fundo de reserva,
  prazo, adesão e seguro vêm de mim ou do
  simulador oficial. Nunca de memória.
- A taxa muda por linha. Fundo de reserva
  só em motorizados (auto, pesados, moto).
- Custo de uma linha nunca vale para outra.

CONTAS
- Saldo devedor = crédito + taxa
  + fundo de reserva (quando houver)
- Parcela = saldo devedor ÷ prazo
- Parcela reduzida =
  ((% de redução × crédito) + taxa) ÷ prazo
  (taxa sobre o crédito cheio: confirmar
  no contrato)
- Pós-contemplação =
  (crédito + taxa − pago − lance)
  ÷ prazo restante
- Reajuste: imóvel pelo INCC; veículo e
  serviço pelo INPC. Sem reajuste, é piso.

LANCE: o prazo não muda, a parcela cai
- Livre: oferta em % ou em parcelas;
  vence a maior, é leilão.
- Fixo: % definido pelo grupo; empate
  vai a sorteio.
- Embutido: sai da própria carta, sem
  dinheiro do bolso; o crédito líquido
  fica menor. Mostrar até onde ainda
  compra o bem.
- Fidelidade: exclusiva da Ademicon,
  cliente antigo em dia, regras próprias.

COMPARAR
- Financiamento: Price e SAC pelo CET
  (IOF, avaliação, seguros, entrada),
  nunca pelo juro nominal.
- Capital próprio: poupança, CDI, CDB com
  IR, LCI/LCA e IPCA+; e o mês em que
  "aplico e compro à vista" se cruza.
- Meses comprados = (custo do
  financiamento − custo do consórcio)
  ÷ aluguel ou custo mensal da espera.

COMO RESPONDER
- Fórmula, substituição e resultado.
- Cenários quando um número é incerto.
- Índices e taxas de mercado com fonte
  e data.
- Fechar com as premissas: linha,
  origem e data de cada número.
- Nunca afirmar chance, probabilidade
  ou data de contemplação.
```

</div>

---

## Prompt 3 · Receber o calculista

```
Crie o agente calculista em .agents/agents/calculista.md.

Quem ele é: um colega de fora que faz ou confere contas
de consórcio. Usa a skill calculadora para toda fórmula.

Limites:
- Só lê e calcula. Não edita arquivo, não escreve mensagem.
- Libere para ele só as ferramentas de leitura.
- Recebe o caso inteiro no pedido; não depende da conversa.

Quando for chamado:
- Para conferir números de uma mensagem ou proposta:
  refaz a conta do zero e aponta cada diferença.
- Para um comparativo que vai ao cliente: devolve a conta
  aberta e as premissas, com origem e data.

Me mostre antes de salvar.
```

## Prompt 4 · A próxima é sua

```
Quero criar uma nova [skill ou agente]: [nome].

Para que serve: [                                      ]
Quando eu uso: [                                       ]
O que eu tenho em mãos: [                              ]
O que ele me entrega: [                                ]
O que ele nunca pode fazer: [                          ]

Antes de escrever, me faça as perguntas que faltarem, uma por vez.
Siga as regras desta pasta e me mostre antes de salvar.
```
