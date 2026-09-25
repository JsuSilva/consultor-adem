# AGENTS.md — regras de trabalho do agente neste repositório

> Vale para qualquer harness que leia `AGENTS.md` (Claude Code, Codex, Cursor e outros).
> "O consultor" é a pessoa dona desta cópia do repositório. Os dados dele estão em
> `config/consultor.json`, que a skill `configuracao` preenche.

## Regra nº 1 — não decidir pelo consultor

**Proibido tomar decisão pelo consultor.** Vale para negócio, produto, discurso, design, escopo e
processo — e também para o que o agente julgar "decisão pequena e óbvia".

Ao ver que uma escolha precisa ser feita: **parar, apresentar a proposta com trade-offs e esperar o
aval.** Não escrever a escolha em arquivo, peça ou commit antes do "pode fazer".

**Não é permitido:**
- Virar observação própria em pendência, tarefa ou proposta dentro dos documentos.
- Fazer melhoria adjacente não pedida, mesmo que pareça consequência natural do pedido.
- Ler documento antigo ou mensagem anterior como se fosse aval — **histórico não é validação**.
- Registrar decisão como validada sem aprovação explícita e citável do consultor
  (ver `governanca/decisions-log.md`).

## Regra nº 2 — escopo estrito por mensagem

Fazer **exatamente o que foi pedido naquela mensagem**, nada além. Se pedirem para acrescentar uma
coluna a uma tabela, acrescenta-se **uma coluna** — não se refaz a tabela.

Surgindo sugestão: **uma linha no fim da resposta**, em forma de pergunta. Nunca trabalho já
executado. Pedido ambíguo: perguntar antes — é mais barato que refazer.

## Regra nº 3 — resposta em bullets numerados

Toda resposta vem em **bullets numerados**, nunca em texto corrido.

- Um item = um fato. Frase curta.
- Passando de dez itens no mesmo nível, agrupar em categorias com sub-itens (1.1, 1.2). Cortar item
  para caber é proibido.
- **Decisão que depende do consultor vai num bloco "Decisões" no fim**, uma linha por decisão, com
  as opções.
- Sem relatório não pedido. Código, comando e diff entram como bloco.

## Regras do ofício — valem em toda peça e toda conta

1. **Consórcio não é investimento.** É planejamento de compra. A distinção é regulatória
   (Lei 11.795/2008, supervisão do Banco Central) — ver `conhecimento/regras-e-compliance/`.
2. **Nunca prometer contemplação**, data, chance ou probabilidade de sorteio ou lance.
3. **Nada de número inventado.** Taxa, prazo, fundo de reserva e comissão vêm de
   `config/consultor.json`, informados pelo consultor a partir de documento da administradora.
   Campo vazio é pergunta, não estimativa.
4. **Mostrar a conta** em todo número: fórmula, substituição, resultado. Premissa não confirmada
   leva ⚠️. Fonte e data em todo dado de mercado.
5. **LGPD:** dado nominal de lead ou cliente fica em `dados/`, fora do Git. Templates sim, gente não.
6. **Peça que vai a pessoa real** (mensagem, card, proposta) só sai com aval do consultor naquela
   rodada.

## Mapa do repositório

| Pasta | O que tem |
|---|---|
| `config/` | a configuração do consultor (modelo versionado; o preenchido fica fora do Git) |
| `agentes/` | subagentes — calculista, auditor, pesquisador, sentinela, prospector |
| `skills/` | skills — configuração, diagnóstico, roteiro, follow-up, comparativo, CRM, WhatsApp, cards |
| `conhecimento/` | regras e compliance, fontes públicas, modelo de tese, cadência de WhatsApp |
| `governanca/` | decisions-log, BACKLOG e como os dois funcionam |
| `scripts/` | geradores de peça e utilitários; todos leem `scripts/config.py` |
| `apresentacao/` | a aula de IA para consultores |
| `dados/` · `saida/` | fora do Git — dado de cliente e peças geradas |

`.claude/agents` e `.claude/skills` são atalhos para `agentes/` e `skills/`; o conteúdo é um só.
