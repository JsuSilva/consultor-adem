---
name: comparativo-credito
description: Consórcio × financiamento × capital próprio aplicado, com a conta mostrada e os disclaimers obrigatórios: escolhe a comparação pela objeção do cliente, pede a conta ao calculista e monta a peça. Invoque com /comparativo-credito quando o cliente já entendeu o produto e pergunta "compensa?"; não dispara sozinha, porque produz peça que vai a campo.
---

# Skill — `comparativo-credito`

> Consórcio × financiamento × capital próprio, com a conta mostrada e os disclaimers obrigatórios,
> com a fronteira skill × `calculista` aplicada.
> Sem dado de cliente aqui dentro — a skill recebe o dado no momento do uso.

## Quando usar

O cliente já entendeu o produto e agora pergunta **"compensa?"**. A skill só entra depois disso.

**Não usar** para: apresentar consórcio a quem nunca ouviu falar (isso é apresentação do produto,
não comparativo), responder "quando eu sou contemplado?" (não tem resposta — ver §Compliance), ou
montar proposta com crédito que o cliente não declarou caber no orçamento.

## A fronteira — o que é da skill e o que é do `calculista`

| Passo | Quem faz |
|---|---|
| Ler a objeção e escolher a comparação (break-even · tributário · acesso) | **skill** |
| Reunir as entradas do cliente e **a linha** (auto × imóvel × pesados) | **skill** |
| Rodar a conta: números, sensibilidade, bloco de premissas | **`calculista`** |
| Montar a peça — o câmbio em uma frase, as tabelas juntas, a fronteira, os limites | **skill** |
| Revisar a peça | ⚠️ nenhum agente revisa o discurso — carimbo obrigatório |

**Aritmética zero na prosa** — nem por atalho, nem por ser "uma continha simples". Conta feita na
conversa muda a cada rodada: o custo total chega a mudar três vezes na mesma sessão. O script é a
única parte que não erra duas vezes igual, e é auditável depois.

## Qual comparação — a escolha vem da fala do cliente

| O cliente diz… | Comparação |
|---|---|
| "o banco me ofereceu CDC / financiamento a X%" | **Break-even** — consórcio × financiamento: break-even de taxa e, o que decide, de **tempo** |
| "eu junto no banco e compro à vista" · "prefiro deixar rendendo" · "e a poupança?" | **Acesso** — consórcio × capital aplicado: acumulação (o consórcio perde) e acesso (ganha por anos) |
| "tenho o dinheiro, mas não quero tirar do caixa" | **as duas** — break-even para a dívida, acesso para o custo de oportunidade |
| "no meu regime eu não abato nada mesmo" | **Tributário** antes das duas — como o regime do cliente muda a resposta |

**Na dúvida, é a de acesso.** Cliente que compara com dívida chega dizendo a taxa; cliente que
compara com poupança chega dizendo "eu me viro" — e esse é o mais comum e o mais difícil.

## Entradas

**Do cliente:** valor do bem · parcela que cabe no orçamento · o que ele faz hoje (aluga? paga
CDC? tem o capital?) · quanto tempo consegue esperar · caixa disponível para lance · regime
tributário (se for PJ) · **a linha** — automóvel, imóvel ou pesados, porque custo, prazo e teto de
embutido mudam e **a linha errada invalida a conta inteira**.

**Do produto:** nunca de memória, nunca da conversa. Os valores vivem em `config/consultor.json` —
`produto.linhas.<linha>` (taxa de administração, fundo de reserva, prazo, índice de reajuste),
`produto.lance`, `produto.seguro_mensal`, `produto.taxa_adesao` e, para o lado do banco,
`mercado.*` —, informados pelo consultor a partir de documento da administradora. **Campo vazio é
pergunta ao consultor, não estimativa.**

## Passos

1. **Ler a objeção antes de calcular.** Escolher a comparação pela tabela acima. Calcular as duas
   quando o cliente hesita entre dívida e capital próprio — a resposta costuma ser oposta em cada uma.
2. **Pedir a conta ao agente `calculista`, com comparação, linha e entradas declaradas.** É ele quem
   roda, lendo os parâmetros da config; a saída vai para `saida/` (fora do Git). Se o parâmetro da
   linha pedida estiver vazio na config, o `calculista` recusa a linha e explica — não troca por
   outra.
3. **Conferir a linha de fonte** no cabeçalho da saída. Sem `_fonte` declarada, a peça não sai.
4. **Montar a peça** com as duas colunas juntas — acumulação **e** acesso. Nunca só a favorável.
5. **Passar pelo checklist** de `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`;
   sem essa passada, a peça sai com o carimbo **⚠️ não revisado por compliance**.

## Saída esperada

Uma peça curta com, nesta ordem:

1. **O câmbio, em uma frase.** "Você troca R$ X de rendimento por Y anos de uso do bem."
2. **A tabela de acumulação** — saída do `calculista`; entra **inclusive quando é desfavorável**.
   Ela é o que dá credibilidade à seguinte.
3. **A tabela de acesso** — saída do `calculista` —, com a coluna de caixa exigido e o ajuste de
   régua declarado.
4. **A fronteira**, explícita: até que mês a contemplação faz o negócio valer a pena.
5. **Os limites declarados** que se aplicam ao caso: sempre, que todo mês de contemplação é
   premissa, não previsão; quando o cliente investe melhor que a poupança, que a conta o subestima;
   quando o parâmetro da linha não vier de documento da administradora, que ele é premissa ⚠️.
6. **O bloco de origem:** linha do produto e fonte do parâmetro (contrato × simulação × premissa ⚠️).

## Modelos de card para reutilizar

Dois cards de campo prontos, no mesmo design (`scripts/design.py`) e na mesma estrutura — destaques,
gráfico da fronteira, tabela lado a lado, faixa de conclusão, ficha de custos e rodapé de premissas.
Para um caso novo, copie o gerador mais próximo, troque o bloco de dados do caso e os textos; a
conta continua vindo do `calculista`.

| Modelo | Pergunta que responde | Gerador | Saída |
|---|---|---|---|
| Consórcio × financiamento na construção | em quanto tempo preciso vender para o financiamento seguir vantajoso | [`gerar-comparativo-construcao.py`](../../../scripts/gerar-comparativo-construcao.py) | `saida/comparativo-construcao.html` |
| Troca de financiamento pelo consórcio | vale quitar o financiamento com uma carta contemplada, e até que mês de contemplação | [`gerar-comparativo-troca-financiamento.py`](../../../scripts/gerar-comparativo-troca-financiamento.py) | `saida/comparativo-troca-financiamento.html` (e `.png` com `--png`) |

## Compliance — o que nunca sai desta skill

- ❌ **Data ou probabilidade de contemplação.** Toda linha da tabela de acesso é premissa, não
  previsão. A frase "não é promessa de contemplação" vai grudada na tabela, não em rodapé.
- ❌ **"Rende mais que a poupança" / "é investimento".** É falso pela tabela de acumulação e vedado
  pela Lei 11.795/2008 — e o contrato de adesão faz o próprio cliente declarar que não recebeu
  promessa de contemplação.
- ❌ **Só a tabela favorável.** Mostrar o acesso escondendo a acumulação é a versão elegante da
  mentira: o cliente que refaz a conta em casa não volta.
- ❌ **Antecipação sem ajuste de régua.** Se o cenário exige caixa para lance, esse caixa entra
  também do lado da poupança.
- ❌ **Custo de uma linha na conta de outra** — nem "porque é o número real mais recente".
- ✅ **Dizer que a poupança ganha quando ela ganha.** É o que sustenta a frase seguinte.

## Limites da própria skill

| # | Limite |
|---|---|
| S1 | Os parâmetros valem o que vale a fonte declarada na config (contrato, simulação ou afirmação do consultor). O que costuma faltar é o **reajuste**, que faz de todo custo um piso |
| S2 | A comparação de acesso usa **poupança** como piso do capital próprio. Cliente com CDB/Tesouro precisa da taxa dele, senão a conta o subestima |
| S3 | Nenhuma comparação monetiza o **valor de uso do bem** — a frase do câmbio fica em aberto |
| S4 | Sem o histórico de **lance vencedor** do grupo, escolher entre modalidades de lance fixo é preferência, não cálculo |
| S5 | A linha declarada na entrada é a linha da conta inteira — trocar de linha no meio é recomeçar do passo 2 |
