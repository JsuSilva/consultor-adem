---
name: diagnostico-de-lead
description: Da conversa crua à qualificação de um lead de consórcio: separa fato de interpretação, casa o gatilho com uma das teses do consultor, roda os desqualificadores, identifica linha e regime, nomeia a objeção provável e devolve a ficha pseudonimizada com o próximo passo. Use logo depois de qualquer primeiro contato — reunião, ligação, WhatsApp, indicação —, antes de calcular ou escrever qualquer roteiro.
---

# Skill — `diagnostico-de-lead`

> Da conversa crua à qualificação. É o primeiro elo do meio do funil.
> Sem dado de cliente aqui dentro — a skill recebe o dado no momento do uso.

## Quando usar

Logo depois de qualquer primeiro contato — reunião, WhatsApp, ligação, indicação. **Antes** de
calcular qualquer coisa e antes de escrever qualquer roteiro.

## Entradas

- as notas cruas da conversa;
- o que se sabia do lead antes dela (a linha da lista do `prospector`, se veio de lista);
- o canal de origem — frio, ponte de contador, indicação.

## Passos

1. Separar **o que o cliente disse** do que se interpretou — são registros diferentes.
2. Extrair o **gatilho observável** e casar com uma das teses do consultor em `conhecimento/teses/` —
   conferindo se a tese está viva: tese vetada ou bloqueada pela própria régua não recebe lead.
3. Rodar os **desqualificadores** da tese — os checáveis na lista e os de reunião (§5 da tese).
4. Identificar a **linha do produto** (automóvel × imóvel × pesados) e o **regime tributário** —
   mudam a conta e o discurso, e a linha errada contamina a conta inteira: custo, prazo e teto de
   embutido são de cada linha.
5. Estimar o ticket e **quem decide** — sozinho, cônjuge, sócio, contador.
6. Nomear a **objeção provável**: dívida ("o banco me ofereceu X%") → break-even de tempo,
   consórcio × financiamento · capital próprio ("junto e compro à vista") → acumulação × acesso,
   consórcio × capital aplicado · regime ("não abato nada mesmo") → o corte tributário antes.
7. Definir o próximo passo e **qual conta pedir ao `calculista`** — tipo de comparação, linha, entradas.

## Saída esperada

Ficha curta **pseudonimizada por código** (`PAR-AAAA-NNN`): gatilho · tese · linha · regime ·
desqualificadores checados e os por checar · ticket estimado · quem decide · objeção provável ·
conta a pedir · próximo passo · estágio de pipeline sugerido.

## Limites

- **Sem gatilho não é lead qualificado — é curiosidade**, e a ficha diz isso em vez de forçar uma tese.
- Não inventar dado que o cliente não deu; número citado de cabeça entra como **declarado, não conferido**.
- Nome, CPF e telefone **não entram no Git**: ficam em `dados/` ou no CRM.
  ⚠️ MEI e empresário individual: o dado da "empresa" é dado pessoal — tratar como identificado
  desde o início.
- Nenhuma conta de produto aqui — a conta é do `calculista`.
