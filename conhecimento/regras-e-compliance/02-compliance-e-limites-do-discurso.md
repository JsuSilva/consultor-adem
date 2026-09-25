# 02 — Compliance e limites do discurso

> **Régua de trabalho.** Escrita pelo `pesquisador` em **2026-09-01**, a partir das fontes públicas
> congeladas em `conhecimento/fontes-publicas/`. Vale como régua até o consultor revisá-la; o
> aprimoramento vem conforme a necessidade for surgindo.
>
> As 11 lacunas da tabela final **continuam abertas**: onde uma regra está marcada "⚠️ sem fonte
> normativa — premissa do repo", ela vale como régua de trabalho, não como citação de dispositivo.

## O que este documento é, e o que não é

É a **régua** do que pode e não pode ser dito numa peça de venda de consórcio — roteiro, simulação,
post, WhatsApp, slide, parecer. Não julga peça nenhuma: quem aplica a régua a uma peça concreta não
deve ser o mesmo que a escreveu, para não ser autor e juiz da mesma norma.

**Cada regra abaixo cita a fonte congelada em `conhecimento/fontes-publicas/` que a sustenta.** Onde
não achei base normativa direta, a regra vem marcada **⚠️ sem fonte normativa — premissa do repo, a
validar** — nunca inventei artigo, número de resolução ou alíquota para preencher a lacuna.

**Nenhum percentual de taxa de administração, fundo de reserva, comissão ou custo total aparece
neste documento.** Onde a regra precisa de um número real, ela diz *que* o número tem de ser
mostrado — o valor em si vive em `config/consultor.json` (`produto.*`), informado pelo consultor a
partir de documento da administradora. Índice de reajuste (qual índice, qual percentual), taxas de
mercado do crédito concorrente e CDI/Selic são insumo do `calculista` — este documento exige que a
peça **abra** o reajuste, não define qual índice usar.

---

## 1. O que é o produto, e como nomeá-lo

**Fonte:** `conhecimento/fontes-publicas/02-lei-11795-2008-sistema-de-consorcio.md` §1;
`05-cdc-publicidade-e-oferta-consorcio.md` §1 (art. 31).

**Art. 2º, Lei 11.795/2008** (literal): "Consórcio é a reunião de pessoas naturais e jurídicas em
grupo, com prazo de duração e número de cotas previamente determinados, promovida por
administradora de consórcio, com a finalidade de propiciar a seus integrantes, de forma isonômica,
a aquisição de bens ou serviços, **por meio de autofinanciamento**." **Art. 10, caput**: o contrato
é "instrumento plurilateral de **natureza associativa**".

**Regra 1.1.** Nomear sempre como "consórcio", "cota de consórcio" ou "carta de crédito de
consórcio". **Nunca** "investimento", "aplicação", "rendimento garantido" ou "reserva que
valoriza". Fonte: art. 2º (a finalidade legal é autofinanciamento para **aquisição**, não geração de
rendimento) + CDC art. 31 (nomear o produto pelo que ele é) + CDC art. 37, §1º (enganosidade se
induzir o consumidor a crer que é outra categoria de produto).

> ⚠️ **Sem fonte normativa literal — premissa do repo, a validar.** Nenhum artigo da Lei
> 11.795/2008 usa a frase "consórcio não é investimento" ou equivalente. A vedação acima é
> **inferência estrutural** do art. 2º (autofinanciamento × rendimento), não citação de dispositivo.
> Se este documento quiser usar essa frase pronta, falta uma fonte própria — material educativo do
> BCB ou da CVM que a use nessas palavras. Não encontrada em nenhuma das rodadas de pesquisa até
> aqui (`02-lei-11795...md` §7, item 1). Fica como pendência de pesquisa (ver fechamento).

**Regra 1.2.** Não usar "rendimento" ou "valorização" como benefício vendável do plano. A única
menção legal a rendimento é o **art. 24, §1º**: o crédito do contemplado é "acrescido de rendimentos
líquidos financeiros proporcionais ao período que ficar aplicado" — é a **remuneração do fundo
comum enquanto o dinheiro coletado aguarda uso**, mecânica de gestão do grupo, não promessa
individual ao consorciado. Confundir os dois numa peça — "seu dinheiro rende enquanto espera" dito
ao cliente como vantagem pessoal — é risco de enganosidade por omissão do que essa mecânica
realmente é (CDC art. 37, §1º).

**Regra 1.3.** O consórcio é regido pela Lei 11.795/2008 e supervisionado pelo Banco Central (art.
6º da Lei). Isso pode ser dito como fato — reforça credibilidade — mas não como sinônimo de "produto
financeiro regulado" no sentido de aplicação com garantia; a supervisão do BCB aqui é sobre
administração de grupo, não sobre rentabilidade prometida.

---

## 2. Contemplação — o que não se promete

**Fonte:** `02-lei-11795-2008...md` §2; `03-normativos-bcb-consorcio-resolucao-285-2023.md` §5;
`05-cdc-publicidade-e-oferta-consorcio.md` §1 (arts. 30 e 37).

**Regra 2.1.** Nunca afirmar data, mês, prazo ou probabilidade de contemplação — **inclusive por
implicatura** ("costuma sair em torno do mês X", "ele pode ser contemplado no mês 60" dito como
exemplo). Fonte: **art. 22, §1º** da Lei (contemplação por sorteio ou lance) + **art. 23** (a
contemplação está "condicionada à existência de recursos suficientes no grupo" — a lei não a
garante) + CDC **art. 30** (o que a peça diz integra o contrato) + **art. 37, §1º/§3º** (enganosidade,
inclusive por omissão, quanto a "quantidade" e "propriedades" do serviço).

> ⚠️ **Sem fonte normativa literal para "promessa por implicatura" como categoria própria —
> premissa do repo, a validar.** Não há dispositivo que use essa palavra. A vedação é leitura
> combinada dos artigos acima: se uma frase planta expectativa de prazo sem afirmá-lo literalmente,
> ela ainda "integra o contrato" pelo art. 30 do CDC e pode configurar indução em erro pelo art. 37,
> §1º. É a leitura que sustenta a regra — não um dispositivo que a nomeie assim. Vale confirmação do
> consultor antes de virar critério automático de julgamento.

**Regra 2.2.** Adimplência é condição para concorrer à contemplação. Fonte: **art. 11, §1º**, Res.
BCB 285/2023 ("Só concorre o consorciado adimplente") + **art. 22, §2º** da Lei (só concorre o
consorciado ativo).

**Regra 2.3.** O lance só pode ocorrer **depois** das contemplações por sorteio da assembleia (ou na
ausência delas, por falta de recursos), e só é considerado vencedor **depois que a administradora
efetivamente recebe** o valor ofertado. Fonte: **art. 12, I e II**, Res. BCB 285/2023.

**Regra 2.4.** O lance embutido é **deduzido do próprio crédito** do consorciado — não é dinheiro
adicional que sai do bolso dele. Fonte: **art. 13, parágrafo único, I**, Res. BCB 285/2023 (o lance
vencedor é "integralmente deduzido do crédito previsto para distribuição, sendo disponibilizada ao
contemplado a diferença").

**Regra 2.5.** O lance **reduz a parcela**, nunca encurta o prazo do plano. Fonte: **art. 12,
parágrafo único** (redação Res. BCB 362/2023): o lance vencedor é destinado à "quitação ou à
amortização parcial de prestações vincendas" — abate parcela futura, não devolve tempo.

**Regra 2.6.** Contemplação **não é** crédito liberado. O crédito só é colocado à disposição do
contemplado até o **3º dia útil** após a homologação (que pressupõe, no caso de lance, o
recebimento do valor — Regra 2.3) — e mesmo essa liberação ainda depende de análise de crédito e
garantias do grupo. Fonte: **art. 16**, Res. BCB 285/2023.

> ⚠️ **Critério de análise de crédito e garantias exigidas na contemplação — sem fonte normativa
> nesta pesquisa.** É devida diligência de operação (itens D-1 e D-2 de `04-checklist-de-bolso.md`),
> não normativo do BCB. Enquanto não respondido, nenhuma peça pode dizer "contemplado = carta na
> mão" sem essa ressalva.

---

## 3. O que precisa estar aberto numa simulação ou peça com número

**Fonte:** `07-normativo-bcb-consorcio-resolucao-155-2021.md` §3 (art. 5º); `03-normativos-bcb-
consorcio-resolucao-285-2023.md` §3–4 (arts. 2º e 49).

**Regra 3.1.** Toda peça ou simulação que traz um número precisa discriminar, no mínimo:

- **valor do crédito/carta** simulado;
- **taxa de administração**, inclusive se cobrada de forma antecipada;
- **fundo de reserva**, se houver;
- **seguro**, se houver, e a forma de cobrança (desde a adesão ou só após a contemplação — Regra
  3.2);
- o **custo expresso como percentual sobre o valor do crédito**, considerando o **total dos
  pagamentos previstos** ao longo do plano — não só a parcela mensal isolada;
- a **existência e periodicidade do reajuste** do valor do crédito/bem (sem citar índice nem
  percentual aqui — zona do `calculista`);
- o **prazo do plano**.

Fonte: **art. 5º, caput, incisos I–III e §1º**, Res. BCB 155/2021 (custos "expressos sob a forma de
percentual sobre o valor do crédito, considerando o total dos pagamentos previstos") + **art. 2º,
VIII e IX** e **art. 49**, Res. BCB 285/2023 (discriminação obrigatória no contrato e no
Demonstrativo Individual do Consorciado) + **art. 2º, IV**, Res. BCB 285/2023 (critérios de
atualização do valor do bem/crédito como cláusula contratual obrigatória — base para exigir que a
peça mencione que existe reajuste, mesmo sem citar o índice).

**Regra 3.2.** Quando o seguro só é cobrado **após** a contemplação, a peça só precisa informar a
**existência** e a **forma** de cobrança — não é obrigatório expressar o percentual desde a
simulação inicial. Fonte: **art. 5º, §2º**, Res. BCB 155/2021.

**Regra 3.3.** A discriminação de custos deve vir **em forma de tabela**, não diluída em texto
corrido. Fonte: **art. 2º, IX**, Res. BCB 285/2023 ("discriminando-se, sob a forma de tabela...").

---

## 4. Comparar com financiamento

**Fonte:** `07-normativo-bcb-consorcio-resolucao-155-2021.md` §5 (achado 2); `05-cdc-publicidade-e-
oferta-consorcio.md` §1 (art. 37).

**A norma permite comparar** — não veda — mas regula a forma. **Art. 5º, §3º**, Res. BCB 155/2021
(literal): "No caso de eventual comparação das taxas e dos valores cobrados nas operações de
consórcio com os cobrados nas operações de crédito ou de arrendamento mercantil financeiro, as
administradoras devem prestar as informações necessárias acerca das **diferenças entre as
operações** e os **efeitos financeiros decorrentes de cada forma de cobrança**."

**Regra 4.1.** Toda peça que compara consórcio com financiamento (ou leasing) precisa, além do
número final, declarar a **diferença estrutural** entre as operações: o consórcio é rateio de custo
administrativo sobre um crédito que só se recebe **após contemplação** (sorteio ou lance); o
financiamento é amortização mais juros sobre um crédito recebido **de imediato**. Não basta mostrar
"consórcio custa X%, financiamento custa Y%" isolado. Fonte: art. 5º, §3º, Res. BCB 155/2021.

**Regra 4.2.** A peça precisa declarar também o **efeito financeiro** de cada forma de cobrança —
inclusive que o crédito do consórcio depende de contemplação (variável de tempo incerta) e que o
valor do consorciado não fica disponível a ele enquanto aguarda. Omitir esse efeito, numa peça que
já decidiu comparar, soma-se ao risco de enganosidade por omissão de dado essencial (CDC art. 37,
§1º/§3º) — os dois dispositivos (BCB e CDC) convergem para a mesma exigência prática.

---

## 5. Uso do crédito e limites

**Fonte:** `03-normativos-bcb-consorcio-resolucao-285-2023.md` §5 (art. 15).

**Regra 5.1.** O crédito pode ser usado para (I) aquisição do bem/serviço da linha contratada, **ou**
(II) quitação **total** de financiamento de titularidade do consorciado, desde que da **mesma
categoria** do bem/serviço do contrato de consórcio. Nunca quitação **parcial**, nunca de categoria
**diferente**. Fonte: **art. 15, caput, incisos I e II, e §1º**, Res. BCB 285/2023.

**Regra 5.2.** Se o crédito não for usado em **180 dias** da contemplação, o consorciado pode pedir
o valor em espécie, mediante quitação de suas obrigações com o grupo e a administradora. Fonte:
**art. 15, §2º**, Res. BCB 285/2023.

> ⚠️ **Sem fonte normativa nesta pesquisa — devida diligência pendente.** O art. 15, II fecha com "na
> forma prevista contratualmente": o **regulamento do grupo específico** pode impor condição
> adicional sobre a forma de quitação, não capturada aqui (blocos B/C/D de
> `04-checklist-de-bolso.md`). Nenhuma peça deve afirmar condição de uso além das duas do art. 15
> sem confirmar o regulamento do grupo específico.

---

## 6. Saída, desistência e devolução

**Fonte:** `02-lei-11795-2008-sistema-de-consorcio.md` §4.

**Regra 6.1.** **Nunca afirmar "se desistir, recebe tudo de volta"** (nem "todo o valor pago", nem
qualquer formulação de devolução integral e imediata). O consorciado excluído tem direito à
restituição **calculada com base no percentual amortizado** do valor do bem/serviço vigente na data
da assembleia de contemplação, acrescida de rendimentos da aplicação financeira do fundo — não é
devolução automática do total pago. Fonte: **art. 30, caput**, Lei 11.795/2008.

**Regra 6.2.** A pretensão do consorciado (ou excluído) contra o grupo ou a administradora — e
vice-versa — prescreve em **5 anos**. Fonte: **art. 32, §2º**, Lei 11.795/2008.

**Regra 6.3.** Recursos não reclamados entram no regime de "recursos não procurados": taxa de
permanência facultada (percentual não citado aqui — vem do contrato da administradora) e pagamento
obrigatório em até **30 dias corridos** da procura do consorciado. Fonte: **arts. 33 a 38**, Lei
11.795/2008.

> ⚠️ **Sem fonte confirmada — prazo e forma exatos de devolução ao excluído.** Os §§1º a 3º do art.
> 30 (que detalhariam prazo/forma) foram **vetados**. A lei sinaliza que a regulamentação está nos
> **arts. 32–33 da Res. BCB 285/2023**, mas o texto literal desses dois artigos **não foi congelado**
> nesta pesquisa (só a referência de que existem). **Nenhuma peça deve citar prazo específico de
> devolução ao excluído** até essa confirmação. Fica como pendência de pesquisa (ver fechamento).

---

## 7. Oferta e publicidade

**Fonte:** `05-cdc-publicidade-e-oferta-consorcio.md` §1 (Lei 8.078/1990, arts. 30–38).

**Regra 7.1 — vinculação da oferta.** Qualquer número, prazo, condição de contemplação ou vantagem
citada em anúncio, roteiro, post ou material impresso **passa a integrar o contrato**, mesmo que a
proposta formal diga outra coisa. Toda projeção ou estimativa precisa estar **claramente marcada**
como tal. Fonte: **art. 30**, CDC.

**Regra 7.2 — clareza e nomeação correta.** Informação correta, clara, precisa, ostensiva, em
português — e o produto nomeado pelo que é (Regra 1.1). Fonte: **art. 31**, CDC.

**Regra 7.3 — as três saídas são do cliente.** Se a peça prometeu algo que o contrato não cumpre, o
consumidor escolhe entre cumprimento forçado, produto equivalente ou rescisão com devolução
monetariamente atualizada e perdas e danos — **nunca a administradora/representante que escolhe por
ele**. Fonte: **art. 35, incisos I–III**, CDC.

**Regra 7.4 — identificabilidade e lastro documental.** Conteúdo de venda não pode se disfarçar de
conteúdo educativo neutro. Todo número usado numa peça — "R$ X de crédito por Y de parcela", "grupo
com Z% de contemplados" — precisa ter **lastro documental guardado antes de publicar**, pronto para
ser mostrado se cobrado. Fonte: **art. 36 e parágrafo único**, CDC.

**Regra 7.5 — proibição de publicidade enganosa, inclusive por omissão.** É proibida publicidade
enganosa ou abusiva, inclusive quando **omite** dado essencial capaz de induzir o consumidor em
erro. Fonte: **art. 37, caput, §1º e §3º**, CDC.

> **Lista proposta do que é "dado essencial" numa peça de consórcio** — proposta, depende de aval
> do consultor; o CDC não lista, o teste é caso a caso:
> - existência de taxa de administração (e se cobrada de forma antecipada);
> - mecanismo de contemplação: sorteio ou lance, condicionado à existência de recursos no grupo —
>   não automático, não garantido;
> - inexistência de juros no sentido de financiamento bancário, mas existência de correção do
>   saldo/crédito por índice contratual;
> - necessidade de análise de crédito e garantias para liberar a carta após a contemplação (Regra
>   2.6);
> - prazo de duração do plano;
> - condições de uso do crédito — categoria do bem, quitação total (não parcial) (Regra 5.1);
> - regime de saída/desistência — a restituição não é integral nem imediata (Regra 6.1).
>
> Esta lista **não está fechada nem aprovada** — é o candidato natural para virar o núcleo do
> checklist da §10, mas quem decide o corte final é o consultor.

**Regra 7.6 — ônus da prova.** Se um cliente ou o Procon questionar uma alegação da peça, é quem a
divulgou que tem de provar que era verdadeira — não o cliente que tem de provar que era falsa.
Fonte: **art. 38**, CDC.

> ⚠️ **Sem decisão do repo — vedar comparação agressiva com concorrente.** O Código de Conduta da
> ABAC (fonte **secundária**, autorregulação setorial, sem força de lei — `05-cdc...md` §3) tem um
> inciso sobre "lealdade e respeito" aos concorrentes que o CDC arts. 30–38 não cobre. Registro como
> candidato a regra adicional, não como regra vigente — decisão do consultor.

---

## 8. Quem fala e em nome de quem

**O que se sabe:** o vendedor de consórcio costuma atuar como **representante comercial autônomo,
vínculo PJ** — não funcionário da administradora. ⚠️ Isso **não é fonte normativa externa**: o
vínculo real de cada consultor está no contrato de representação dele, e é lá que se confirma.
Base de transparência sobre quem trata o dado: **art. 6º, VI**, LGPD (garantia de informações
claras sobre os agentes de tratamento) — `06-lgpd-dado-publico-e-abordagem-como-fornecedor.md` §4.

**Regra 8.1.** Identificar-se sempre pelo vínculo real — no caso comum, representante comercial
autônomo (PJ) —, nunca como "funcionário", "consultor da [administradora]" ou formulação que sugira
vínculo empregatício ou institucional direto.

> ⚠️ **Sem fonte — depende do contrato de representação.** Uso da marca da administradora, logotipo,
> e quais materiais são "aprovados" para uso em peça (E-5 de `04-checklist-de-bolso.md`) **dependem
> do contrato de cada consultor**. **Enquanto não confirmado: tratar qualquer uso de marca/logo em
> posição institucional (cabeçalho, assinatura, papel timbrado) como vedado por precaução**, e
> qualquer peça autoral (parecer, simulação própria) como análise do consultor, não material oficial
> da administradora. Pergunta que fecha isso: "que materiais e que uso de marca o contrato de
> representação autoriza?" — devida diligência, não pesquisa web.

---

## 9. Dados pessoais

**Este documento não repete o protocolo de dados.** A regra de base está no `AGENTS.md`: dado
nominal de lead ou cliente fica em `dados/`, fora do Git.

**O que as duas rodadas de LGPD trouxeram de novo**, e vale como regra adicional de discurso (não
de fluxo de dados):

**Regra 9.1.** "Abordar como fornecedor, não como cliente" **não é categoria da LGPD** — a lei não
distingue tratamento por papel comercial do titular. O que muda de verdade é que essa finalidade,
**se for real**, fortalece o teste de legítimo interesse (art. 10, I, LGPD — "apoio e promoção de
atividades do controlador"). **Se a finalidade declarada não for a real**, ela fere o princípio da
finalidade (**art. 6º, I**, LGPD) e, se a conversa migrar para oferta de consórcio como consumidor,
soma-se ao risco de enganosidade do CDC (art. 37, §1º). Fonte:
`06-lgpd-dado-publico-e-abordagem-como-fornecedor.md` §0 e §3.

**Regra 9.2.** Dado tornado público **pelo titular** dispensa só o **consentimento** — não dispensa
finalidade, boa-fé, nem o direito de oposição. Dado publicado **pela empresa dele** (site
institucional, cadastro de CNPJ, "fale conosco") tem enquadramento mais frágil nessa dispensa; a
base legal correta nesse caso é o **legítimo interesse** (art. 7º, IX, LGPD), com o teste de
balanceamento documentado — não a dispensa do §4º. Fonte: **art. 7º, §§3º, 4º e 6º**, LGPD —
`06-lgpd-dado-publico-e-abordagem-como-fornecedor.md` §1.

**Regra 9.3.** Prospecção fria (lista montada de dado público — mapa + CNPJ + estimativa, sem
relação prévia) se sustenta por **legítimo interesse** (art. 7º, IX combinado com art. 10, I, LGPD),
mas os dois exemplos oficiais mais próximos no Guia da ANPD **pressupõem relação prévia**, que falta
nesse caso — o que torna o teste de balanceamento mais frágil e pede salvaguarda visível (origem do
contato declarada, opt-out imediato). Fonte: `04-lgpd-legitimo-interesse-prospeccao-b2b.md` §3–4, 6.

> ⚠️ **Ponto a validar pelo consultor** — este documento não decide, só reúne a fonte já congelada
> para quando o consultor validar.

---

## 10. Checklist de peça de venda

Ordem de revisão — cada item aponta a regra que o sustenta:

**A — Nome e natureza do produto**
- [ ] Nomeado como "consórcio" / "cota de consórcio" / "carta de crédito" — nunca "investimento",
  "aplicação", "rendimento garantido" (Regra 1.1)
- [ ] Nenhuma menção a "rendimento" ou "valorização" como benefício ao consorciado (Regra 1.2)

**B — Contemplação**
- [ ] Nenhuma data, prazo ou probabilidade de contemplação — nem por implicatura (Regra 2.1)
- [ ] Se menciona lance: respeita a ordem (sorteio antes) e o recebimento como condição de vitória
  (Regra 2.3)
- [ ] Se menciona lance embutido: descrito como dedução do próprio crédito, não dinheiro extra
  (Regra 2.4)
- [ ] Lance descrito como redutor de parcela, nunca de prazo (Regra 2.5)
- [ ] Contemplação não é apresentada como sinônimo de carta liberada (Regra 2.6)

**C — Números e simulação**
- [ ] Crédito, taxa de administração, fundo de reserva (se houver), seguro (se houver) e forma de
  cobrança, todos discriminados (Regra 3.1)
- [ ] Custo expresso como percentual sobre o crédito, considerando o total dos pagamentos — não só
  a parcela isolada (Regra 3.1)
- [ ] Reajuste mencionado como existente (índice/percentual fica com o `calculista`) (Regra 3.1)
- [ ] Se compara com financiamento/leasing: explica a diferença estrutural e o efeito da espera pela
  contemplação, não só o número final (Regras 4.1, 4.2)

**D — Uso do crédito**
- [ ] Se menciona quitação de financiamento: só quitação total, só mesma categoria do bem/serviço
  (Regra 5.1)

**E — Saída e devolução**
- [ ] Nenhuma afirmação de devolução integral e imediata em caso de desistência (Regra 6.1)
- [ ] Nenhum prazo específico de devolução afirmado sem fonte confirmada (§6, pendência)

**F — Oferta e publicidade**
- [ ] Todo número tem lastro documental guardado antes de publicar (Regra 7.4)
- [ ] Conteúdo de venda identificável como tal, não disfarçado de conteúdo neutro (Regra 7.4)
- [ ] Nenhum dos itens da lista de "dado essencial" (§7) foi omitido (Regra 7.5 — lista sujeita a
  aval)

**G — Identidade de quem fala**
- [ ] Identificação pelo vínculo real (no caso comum, representante autônomo PJ), não funcionário
  (Regra 8.1)
- [ ] Nenhum uso de marca/logo em posição institucional (§8, pendente de contrato)

**H — Dados pessoais**
- [ ] Dado nominal de lead ou cliente fica em `dados/`, fora do Git, sem exceção
- [ ] Se "abordagem como fornecedor": finalidade declarada é a finalidade real (Regra 9.1)

---

## O que esta régua ainda não resolve

| # | O que falta | Onde se fecha |
|---|---|---|
| 1 | Fonte primária com a frase "consórcio não é investimento" (ou equivalente), do BCB ou da CVM | Nova rodada de pesquisa, se o consultor quiser essa frase pronta em vez da inferência do art. 2º |
| 2 | Lista final de "dado essencial" (§7) — hoje é proposta | Decisão do consultor |
| 3 | Texto literal dos arts. 32–33 da Res. BCB 285/2023 (prazo/forma de devolução ao excluído) | Nova rodada de pesquisa normativa |
| 4 | Texto integral da Res. BCB 362/2023 e das alterações posteriores (368/2024, 552/2026) sobre o art. 5º da Res. 155/2021 | Nova rodada de pesquisa normativa |
| 5 | Uso de marca, logotipo e material aprovado (E-5) | Contrato de representação — devida diligência, não pesquisa web |
| 6 | Critérios de análise de crédito e garantias na contemplação (D-1, D-2) | Devida diligência com a área de crédito da administradora |
| 7 | Regulamento do grupo específico sobre forma de quitação de financiamento (art. 15, II) | Devida diligência de grupo (blocos B/C/D) |
| 8 | Comissionamento (tabela oficial, regras de estorno) e histórico de contemplação | Contrato e visita à administradora — não está na web, por design |
| 9 | "Promessa por implicatura" (Regra 2.1) como critério de julgamento automático | Confirmação do consultor antes de aplicar isso mecanicamente |
| 10 | Vigência atual dos normativos citados (checagem pontual antes de qualquer julgamento real) | Checagem de vigência, a cada uso relevante — normativos podem mudar entre 2026 e a data de uso |
| 11 | Vedação de comparação agressiva com concorrente (ABAC, fonte secundária) | Decisão do consultor sobre incluir ou não |
