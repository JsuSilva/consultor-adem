# Sobra de crédito na carta de imóvel usada para construção

> Pesquisado e congelado em **2026-10-16**, para dizer se a premissa de uma peça de campo — "a sobra
> do crédito, quando a obra custa menos que a carta, é liberada em dinheiro no habite-se" — se
> sustenta em fonte. Vale para qualquer administradora: o detalhe da construção (liberação por
> etapa, retenção, garantia) está no regulamento do seu grupo, não aqui. **Nenhum percentual de
> taxa, comissão ou fundo de reserva.** O único percentual citado (10%) é limite público da
> Resolução BCB 285/2023. Complementa `03-normativos-bcb-consorcio-resolucao-285-2023.md` §9 (sobra
> na **compra** de bem mais barato), que não tratava de construção.

## 0. Pergunta, em termos verificáveis

Em carta de crédito de **imóvel** usada para **construção** (opção do art. 15, I, "c", da Res. BCB
285/2023), quando o contemplado não usa todo o crédito porque a obra custou menos que a carta, o que
a norma pública e o contrato-padrão de uma administradora dizem sobre o saldo não usado:

1. é liberado ao consorciado em dinheiro, e **quando** (habite-se, averbação, outro marco)?
2. abate o saldo devedor (parcela ou prazo)?
3. se perde (volta ao grupo, o consorciado segue devendo o saldo cheio)?

## 1. Fontes — qualificação

| Fonte | Natureza | Acesso | Usada para |
|---|---|---|---|
| **Resolução BCB nº 285/2023**, texto vigente via API do portal do BCB: `https://www.bcb.gov.br/api/conteudo/app/normativos/exibenormativo?p1=Resolução%20BCB&p2=285` (VersaoNormativo 2; alterações listadas no próprio registro: só Res. BCB 362/2023, que **não** toca os arts. 15–18) | ✅ **Primária** (BCB) | 2026-10-16; JSON sha256 `93260b11…d2735` | arts. 2º (XIV, XV), 15, 17, 18, 26 |
| `static.poder360.com.br/2023/01/resolucao-bcb-consorcios-285-19jan2023-1.pdf` | ⚠️ Secundária (reprodução de terceiro) | 2026-10-16; sha256 `0db8cf60…fc30` | só como conferência cruzada: **idêntica** ao BCB nos arts. 15 e 18 |
| **Lei nº 11.795/2008**, `https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11795.htm` | ✅ **Primária** | 2026-10-16; sha256 `bc35ddda…1f4c` | busca por "construção", "reforma", "diferença", "habite-se", "saldo devedor": **zero ocorrências**; art. 14 |
| Regulamento-padrão de imóveis (contrato de adesão) e manual do contemplado publicados por **uma administradora** no próprio site | ✅ **Primária, camada da administradora** — contrato-padrão, **não** o regulamento/proposta de um grupo específico | 2026-10-16 | o que um regulamento de imóveis costuma trazer sobre construção — §3 |
| Bradesco Consórcios, *Guia do contemplado — imóveis* (PDF de fev/2023, **anterior** à vigência da Res. 285): `https://banco.bradesco/html/classic/produtos-servicos/consorcios/assets/pdf/guia_contemplado_imoveis.pdf` | **Primária de outra administradora; comparativo, não fonte de regra geral**, e pré-Res. 285 | 2026-10-16; sha256 `c93058de…a1d9` | só para mostrar o que outra grande administradora faz — p. 10 |
| Santander Consórcios, *Fui contemplado, e agora? Imóvel* (PDF; data de 12/05/2026 só pelo nome do arquivo): `https://cms.santander.com.br/sites/WPS/documentos/arq-fui-contemplado-e-agora-imovel/26-05-12_165821_fui-contemplado-e-agora-imovel-2704.pdf` | idem (outra administradora; comparativo) | 2026-10-16; sha256 `f2af08fd…8f16` | só comparativo: confirma que sobra pode ser paga em espécie com a cota quitada e que, após formalizada a compra, a sobra não vira obra (ver §6, item 7) |

Não consultei, por regra: blog de corretora, site de concorrente comercial, material de venda.

## 2. O que a norma pública diz

**Lei 11.795/2008.** Nenhum artigo trata de construção, reforma ou da destinação de diferença entre
crédito e preço (busca textual no texto consolidado: zero ocorrências). O que toca o caso é só
garantia: art. 14, §3º ("quando, na data de utilização do crédito, o bem estiver sob produção,
incorporação ou situação análoga definida pelo Banco Central do Brasil" admitem-se garantias reais ou
pessoais sem vinculação ao bem), §4º (garantias complementares proporcionais às prestações vincendas)
e §5º, II (a administradora indeniza o grupo por "liberação de garantias enquanto o consorciado não
tiver quitado sua participação no grupo").

**Res. BCB 285/2023, art. 15, I, "c"** — o crédito pode ser usado em:
> "bem imóvel ou conjunto de bens imóveis, construídos ou na planta, inclusive terreno, com opção de
> uso para construção ou reforma, nos termos previstos no contrato, se o contrato tiver como objeto
> bem imóvel ou conjunto de bens imóveis"

A norma **não** traz regra própria de liberação por etapa/medição nem de saldo não usado em obra: a
modalidade construção é uma das opções do mesmo inciso de aquisição, e o detalhe fica "nos termos
previstos no contrato".

**Art. 17.** O crédito disponibilizado "deverá ser acrescido de rendimentos líquidos financeiros
proporcionais ao período em que o respectivo valor for aplicado [...] até a sua efetiva utilização
pelo consorciado." (o crédito não usado rende a favor do consorciado).

**Art. 18, §3º** (texto literal, idêntico na fonte BCB e no poder360):
> "Caso o consorciado contemplado adquira bem, conjunto de bens, serviço ou conjunto de serviços com
> preço inferior ao valor do respectivo crédito, a diferença deve ser utilizada, a critério do
> consorciado, para:
> I - pagamento de obrigações financeiras, vinculadas ao bem ou ao serviço, observado o limite total
> de 10% (dez por cento) do valor do crédito objeto da contemplação, relativamente às despesas com
> transferência de propriedade, tributos, registros cartoriais, instituições de registro, seguros ou
> tarifas ou ressarcimento de despesas em favor da administradora de consórcio;
> II - quitação das prestações vincendas na forma estabelecida no contrato; ou
> III - devolução em espécie ao consorciado ou por meio de transferência para conta de depósitos ou
> conta de pagamento de sua titularidade, mediante quitação das obrigações financeiras para com o
> grupo e a administradora de consórcio."

**Art. 18, caput.** A administradora paga "o bem [...] ou o serviço [...] escolhido pelo consorciado
diretamente ao vendedor ou fornecedor do bem ou ao prestador do serviço". **§1º** (a única via de
dinheiro ao titular que **não** depende de quitação): "haver pago ou antecipado com recursos
próprios algum valor para aquisição do bem [...] a ele é facultado receber o valor correspondente
em espécie [...] deduzindo-o do valor do crédito, observadas as disposições contratuais". **§2º, I:**
a comunicação formal deve conter a identificação do vendedor, fornecedor ou prestador e "as
condições de pagamento acordadas" com ele.

**Art. 15, §2º.** Crédito **integralmente** não utilizado: em espécie após 180 dias da contemplação,
"mediante quitação das obrigações financeiras para com o grupo e a administradora" (hipótese
distinta da sobra; já registrada em `03-…` §9).

**Art. 26.** Saldo devedor "compreende o valor não pago das prestações e das diferenças negativas de
prestações, bem como quaisquer outras obrigações financeiras do consorciado não pagas".

**Art. 2º, XIV, "d", e XV.** O contrato deve dispor sobre "os procedimentos e prazos" do pagamento
ao fornecedor/prestador e sobre "as garantias que serão exigidas".

**Leitura que a norma permite, e o limite dela.** O art. 18, §3º fala em "adquira bem [...] ou
serviço com preço inferior ao valor do crédito"; o art. 15, I, "c" põe a construção dentro das
opções de aquisição. A aplicação do §3º à sobra de **obra** é, portanto, a leitura natural, **mas é
leitura**: nenhum dispositivo da Resolução diz expressamente "sobra de construção". 🔴 Ponto a
confirmar com a administradora (§6, item 1).

## 3. O que um contrato-padrão de imóveis diz — confirme no regulamento do seu grupo

O regulamento-padrão de imóveis lido nesta rodada (público no site da administradora que o emite)
traz, sobre construção, o que segue. **É um contrato, não a norma:** o do seu grupo pode ser
diferente, e é ele que vale.

- **Diferença de preço:** se o bem custar menos que o crédito, a diferença, a critério do
  consorciado, vai para a compra de outro bem (com garantia), para pagar as prestações vincendas
  **na ordem inversa, a contar da última**, ou volta em espécie **após 180 dias da contemplação, se o
  débito junto ao grupo estiver integralmente quitado**. As despesas do art. 18, §3º, I podem ser
  deduzidas do crédito.
- **Liberação em parcelas:** na construção, o crédito é liberado conforme a execução do cronograma
  físico-financeiro, vistoriado por empresa designada pela administradora, depois de constituída a
  garantia (hipoteca ou alienação fiduciária do terreno ou do imóvel).
- **Terreno:** deve ser do consorciado e estar quitado; o mesmo regulamento admite usar parte do
  crédito para comprar o terreno, sem regra visível que concilie os dois dispositivos.
- **Retenção:** uma fração do crédito fica retida **até a apresentação da averbação da construção no
  registro de imóveis**.
- **Seguro do imóvel:** obrigatório pelo prazo remanescente da dívida; na construção, permanece após
  a averbação.
- **Garantia:** não é liberada enquanto não houver quitação do saldo devedor.
- **Despesas do consorciado:** incluem avaliação do imóvel ou medição de obra.
- **Crédito não aprovado na análise jurídico-cadastral:** só pode ser retirado após a total quitação
  do saldo devedor.

**"Habite-se" não aparece no regulamento lido** (busca textual no documento inteiro). O marco
documental da obra que o contrato cita é a **averbação da construção no registro de imóveis**.

## 4. Resposta às três possibilidades

### 4.1 Possibilidade 1 — "liberado em dinheiro depois da conclusão da obra / habite-se / averbação"

**Parcialmente sustentada: existe devolução em espécie, mas o gatilho é outro.**

- A devolução em espécie da diferença **existe** — art. 18, §3º, III (Res. 285) e o regulamento
  lido.
- O gatilho, nas duas fontes, **não é a conclusão da obra, nem o habite-se, nem a averbação**: é a
  **quitação das obrigações com o grupo** (norma) / **débito integralmente quitado, somado a 180 dias
  da contemplação** (regulamento lido), que o mesmo regulamento lê como "total quitação do saldo
  devedor". Em leitura literal, isso significa **só no fim do plano**, ou antes se o consorciado
  quitar o saldo.
- ⚠️ A expressão "quitação das obrigações financeiras para com o grupo" (art. 18, §3º, III) é
  ambígua na norma (parcelas vencidas × saldo devedor inteiro). Quem desambigua, no contrato-padrão
  lido, é o regulamento — "integralmente quitado". Não há, nas fontes, hipótese de entrega em
  dinheiro no marco do habite-se.
- A averbação aparece, mas como gatilho de **outra** coisa: a liberação da fração **retida** do
  crédito e a continuidade do seguro. O regulamento não diz o que acontece com o retido se a obra não
  o consumir.
- Antes de qualquer devolução, a sobra é **reduzida** pelas despesas dedutíveis do art. 18, §3º, I
  (até 10% do crédito: transferência, tributos, registros, seguros, tarifas, ressarcimento à
  administradora) e pelas despesas do consorciado previstas no contrato (avaliação, medição de obra
  etc.). A "sobra" bruta não é a sobra entregável.

### 4.2 Possibilidade 2 — "abate o saldo devedor (reduz parcela ou prazo)"

**Sustentada, com uma precisão sobre o efeito.**

- Art. 18, §3º, II: "quitação das prestações vincendas na forma estabelecida no contrato" — a
  escolha é do consorciado.
- Regulamento lido: pagar as prestações vincendas "na ordem inversa a contar da última".
- Efeito: pagar da última para a frente **elimina as últimas parcelas** — leitura literal é de
  **redução de prazo, não de valor da parcela**. ⚠️ Isto é inferência do verbo "ordem inversa"; o
  regulamento não diz "reduz o prazo" nem "reduz a parcela". Não afirmar "reduz a parcela". Confirme
  a forma no contrato do seu grupo.
- É a rota que **não depende de nenhum marco da obra** (nem de quitação total): vale desde que a
  sobra exista.

### 4.3 Possibilidade 3 — "se perde: volta ao grupo e o consorciado segue devendo o saldo cheio"

**Descartada pelo texto lido.**

- Nenhum dispositivo da norma (art. 18, §3º) nem do regulamento lido destina a sobra ao grupo. O
  verbo é "**deve** ser utilizada, **a critério do consorciado**", entre as opções acima.
- Ressalva honesta: **nenhuma fonte diz o que ocorre se o consorciado não escolher nenhuma
  das opções** (silêncio), nem o destino do retido não consumido pela obra. Esse silêncio não
  autoriza afirmar "perde-se"; também não autoriza afirmar que fica à disposição.
- Comparativo, **não regra geral**: o *Guia do contemplado* do Bradesco (p. 10, pré-Res. 285) diz
  "Se existir sobra do valor da sua carta de crédito, será reduzido do saldo devedor [...] Caso seu
  consórcio esteja quitado, o valor será devolvido na sua conta" e que, em construção e reforma,
  paga "o menor valor, considerando a carta de crédito e o valor apurado para conclusão da obra".
  Mostra o mesmo padrão (abate primeiro, dinheiro só com cota quitada), em outra administradora.

## 5. Veredito sobre a premissa ("devolvida em dinheiro no habite-se")

**Não pode ir a campo sem ⚠️ — e, como está escrita, o texto lido a contradiz no gatilho.**

1. "Em dinheiro": **sustentado**, com condição (art. 18, §3º, III; regulamento lido).
2. "No habite-se" (ou na conclusão da obra): **sem fonte**. Habite-se não consta de nenhuma
   fonte; o marco do contrato é a averbação, e só para o **retido**.
3. A condição real encontrada é **quitação integral do débito com o grupo (+180 dias, no regulamento
   lido)**. Em leitura literal, dinheiro livre na conclusão da obra só ocorre se o consorciado já
   tiver quitado o saldo.
4. A sobra bruta ainda sofre dedução das despesas dedutíveis antes de ser devolvível.
5. Redação que as fontes sustentam, a título de insumo (decisão de redação é do consultor): a sobra
   tem três destinos à escolha do consorciado — pagar despesas vinculadas à obra (até 10% do
   crédito), abater as últimas parcelas, ou voltar em dinheiro **quando o débito com o grupo estiver
   quitado** (no contrato-padrão lido, também após 180 dias da contemplação).
6. ⚠️ O que as fontes **não** sustentam em nenhuma peça: "libera no habite-se", "sobra volta
   quando a obra termina", "o que não gastar na obra vai para o seu bolso".

## 6. O que ficou sem resposta (🔴/🟡) e como fechar

| # | Lacuna | Por que não fechei | Como fechar |
|---|---|---|---|
| 1 | 🔴 O regulamento aplica o art. 18, §3º à **sobra de obra** expressamente? (a cláusula de diferença fala em "bem a adquirir"; a de construção só trata da liberação em parcelas) | Nenhuma cláusula diz "sobra de construção"; aplicação é leitura | Pergunta escrita à administradora (operações/crédito) |
| 2 | 🔴 O que acontece com o **crédito liberado em parcelas que a obra não consumiu** quando a obra termina (volta ao saldo da carta? fica rendendo? exige o consorciado pedir?) | O regulamento lido não diz | Idem |
| 3 | 🔴 Destino do **retido** se a obra custar menos que o crédito menos o retido | Cláusula silente | Idem |
| 4 | 🔴 **Regulamento e Proposta de Adesão do seu grupo**: o lido é contrato-padrão. Pode haver versão posterior ou condição específica do grupo (art. 2º da Res. 285 manda o contrato dispor sobre o pagamento ao fornecedor) | Contrato privado do grupo; não está na web | Pedir à administradora o regulamento do grupo e a versão aplicável à data de adesão |
| 5 | 🟡 **Política de crédito vigente** e **empresa/tabela de medição de obra** | Documento interno | Contrato com a administradora |
| 6 | 🟡 Terreno exigido "de propriedade do consorciado e devidamente quitado" × uso de "parte do valor do crédito para aquisição do terreno": os dois dispositivos coexistem sem regra de conciliação visível | Texto do contrato, sem norma pública que decida | Perguntar à administradora (relevante quando a carta compra o terreno) |
| 7 | 🟡 Grandes administradoras: em Santander (arquivo de 12/05/2026) e Bradesco (fev/2023) não achei regra específica de sobra de **obra** além do §4.3; o Santander diz apenas, sem distinguir obra, que a cota quitada recebe a diferença em espécie | Fonte não pública ou inexistente | Não prosseguir por web |

Nada disto está na web: lacunas 1–5 vêm do regulamento do grupo e de interlocução com a
administradora.

## 7. Cruzamentos com o repo

1. **`03-normativos-bcb-consorcio-resolucao-285-2023.md`, "Art. 15 — Uso do crédito", citado como
   "Texto literal"** não confere com o texto oficial do BCB lido em 2026-10-16 (a API do portal, com
   a versão vigente da Resolução). O arquivo 03 transcreve "Art. 15. O crédito objeto do contrato de
   participação em grupo de consórcio deve ser utilizado exclusivamente para: I - aquisição, no
   fornecedor que melhor convier [...]"; o texto oficial é "Art. 15. Os recursos do grupo de
   consórcio podem ser utilizados para atender exclusivamente as seguintes finalidades: I - aquisição
   pelo consorciado contemplado, em vendedor ou fornecedor [...], observado o disposto no art. 18,
   de: [alíneas a–e] [...]; V - outros pagamentos". A **substância usada pelo repo se mantém** (II:
   quitação total de financiamento de mesma categoria; §1º; §2º: espécie após 180 dias, se o
   crédito não foi usado, mediante quitação), mas a citação entre aspas **não é literal**. O arquivo
   03 é congelado e não foi reescrito; acrescentar nele a nota de correção é decisão do consultor.
2. **`03-…` §9.3** ("enquanto restarem prestações vincendas em aberto, a diferença não é entregue
   como dinheiro livre"): **confirmado**, e agora estendido à construção (§4.1 acima). Sem
   contradição.
3. **`conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`, Regra 5.2** (art.
   15, §2º): o dispositivo existe com o conteúdo citado. Sem contradição. Esta pesquisa dá insumo
   para ampliar a régua à sobra de construção — decisão do consultor.

---

# RODADA 2 — 2026-10-16 (acréscimo; o texto acima não foi alterado)

> Pergunta corrigida: na rodada 1 ela foi formulada como "a obra custou menos que a carta". O
> gatilho da cláusula de diferença é "bem a adquirir de **preço** inferior ao crédito"; em
> construção, o bem é o imóvel pronto e a obra é o custo. Esta rodada volta às mesmas fontes com
> cinco perguntas. As seções 4 a 6 acima continuam valendo **para a pergunta que respondem**
> (destino da diferença quando o que se paga é menor que o crédito); esta rodada diz se essa
> pergunta é a certa e o que cobre o caso em que o imóvel pronto vale mais que o crédito. Em cada
> item: **A fonte diz** (literal ou fato do texto) e **Inferência** (separadas, sempre).

## R2.0 Resposta curta

1. **Q1 — fontes não dizem** se a comparação "preço × crédito" é contra o custo da obra ou contra o
   valor do imóvel pronto. A leitura mais coerente com o texto é contra o **custo pago a terceiros**
   (inferência). Mesmo se a cláusula de diferença não disparar, **nenhuma outra cláusula entrega o
   remanescente em dinheiro sem quitação** (Q4/Q5).
2. **Q2 — o contrato-padrão é silente** sobre cronograma menor que o crédito, cronograma igual ao
   crédito e economia de obra.
3. **Q3 — a cláusula de retenção é silente** sobre a quem o retido é pago e para onde vai se o
   cronograma estiver esgotado. O texto **não sustenta** "o retido chega ao titular na averbação" e
   **não exclui** (silêncio).
4. **Q4 — nenhuma cláusula condiciona a liberação do crédito à suficiência da garantia.** A única
   condição de dinheiro ao titular é a quitação. Nenhuma cláusula liga a liberação da garantia à
   liberação do crédito além de os dois dependerem, cada um por si, da quitação do saldo devedor.
5. **Q5 — não encontrei terceira hipótese na norma.** Crédito parcialmente utilizado em obra, com
   resultado maior que o crédito, é **lacuna** da Resolução; a norma remete ao contrato (art. 2º,
   XIV, "d", e XV).
6. **Conclusão:** o contrato-padrão **não resolve** o caso. É preciso o **regulamento e a proposta
   do seu grupo** e as respostas da administradora listadas em §R2.6.

## R2.1 Q1 — a cláusula de diferença se aplica quando o imóvel pronto vale mais que o crédito?

**A fonte diz.**
- Regulamento lido: o contemplado pode optar por construção ou reforma "desde que apresentadas às
  garantias compatíveis com o valor do crédito de sua cota". Se o bem for de preço **superior** ao
  crédito, o consorciado fica responsável pela diferença; se for **inferior**, valem os destinos do
  §3.
- A palavra "preço" **não é definida** no regulamento para o caso de construção. Nenhuma cláusula
  compara o crédito com a avaliação do imóvel resultante; "avaliação" aparece só para análise de
  garantia, discordância sobre o preço do imóvel e garantias complementares.
- Res. BCB 285/2023, art. 18, caput e §2º, I (§2): pagamento direto ao vendedor, fornecedor ou
  prestador, nas "condições de pagamento acordadas" com ele. A norma **não define** "preço" para
  construção.
- Prática descrita pela administradora cujo regulamento foi lido (material comercial, ⚠️ descreve
  prática, **não é fonte de regra**): ela "paga diretamente os profissionais e fornecedores
  escolhidos", "liberando cada pagamento conforme o andamento da obra".
- Comparativo (Bradesco, p. 10, fev/2023, outra administradora): "Nos processos de construção e
  reforma, pagaremos o menor valor, considerando a carta de crédito e o valor apurado para conclusão
  da obra no estudo de viabilidade" — compara o crédito com o **custo apurado da obra**.

**Inferência.**
- O que a administradora efetivamente paga a terceiro (prestador da obra, vendedor do terreno) é o
  custo; a leitura de "preço" mais próxima da mecânica do art. 18 é o **valor pago ao
  fornecedor/prestador**, não o valor de mercado do imóvel concluído.
- A leitura alternativa (preço = valor do imóvel pronto) faria a cláusula do preço superior incidir
  em quase toda construção bem-sucedida e atribuiria ao consorciado a "diferença" entre o valor do
  imóvel e o crédito. Isso não corresponde a nenhuma obrigação descrita no contrato.
- Nessa leitura, "imóvel pronto vale mais que o crédito" é **irrelevante** para o gatilho: o que
  importa é o custo pago × crédito. É leitura; **as fontes não dizem**.
- Mesmo que o gatilho **não** ocorresse, o contrato não traz outra cláusula para o remanescente que
  o entregue em dinheiro sem quitação (ver Q4 e Q5).

**Resposta:** as fontes não dizem contra o quê se faz a comparação. 🔴 Pergunta 1 à administradora
(§R2.6).

## R2.2 Q2 — crédito liberado por cronograma que a obra não consumiu

**A fonte diz.**
- Regulamento lido: o consorciado "terá os valores correspondentes ao seu crédito liberados em
  parcelas, conforme a execução do cronograma físico financeiro da obra devidamente vistoriado". O
  verbo está na voz passiva; "valores correspondentes ao seu crédito" não esclarece se é o crédito
  inteiro ou o total do cronograma aprovado.
- Cronograma e alvará são apresentados pelo consorciado junto com as certidões; o manual do
  contemplado lido pede cronograma físico-financeiro "assinado por engenheiro e consorciado, com
  endereço do imóvel e constando o registro no CREA MODELO CEF" — "modelo CEF" é o formato do
  documento; não importa regra de financiamento Caixa.
- **Busca textual no regulamento inteiro** (termos: cronograma, economia, excedente, remanescente do
  crédito, nota fiscal, empreit, aditivo): **nenhuma cláusula** trata de (a) cronograma menor que o
  crédito, (b) cronograma igual ao crédito, (c) economia de obra durante a execução, (d) alteração
  do cronograma. O regulamento e o art. 17 dizem apenas que o crédito não utilizado fica aplicado,
  com rendimento líquido a favor do consorciado.

**Inferência.**
- Cronograma **menor** que o crédito: o texto não diz; a cláusula de diferença (se lida como custo,
  Q1) é a única que dá destino à diferença, e só com as condições do §4.1.
- Cronograma **igual** ao crédito: não sobra nada a destinar no desenho original; economia
  **durante** a obra e aditivo de cronograma ficam sem regra.

**Resposta:** o contrato-padrão não diz. 🔴 Perguntas 3 e 6 (§R2.6).

## R2.3 Q3 — a fração retida até a averbação

**A fonte diz.**
- A cláusula de retenção (uma fração do crédito retida "até a apresentação da averbação da
  construção no registro de imóveis") é a **única** menção a retenção em todo o regulamento lido
  (busca textual).
- A cláusula **não diz** a quem é pago o retido (titular, prestador, contra nota fiscal, conforme
  cronograma) nem que documento, além da averbação, o libera, nem o destino se o cronograma estiver
  esgotado ou se a obra custar menos que o crédito menos o retido.
- Res. 285, art. 18, caput: pagamento "diretamente ao vendedor ou fornecedor [...] ou ao prestador
  do serviço". Art. 18, §1º: o reembolso ao titular depende de ele ter pago do próprio bolso **após a
  contemplação**, o que não é a hipótese do retido.

**Inferência.**
- Pela estrutura (liberação em parcelas; retenção de fração do crédito) e pelo art. 18, caput, o
  retido é lido como **parcela final do cronograma**, paga ao prestador. Se for isso, a obra termina
  e o último pagamento só ocorre depois da averbação: o contrato não diz como a última etapa é
  custeada até lá.
- Se o cronograma já estiver esgotado, **não há texto**. Se o retido não for consumido pelo
  cronograma, ele integraria a "diferença", com as condições de §4.1 (inferência).
- A hipótese "o retido chega ao titular na averbação" **não tem apoio no texto** e não é excluída
  expressamente. Esgotei o texto: é silêncio.

**Resposta:** 🔴 Pergunta 4 (§R2.6).

## R2.4 Q4 — a garantia completa muda alguma coisa?

**A fonte diz** — o que liga crédito e garantia, e o que cada ponto condiciona:

| Fonte | O que condiciona | Condição |
|---|---|---|
| Regulamento lido | **uso** do crédito | garantias "compatíveis com o valor do crédito de sua cota" — **antes** de liberar; a escolha da garantia compete à administradora |
| Regulamento lido | liberação em parcelas | **após** a escritura/contrato de hipoteca ou alienação fiduciária do terreno ou do imóvel, a favor da administradora |
| Regulamento lido | liberação do crédito | certidões; aprovação jurídico-cadastral; pagamento das obrigações **atrasadas** |
| Regulamento lido | **dinheiro** ao consorciado (sobra / crédito retirado) | "débito junto ao grupo integralmente quitado" / "total quitação do saldo devedor" |
| Regulamento lido | **liberação da garantia** | a garantia serve "para garantir o pagamento das prestações vincendas", sem liberação "enquanto não houver quitação do saldo devedor" |
| Regulamento lido | garantias **complementares** | perduram enquanto houver saldo devedor superior à avaliação do imóvel gravado — única comparação explícita avaliação × saldo devedor |
| Regulamento lido | caso de várias cotas | a garantia "deve cobrir o saldo devedor presente de todas as cotas contempladas" |
| Manual do contemplado lido | cancelamento da alienação fiduciária | "Após a quitação do saldo devedor", com Termo de Liberação |
| Lei 11.795, art. 14, §1º, §3º, §5º, II | garantia | recai sobre o bem adquirido; garantias sem vinculação ao bem quando "o bem estiver sob produção, incorporação ou situação análoga"; a administradora indeniza o grupo por "liberação de garantias enquanto o consorciado não tiver quitado sua participação" |

- **Nenhuma cláusula condiciona liberação de crédito à suficiência da garantia pós-obra.** Também
  nenhuma a dispensa.
- **Nenhuma cláusula liga a liberação da garantia à liberação do crédito.** Cada uma depende,
  separadamente, da quitação do saldo devedor. O ponto em comum é a quitação, não a suficiência da
  garantia.
- Res. 285, art. 26 (§2): saldo devedor inclui "quaisquer outras obrigações financeiras do
  consorciado não pagas". O art. 18, §3º, III diz "quitação das **obrigações financeiras**" (e não
  "saldo devedor"). A norma não esclarece se isso é saldo devedor inteiro ou só o vencido; quem fecha
  como saldo inteiro é o regulamento lido. Não localizei manifestação do BCB sobre esse ponto.

**Inferência.**
- A tese "concluída a obra e feita a averbação, a garantia cobre a exposição, logo o remanescente
  iria ao titular" é um **argumento de risco coerente**, mas **não é a regra escrita**: o contrato
  escolheu a **quitação** como gatilho, não a suficiência da garantia.
- A norma, por ser ambígua em "obrigações financeiras", não proíbe nem exige a leitura mais
  restritiva do regulamento. Se a administradora aceita a leitura mais favorável, ela precisa
  constar do regulamento do grupo ou de política de crédito (§R2.6, perguntas 6 e 7). Não julgo se a
  cláusula do regulamento é compatível com a norma; isso é questão jurídica fora do que as fontes
  respondem.

**Resposta:** a garantia completa **não altera** o que o contrato-padrão diz. Pode ser pedida como
tratamento diferenciado, não afirmada como regra.

## R2.5 Q5 — art. 15, §2º × art. 18, §3º: existe terceira hipótese?

**A fonte diz.**
- Art. 15, caput: os recursos do grupo "podem ser utilizados para atender **exclusivamente** as
  seguintes finalidades", e o inciso V fecha com "outros pagamentos, nos casos de que tratam os arts.
  18, § 3º, e 22" (o art. 22 é o fundo de reserva).
- Art. 15, §2º: crédito em espécie, "caso ainda não tenha utilizado o respectivo crédito", após 180
  dias, "mediante quitação das obrigações financeiras".
- Art. 18, §1º (reembolso de recursos próprios pagos após a contemplação) e §3º (preço inferior ao
  crédito: três destinos).
- Art. 2º, XIV, "d", e XV: o contrato deve dispor sobre "os procedimentos e prazos" do pagamento ao
  fornecedor/prestador e sobre "as garantias que serão exigidas".

**Inferência.**
- O §2º, na letra, descreve crédito **não utilizado**; crédito parcialmente utilizado em obra por
  etapas não se encaixa literalmente.
- O §3º serve se "preço" for o custo pago (Q1). Se o resultado supera o crédito, isso não o afeta.
- Pela exclusividade do caput, a Resolução não autoriza pagar ao consorciado fora de §1º, §2º, §3º
  (e dos casos de excluído e fundo de reserva). **Não encontrei terceira hipótese.**
- **É lacuna** da norma para o caso "crédito parcialmente utilizado, liberado por etapas, resultado
  maior que o crédito". A Resolução entrega ao contrato (art. 2º, XIV e XV), e o contrato-padrão é
  silente (§R2.2, §R2.3).

## R2.6 O que perguntar à administradora (lista exata) e o que pedir

**Pedir por escrito:**
1. Regulamento (cláusulas gerais) e Proposta de Adesão do **seu grupo**, na versão aplicável à data
   de adesão, e confirmar se existe versão posterior à publicada no site.
2. Política de crédito vigente e a minuta do contrato de liberação do crédito para construção.

**Perguntar:**
1. Na construção, a comparação de preço com o crédito é entre o crédito e o **custo** (cronograma
   aprovado/pago) ou entre o crédito e o **valor do imóvel pronto**?
2. O crédito é pago ao **titular** ou **direto ao prestador** (art. 18, caput)? Há reembolso ao
   titular de etapa paga com recursos próprios (art. 18, §1º)?
3. O cronograma pode ser **menor** que o crédito? Se for, o que acontece com a parte nunca liberada
   ao fim da obra? Há regra para **economia** durante a execução e para **aditivo** de cronograma?
4. A fração retida até a averbação é paga a quem, contra qual documento (só a averbação?), e para
   onde vai se o cronograma estiver esgotado ou se a obra custar menos que o crédito menos o retido?
5. Como a última etapa da obra é custeada até a averbação, se o retido só sai depois dela?
6. "Débito integralmente quitado" inclui as **prestações vincendas**? O titular pode
   **antecipar/amortizar** o saldo para destravar o remanescente em dinheiro? A sobra pode ser
   aplicada nas últimas parcelas e o que restar, devolvido?
7. Existe política em que o remanescente seja liberado com base na **suficiência da garantia**
   (avaliação pós-averbação ≥ saldo devedor), em vez da quitação?
8. Quais despesas contam no limite de 10% (art. 18, §3º, I): medição de obra, vistoria por etapa,
   seguro, escritura, registro, ITBI do terreno?
9. Com terreno comprado com o crédito, em que ordem e sob que garantia saem o pagamento do terreno e
   as parcelas da obra?
10. Rendimentos do crédito ainda não liberado (art. 17): quando e como entram?

Nada disto está na web: vem do regulamento do grupo e da administradora.

## R2.7 Efeito sobre a rodada 1

1. §4.1 a §4.3 e §5 continuam corretos para o que respondem. Nenhuma fonte desta rodada sustenta
   "habite-se" como marco; o único marco documental no contrato continua sendo a **averbação**.
2. O que muda: a pergunta "a cláusula de diferença se aplica?" fica **em aberto** (Q1), e o único
   caminho textual de dinheiro ao titular no marco da averbação (o retido) está **sem destinatário
   definido** (Q3).
3. Redação que as fontes **não** sustentam, além da lista da rodada 1: "a garantia completa libera o
   remanescente", "o retido vai para o titular na averbação", "a sobra é a diferença entre o valor do
   imóvel e o crédito".
4. Pistas não verificadas, só para a próxima rodada: um acórdão do TJPR mencionado em busca web
   interpretaria "recursos próprios" do art. 18, §1º de forma ampla; **não abri a fonte**.
