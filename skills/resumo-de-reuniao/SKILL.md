---
name: resumo-de-reuniao
description: Notas cruas de uma reunião ou call viram resumo, compromissos com dono e data, atualização de estágio no pipeline e a conta a pedir ao calculista. Use ao sair de qualquer conversa com lead, cliente ou contador, enquanto a memória está fresca.
---

# Skill — `resumo-de-reuniao`

> Notas cruas em decisão. Fecha o ciclo da reunião.
> Sem dado de cliente aqui dentro — a skill recebe o dado no momento do uso.

## Quando usar

Ao sair de qualquer reunião ou call, enquanto a memória está fresca.

## Entradas

Notas cruas, gravação transcrita ou o que se lembra; o código da ficha do lead (`PAR-AAAA-NNN`),
se existir.

## Passos

1. Separar **fato dito** de **interpretação** — em blocos diferentes, nunca misturados no parágrafo.
2. Extrair os **números declarados** que alimentam a conta: aluguel, parcela atual, tamanho e idade
   da frota, faturamento, caixa disponível para lance, taxa que o banco ofereceu — todos marcados
   **declarado, não conferido**.
3. Listar os **compromissos com dono e data** — os do cliente e os do consultor.
4. Atualizar o **estágio** do pipeline e registrar o motivo da mudança.
5. Apontar o que falta para a próxima conversa e **a conta a pedir ao `calculista`** — tipo de
   comparação, linha, entradas novas.

## Saída esperada

Resumo em blocos — fato dito · interpretação · números declarados · compromissos · estágio e motivo ·
pendências · conta a pedir — **pseudonimizado por código**.

## Limites

- Interpretação **nunca** vira fato.
- Dado nominal fora do Git: a versão identificada vive em `dados/` ou no CRM.
- Nenhuma conta de produto na prosa — a conta é do `calculista`. Listar compromissos e datas é
  contagem, não conta.
