# T{{N}} — {{Nome da tese}}

> **Modelo em branco.** Copie para `T{{N}}-{{nome-curto}}.md` e preencha seção por seção, seguindo o
> passo a passo do [`README`](./README.md). Apague as instruções em itálico ao preencher.
> Segmentos: {{quem tem este gatilho — liste os tipos de negócio ou de pessoa}}.
> Escrita em **{{AAAA-MM-DD}}**. Estado: {{viva · vetada · pendente}}. Parâmetros da administradora:
> {{com fonte na config · ⚠️ premissa}}.

## 1. O gatilho

**{{O fato observável, em uma frase em negrito.}}**

*Explique como ele se identifica **de fora, sem falar com ninguém**: qual dado público o revela e
qual cruzamento (regime tributário, tempo de endereço, porte) já qualifica ou desqualifica antes do
primeiro contato. Se o gatilho não é visível de fora, diga isso aqui — e diga quem o enxerga.*

## 2. A dor em uma frase

> *"{{A frase, dita na linguagem do cliente — não na do produto.}}"*

*Em duas ou três linhas: o que dói de verdade. Raramente é o valor isolado; é a combinação — caixa
que sai, patrimônio que não se forma, imposto que não reduz, dependência de um terceiro.*

## 3. A aritmética — os três caminhos

**Caso-referência:** {{custo mensal da situação atual}} · crédito de {{C}} · linha {{imóvel · auto ·
pesados · …}} · prazo {{n}} meses · taxa adm + FR {{da config, com fonte}} · financiamento a
{{i}} a.m. ({{fonte e data}}) · horizonte {{N}}, valores nominais.

*Números só do `calculista`, com os parâmetros de `config/consultor.json`. Parâmetro sem fonte leva ⚠️.
Se a aritmética desta tese não é de custo (liquidez, balanço, sucessão), diga no título da seção qual é.*

| Caminho | Desembolso em {{N}} | Ao final |
|---|---|---|
| **A — {{manter a situação atual}}** | {{valor}} | {{o que sobra ao final}} |
| **B — Financiar hoje** | {{valor}} (parcela {{valor}}) | {{posse desde o mês 1}} |
| **C — Consórcio** | {{valor}} + {{custo da espera até a contemplação}} (parcela {{valor}}) | {{posse no mês `k`}} |

*O primeiro número da reunião: a comparação mais simples e mais forte que a tabela produz (ex.: a
parcela do consórcio frente ao que o cliente já paga hoje).*

### O custo da espera, e quanto ele compra

| Contemplado no mês | Desembolso total em {{N}} | vs. financiar | vs. {{situação atual}} |
|---|---|---|---|
| {{k₁}} | | | |
| {{k₂}} | | | |
| {{k₃}} | | | |

> **Break-even de tempo: mês {{X}}.** A diferença de {{valor}} compra **{{X}} meses** de
> {{custo da espera}}. *Escreva o argumento honesto que sai daqui: não "consórcio é mais barato", mas
> "você tem X meses de folga; a pergunta é só qual a chance de ser contemplado antes disso" — pergunta
> que se responde com o histórico do grupo, não com promessa.*

## 4. O corte tributário

| Regime | {{O custo da tese}} deduz? | Força da tese |
|---|---|---|
| **Simples Nacional** | {{sim · não}} | {{🟢 · 🟡 · 🔴}} |
| **Lucro Presumido** | {{sim · não}} | {{🟢 · 🟡 · 🔴}} |
| **Lucro Real** | {{sim · não}} | {{🟢 · 🟡 · 🔴}} |

*Uma frase: em que regime a tese vive e em qual enfraquece. Para tese de pessoa física, diga o que
substitui este corte (ou que ele não se aplica).*

## 5. ⛔ Os desqualificadores — onde esta tese perde

### 5.1 Desqualifica **na lista** — checável antes do contato

*Poda antes de gastar tempo. Nada aqui exige conversa.*

| Condição | Limiar | Como checar |
|---|---|---|
| {{condição}} | {{limiar objetivo}} | {{fonte pública ou estimativa}} |

### 5.2 Desqualifica **na reunião** — o que se diz em voz alta

*Os que só aparecem na conversa. Dizê-los é o que separa consultor de vendedor. Para cada um: a
situação e o que se recomenda no lugar do consórcio.*

- **{{situação}}** — {{por que o consórcio perde aqui e qual é a alternativa}}.

### 5.3 Risco operacional — **checar calado**, não anunciar

*O que mata o negócio por fora da conta — por exemplo, o cliente não passar na análise de crédito
da contemplação. Diga o que se qualifica **antes** de investir ciclo no negócio.*

- {{risco}} — {{como checar}}.

## 6. Estratégia de obtenção da lista

### O registro mínimo

Um lead só conta quando tem **{{m}} dos {{n}} campos**:

`{{campo}}` · `{{campo}}` · **`{{campo que qualifica}}`** · …

*Marque em negrito os campos que qualificam — sem eles não dá para fazer a conta antes da reunião.*

### Rota A — {{nome}} ({{faz sozinho · depende de terceiro}}, ~{{tempo}})

1. {{passo}}
2. {{passo}}

**Rendimento esperado:** ~{{nomes brutos}} → ~{{qualificados}} após os filtros.

### Rota B — {{nome}}

*A rota mais lenta e mais precisa — normalmente um intermediário que já tem o dado (contador,
associação, parceiro).*

### O gargalo desta tese

> *O campo decisivo que não é público, e como contorná-lo. Diga se as rotas rodam em paralelo.*

### Fontes complementares

| Fonte | O que entrega |
|---|---|
| {{fonte}} | {{o que ela dá, e o cuidado que exige}} |

## 7. Nota da tese

Régua ancorada no [`README.md`](./README.md#passo-7--dar-a-nota), com as âncoras que o consultor fixou.

| Critério | Nota | Por quê |
|---|---|---|
| Universo | {{1–5}} | |
| **Listabilidade** ⚡ | {{1–5}} | |
| Aderência | {{1–5}} | *qual credencial e qual rede do consultor abrem esta porta* |
| **Força da aritmética** ⚡ | {{1–5}} | |
| Ciclo de decisão | {{1–5}} | |
| Ticket | {{1–5}} | |
| **Total** | **{{soma}}/30** | {{prioridade}} |

**Veto:** Listabilidade {{nota}} e Força da aritmética {{nota}} — {{passa · ⛔ vetada por ≤ 2}}.

## 8. O que falta para esta tese ir a campo

*Cada parâmetro ⚠️ e cada dependência aberta, uma por linha. Se existe uma pergunta de resposta
binária que decide se a tese existe (ex.: a carta pode ser usada para aquele fim?), destaque-a aqui.
Se a tese está vetada, escreva as **condições de reativação** — e não reescreva a tese antes que
elas se cumpram.*

- ⚠️ {{pendência}}
