# consultor-adem

Um escritório de IA para **consultor de consórcio**: skills, agentes, scripts e base de regras que
transformam um assistente de IA (Claude Code, Codex, Cursor ou outro que leia `AGENTS.md`) num
parceiro de trabalho — da conversa com o lead à conta, do roteiro ao card, do follow-up ao CRM.

O repositório é **universal**: não traz nome, telefone, identidade visual nem número de nenhuma
administradora. Cada consultor clona e **personaliza com a própria configuração**.

> **Regra que ancora tudo:** consórcio não é investimento — é planejamento de compra. A distinção
> é regulatória (Lei 11.795/2008, Banco Central) e está em cada skill que produz fala ou peça.

---

## Comece pela aula

Antes de instalar qualquer coisa, entenda o que é um *harness*, uma skill e um agente — e por que
isso muda a semana de um consultor. A aula está em [`apresentacao/aula-ia-consultores/`](./apresentacao/aula-ia-consultores/):

| Material | Para quê |
|---|---|
| [`pdf/aula-60min.pdf`](./apresentacao/aula-ia-consultores/pdf/aula-60min.pdf) · [`pdf/aula-90min.pdf`](./apresentacao/aula-ia-consultores/pdf/aula-90min.pdf) | a aula, com notas do apresentador |
| [`aula-para-projetar.html`](./apresentacao/aula-ia-consultores/aula-para-projetar.html) | a versão para projetar (tecla **P** abre o apresentador) |
| [`pdf/kit-de-prompts.pdf`](./apresentacao/aula-ia-consultores/pdf/kit-de-prompts.pdf) | os pedidos prontos para o dia a dia |
| [`pdf/plano-30-dias.pdf`](./apresentacao/aula-ia-consultores/pdf/plano-30-dias.pdf) | o roteiro do primeiro mês |

Os `.md` ao lado são as fontes em [Marp](https://marp.app/).

## Primeiro uso

1. **Clone** o repositório e abra a pasta no seu harness (ex.: `claude` no terminal, dentro da pasta).
2. **Configure:** rode a skill `/configuracao`. Ela pergunta, seção por seção:
   - você — nome, contato, credenciais, assinatura, foto;
   - a administradora — nome, unidade, se usa o CRM Apollo;
   - sua identidade visual — cores, fontes, logo;
   - os números do produto — taxa, fundo de reserva, prazo, reajuste, comissão — **sempre com a
     fonte** (tabela, regulamento, contrato).

   Tudo vai para `config/consultor.json`, que **não sobe para o Git**.
3. **Formule sua primeira tese** com [`conhecimento/teses/README.md`](./conhecimento/teses/README.md).
4. **Monte seu caminho de prospecção** no agente [`prospector`](./.agents/agents/prospector.md) — ele vem
   em branco de propósito: cada um acha o seu.

Requisitos: Python 3.9+ para os scripts. Para exportar a aula: Node e `npx @marp-team/marp-cli`.

---

## Panorama

```
consultor-adem/
├── AGENTS.md          → as regras de trabalho do agente (valem em qualquer harness)
├── config/            → o modelo da configuração; a sua fica fora do Git
├── .agents/skills/    → o que você pede ao agente, por tarefa
├── .agents/agents/    → especialistas que o agente aciona
├── conhecimento/      → regras e compliance, fontes públicas, teses, cadência, anúncios
├── governanca/        → decisions-log, BACKLOG e como os dois funcionam
├── scripts/           → geradores de peça e utilitários (leem a config)
├── apresentacao/      → a aula de IA para consultores
├── dados/             → fora do Git — leads e clientes (LGPD)
└── saida/             → fora do Git — peças geradas com seus dados
```

### Skills — `.agents/skills/`

| Skill | Quando usar |
|---|---|
| `configuracao` | primeiro uso, ou quando um dado seu ou da administradora mudar |
| `diagnostico-de-lead` | logo depois do primeiro contato: fato × interpretação, tese, desqualificadores, próximo passo |
| `resumo-de-reuniao` | ao sair de uma conversa: resumo, compromissos, estágio, conta a pedir |
| `roteirista` | a fala — primeiro contato, retomada, objeção, pauta, pedido de indicação |
| `follow-up` | o próximo toque de um lead parado (Quem · Impedimentos · Próximo passo) |
| `comparativo-credito` | "compensa?" — consórcio × financiamento × capital próprio, com a conta aberta |
| `whatsapp-web` | rodada de ativação ativa no WhatsApp Web, com os limites de cadência |
| `crm-apollo` | só para quem usa o CRM Apollo: importa leads, registra ação, lança proposta |
| `reproduzir-card` | reproduz um card de venda com a sua identidade |
| `anuncios-meta` | configura do zero e opera Facebook/Instagram Ads — portfólio, conta, pixel, acesso do agente, ativação com teto |
| `anuncios-google` | configura do zero e opera Google Ads — conta, verificação financeira, conversões, integração de escrita |
| `whatsapp-oficial` | WhatsApp Business oficial (Cloud API) pelo MCP da Meta — **beta, para teste** |
| `auditoria-de-anuncios` | auditoria só de leitura das contas de anúncio, cruzada com as regras de anúncio de consórcio |

Skills que mandam mensagem, escrevem no CRM ou produzem peça para cliente **não disparam sozinhas**.

### Agentes — `.agents/agents/`

| Agente | Papel |
|---|---|
| `calculista` | toda conta de produto: parcela, saldo, lance, Price/SAC/CET, break-even, comissão |
| `auditor-financeiro` | confere a conta de uma peça pronta antes de ir a campo |
| `pesquisador` | dono das fontes: lei, normativo do BC, dado de mercado com origem citável |
| `sentinela` | vigia a coerência do repositório contra o decisions-log e o BACKLOG |
| `prospector` | esqueleto em branco — o seu método de achar quem abordar |

### Scripts — `scripts/`

Decks, cards comparativos, roteiros, placar do dia, fila de ativação, planilha para o CRM e o
cálculo de break-even. Todos leem `config/consultor.json`; campo vazio **para o script com aviso**,
nunca vira número inventado. Detalhes em [`scripts/README.md`](./scripts/README.md).

---

## Governança — por que ela existe

O agente trabalha rápido; sem registro, você perde o **porquê** de cada escolha e o agente passa a
decidir por você. A governança evita as duas coisas:

- **`governanca/decisions-log.md`** — o porquê de cada escolha sua (posicionamento, discurso,
  número adotado). Só entra com o seu aval; nunca se edita, supera-se com nova entrada.
- **`governanca/BACKLOG.md`** — o que falta, o que está em curso, o que foi entregue.
- **`sentinela`** — compara o que está escrito com o que foi decidido e aponta a divergência.
- **`AGENTS.md`** — as três regras: não decidir por você, escopo estrito por pedido, resposta em
  bullets numerados.

Começa vazio: a `D-001` é sua. Como usar, em [`governanca/README.md`](./governanca/README.md).

---

## Limites

- **Não é material de venda.** Peça que vai a cliente passa pela régua de
  [`conhecimento/regras-e-compliance/`](./conhecimento/regras-e-compliance/) e, quando exigido,
  pela aprovação da sua administradora.
- **Não traz números de administradora.** As regras da sua administradora e do Banco Central
  prevalecem sobre qualquer texto deste repositório.
- **LGPD:** dado de lead e cliente só em `dados/`. Templates sim, gente não.

## Licença

Uso livre para fins **não comerciais**, com duas licenças conforme o tipo de arquivo — ver [`LICENSE`](./LICENSE):

- **Código** (`.py`, `.sh`, `.css`, moldes `.tpl.html`): [PolyForm Noncommercial 1.0.0](./LICENSE-CODIGO.md).
- **Documentos** (textos, aula, imagens): [CC BY-NC-SA 4.0](./LICENSE-DOCUMENTOS.txt).

© 2026 Josué Silva.
