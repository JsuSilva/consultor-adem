# Teses — como o consultor organiza a venda

> **O coração comercial do repositório.** Aqui não se vende consórcio: aqui se demonstra, com
> aritmética, **em que situação concreta o consórcio é a melhor decisão de capital — e em quais não é.**
> Esta pasta traz o método e o modelo em branco ([`00-modelo-de-tese.md`](./00-modelo-de-tese.md)).
> As teses são do consultor: cada uma nasce da praça, da rede e das credenciais dele.

## O que é uma tese

Uma tese é a afirmação *"neste grupo de pessoas ou empresas, o consórcio é a melhor forma de
comprar este bem — e aqui está a conta"*. Ela só existe quando tem as três partes:

1. **Um gatilho observável de fora.** Um fato que se verifica **antes** do contato, sem falar com
   ninguém: opera em imóvel alugado há anos, tem frota em ciclo de renovação, disputa licitação. Se
   só dá para saber perguntando, não é gatilho — é descoberta.
2. **A aritmética feita antes do contato.** Os três caminhos — capital próprio, financiamento,
   consórcio — comparados num caso-referência, com a conta aberta e os parâmetros nomeados. O
   consultor chega à primeira conversa sabendo a resposta provável.
3. **O desqualificador obrigatório.** Onde o consórcio **perde** para aquele grupo. Tese sem "onde
   não vale" é folder com planilha — e é justamente a seção que faz um contador entregar a carteira
   dele e um cliente acreditar na conta.

## Por que tese, e não persona

Uma reunião que começa com "quero te apresentar o consórcio" é uma reunião de vendedor. Uma que
começa com *"você paga aluguel neste ponto há anos, está num regime em que isso não abate nada do
imposto — deixa eu te mostrar a conta dos três caminhos"* é uma reunião de consultor. **A diferença
não é postura, é preparo aritmético.**

A persona descreve **quem** a pessoa é — cargo, idade, renda, gosto. A tese descreve **em que
situação** ela está e **quanto essa situação custa**. Três diferenças práticas:

- **A persona não dá lista; a tese dá.** "Médico de 40 anos" é um perfil; "clínica em imóvel
  alugado, num regime em que o aluguel não deduz" é uma consulta que se roda em base pública.
- **A persona não traz conta; a tese já chega com ela.** O gatilho é o que alimenta o `calculista`
  antes da primeira mensagem.
- **A persona não sabe dizer não.** A tese tem desqualificador: sabe de antemão para quem o consórcio
  é a resposta errada — e dizer isso em voz alta é o que constrói credibilidade.

A mesma tese atende públicos muito diferentes — a cabeleireira que quer a própria sala e a clínica
que quer o próprio prédio têm o mesmo gatilho. Muda a linguagem, o tamanho e a prova (skill
`roteirista`); a tese não muda.

## Anatomia de uma tese (modelo obrigatório)

Toda tese tem exatamente estas seções — sem exceção. O modelo em branco está em
[`00-modelo-de-tese.md`](./00-modelo-de-tese.md).

1. **O gatilho** — o fato observável que qualifica, identificável **antes** do contato.
2. **A dor em uma frase** — dita na linguagem do cliente, não na do produto.
3. **A aritmética** — os três caminhos comparados, com a conta aberta e os parâmetros nomeados.
4. **O corte tributário** — em que regime a tese ganha, em qual enfraquece.
5. **⛔ Os desqualificadores** — **onde o consórcio perde.** Seção obrigatória, em partes que se
   usam em momentos opostos: **na lista** (checável antes do contato — poda antes de gastar tempo),
   **na reunião** (o que se diz em voz alta — é o que constrói credibilidade) e o **risco
   operacional** que se checa calado.
6. **Estratégia de obtenção da lista** — não uma tabela de fontes, mas o **método operacional**:
   qual o registro mínimo de um lead, por qual rota se chega a 100, qual o **gargalo de dado** daquela
   tese e como contorná-lo, e quanto tempo custa. Uma tese sem rota de lista não se executa.
7. **Nota da tese** — a pontuação que decide a prioridade (abaixo).
8. **O que falta para ir a campo** — cada parâmetro ⚠️, cada dependência aberta.

## Passo a passo — formular a própria tese

### Passo 1 — Achar o gatilho

Parta de uma situação que custa dinheiro todo mês e que se repete em muita gente: aluguel pago sem
formar patrimônio, bem que se renova em ciclo previsível, dívida cara, patrimônio que precisa ser
organizado. Escreva o gatilho como **fato**, não como perfil.

**Teste do gatilho:** dá para verificar sem falar com a pessoa? Se a resposta for "só perguntando",
volte — ou registre que a tese depende de um intermediário que já enxerga o dado (contador,
associação), e isso vai pesar na Listabilidade.

### Passo 2 — Escrever a dor em uma frase

Na linguagem de quem ouve, não do produto. O que dói raramente é o valor isolado; é a combinação —
caixa que sai, patrimônio que não se forma, imposto que não reduz, dependência de um terceiro.

### Passo 3 — Fazer a conta antes do contato

1. Monte um **caso-referência** típico do gatilho: valor do bem, custo mensal da situação atual,
   linha do produto, prazo.
2. Peça ao agente `calculista` os **três caminhos**, com os parâmetros de `config/consultor.json`
   (produto da administradora e taxas de mercado, com fonte e data):
   ```
   Consórcio       → custo total = C × (1 + ta + fr) + seguro + adesão      parcela = custo total ÷ n
   Financiamento   → parcela = C × [ i(1+i)^n ] ÷ [ (1+i)^n − 1 ]           custo total = parcela × n
   Capital próprio → custo = C + custo de oportunidade do capital imobilizado
   ```
3. Calcule **o que se compra ao esperar** — é a fronteira que decide:
   ```
   meses de espera comprados = (custo total do financiamento − custo total do consórcio) ÷ custo mensal da espera
   ```
   Contemplado antes desse mês, o consórcio custa menos que o financiamento mesmo pagando o custo da
   espera. Não se trata de o consórcio ser "mais barato" — trata-se de **quanto tempo de espera a
   diferença financia**.
4. Monte a tabela do **custo da espera por mês de contemplação** — todas as linhas são premissa,
   nunca previsão.
5. Parâmetro sem fonte documental fica ⚠️ e visível. **Nada de número de memória.**

### Passo 4 — Fazer o corte tributário

Para cliente PJ, o que muda o resultado não é só o custo bruto de cada caminho, mas **quanto de cada
custo retorna pela via fiscal**:

| Regime | Juros de financiamento | Aluguel | Taxa de administração |
|---|---|---|---|
| **Lucro Real** | Despesa financeira **dedutível** | Dedutível | Dedutível |
| **Lucro Presumido** | **Sem aproveitamento** — base presumida sobre a receita | **Sem aproveitamento** | Sem aproveitamento |
| **Simples Nacional** | **Sem aproveitamento** — tributação sobre a receita bruta | **Sem aproveitamento** | Sem aproveitamento |

No Lucro Real a dedutibilidade dos juros e a depreciação que começa com a posse **estreitam** a
vantagem do consórcio. Escreva em qual regime a sua tese vive e em qual ela enfraquece. ⚠️ Há
particularidades por anexo do Simples, atividade e composição da base — o enquadramento específico
de cada cliente se confirma com o contador dele.

### Passo 5 — Escrever os desqualificadores

Três listas:

- **Na lista** — o que se checa antes do contato e poda o lead: condição, limiar, como checar.
- **Na reunião** — o que se diz em voz alta. Pontos de partida que valem para quase toda tese:
  - **o bem é necessário em prazo definido e curto**, sem caixa para lance — o consórcio não entrega
    data; o financiamento entrega;
  - **Lucro Real com resultado tributável relevante** — a dedutibilidade reduz materialmente a vantagem;
  - **existe linha subsidiada acessível** com custo abaixo da fronteira do passo 3;
  - **a capacidade de pagamento não é estável** pelo prazo integral;
  - **o ativo é de giro rápido** — bem que será revendido logo não justifica plano longo.
- **Risco operacional — checar calado** — o que mata o negócio por fora da conta, como o cliente não
  passar na análise de crédito da contemplação.

Se algum desqualificador se aplica, a recomendação para aquele cliente é **contrária** ao consórcio.

### Passo 6 — Desenhar a rota de lista

1. Defina o **registro mínimo** de um lead: os campos, e quais deles qualificam (sem eles, não há
   conta antes da reunião).
2. Descreva a **Rota A** (o que o consultor faz sozinho, com fonte pública) e a **Rota B** (o que
   depende de intermediário), com o rendimento esperado de cada uma.
3. Nomeie o **gargalo de dado** — o campo decisivo que não é público — e como contorná-lo.
4. Estime quanto tempo custa chegar a 100 leads qualificados.

### Passo 7 — Dar a nota

Seis critérios, nota de 1 a 5, **máximo 30**. Nota sem âncora não é reproduzível, e nota não
reproduzível não prioriza nada.

| Critério | Pergunta | 1 | 3 | 5 |
|---|---|---|---|---|
| **Universo** | Quantos existem na praça? | poucos, cabem numa lista curta | algumas centenas | milhares |
| **Listabilidade** ⚡ | Monto uma lista de 100 sem falar com ninguém? | preciso conhecer alguém | dá para listar com trabalho | endereço/CNPJ/regime são públicos |
| **Aderência** | Minha credencial e minha rede abrem *esta* porta? | sou um estranho ali | acesso indireto | falo como par, tenho rede natural |
| **Força da aritmética** ⚡ | A conta é esmagadora ou apertada? | apertada, depende de premissa | vantagem clara | esmagadora, sobrevive a premissa ruim |
| **Ciclo** | Em quanto tempo decide? | muitos meses | um a dois meses | dias |
| **Ticket** | Cabe na meta de ticket do consultor? | bem abaixo da meta | na meta | bem acima da meta |

As âncoras de **Universo, Ciclo e Ticket** dependem da praça e da meta de cada consultor: fixe-as em
número antes de dar a primeira nota e use as mesmas para todas as teses — trocar a âncora entre uma
tese e outra desfaz a comparação.

**Aderência** mede o consultor, não o mercado: os outros cinco critérios medem o mercado; este mede
se as credenciais dele (`consultor.credenciais` na config) e a rede dele abrem aquela porta. É o
critério que faz a mesma tese valer mais para um consultor do que para outro.

**⚡ Regra de veto:** *Listabilidade* e *Força da aritmética* são **eliminatórias**. Se qualquer uma
das duas ficar **≤ 2**, a tese está fora — independentemente do total. Uma tese que não se consegue
listar não se executa, e uma cuja conta é apertada não sobrevive à primeira objeção. Sem essa regra a
soma esconde o veto: uma tese com Listabilidade 1 ainda somaria o bastante para parecer aceitável.

### Passo 8 — Montar o ranking

1. Liste as teses com nota e estado — **viva**, **vetada** (algum eliminatório ≤ 2) ou **pendente**
   (dependência aberta que decide se ela existe).
2. Ordene as vivas pela nota. Empate no topo se desempata pelo objetivo do período — a que converte
   melhor e a que fecha o número podem ser diferentes, e podem rodar juntas. O desempate é decisão
   do consultor.
3. Tese vetada **não se apaga**: fica na prateleira com as **condições de reativação** escritas
   (ex.: a Listabilidade sobe quando um canal de contadores passar a entregar a lista). Cumpridas as
   condições, a nota se refaz; antes disso, não se reescreve.
4. Mudou um parâmetro na config, refazem-se as contas das teses.

## As teses do consultor

| # | Tese | Gatilho identificável de fora | Nota | Estado |
|---|---|---|---|---|
| | | | | |

## Regras desta pasta

- **O desqualificador é obrigatório.** Tese sem "onde não vale" não entra.
- **Todo parâmetro nomeado e datado.** Taxa de administração, fundo de reserva, prazo e regra de
  lance vêm da administradora, via `config/consultor.json`; enquanto não vierem, ficam ⚠️ e visíveis.
- **Passa pelo filtro de compliance** antes de virar peça
  (`conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`): não prometer
  contemplação, não chamar de investimento, taxa de administração sempre aberta.
- **A conta é do cliente, não da venda.** Se a tese não fecha para aquele cliente, a resposta é "não
  compre" — e é isso que sustenta a indicação.
