# Governança — como o repositório lembra do que foi decidido

Dois arquivos e um agente. Existem para que nenhuma sessão de IA trate como decidido o que o
consultor não decidiu, e para que nenhum número velho continue circulando depois que mudou.

## `decisions-log.md` — o porquê

- Toda escolha do consultor que muda produto, discurso, número, processo ou escopo vira uma entrada
  `D-0XX`, com data, contexto, decisão e **aval citável** — a palavra dele, entre aspas.
- **Append-only.** Entrada antiga nunca é editada. Mudou de ideia: entra uma nova que diz qual supera.
- É o que permite, meses depois, saber **por que** um número ou uma regra é como é — e não
  "melhorar" sem querer uma escolha que tinha motivo.

## `BACKLOG.md` — o que falta

- O que está a fazer, em curso e entregue.
- Pendência só sai dali entregue, ou por decisão registrada no `decisions-log.md`.
- Observação do agente **não** vira item sozinha: vira pergunta ao consultor, e entra se ele aprovar.

## Como o `sentinela` usa os dois

- Monta, a partir das entradas que *substituem / corrigem / superam*, o dicionário do valor velho e
  do vigente, e varre o repo atrás do velho ainda circulando.
- Toda afirmação de "o consultor decidiu / aprovou" nos documentos precisa de **âncora** num dos
  dois arquivos. Sem âncora, ele reporta como pergunta.
- Pendência que sumiu do BACKLOG sem ter sido entregue, ou entrada `D-0XX` alterada, é achado.
- Ele só lê e reporta. Não edita nada — nem estes dois arquivos.

## A ligação com o `AGENTS.md`

- **Regra nº 1 (não decidir pelo consultor):** o `decisions-log.md` é o único lugar onde uma decisão
  existe. O que não está lá, com aval citável, não foi decidido.
- **Regra nº 2 (escopo estrito):** sugestão do agente vai para o fim da resposta, como pergunta —
  não para o BACKLOG.
- **Regra nº 3 (bullets numerados):** decisões pendentes saem no bloco "Decisões" da resposta; as
  aprovadas é que viram entrada no log.

## O ritual mínimo

1. **Registrar decisão** sempre que o consultor aprovar algo que muda número, regra, discurso ou
   escopo. Na mesma rodada, com o trecho da mensagem dele como aval.
2. **Atualizar o BACKLOG** quando algo entra, começa ou é entregue.
3. **Chamar o `sentinela`:**
   - ao fim de toda rodada de edição que troque número ou decisão;
   - depois de uma decisão que substitui parâmetro;
   - antes de uma peça ou documento ir a campo;
   - antes de commit nestes dois arquivos.
