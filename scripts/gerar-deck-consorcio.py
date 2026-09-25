#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera as duas versões do deck "como funciona o consórcio", para público geral:

    saida/consorcio-deck.html            7 slides — a que se apresenta
    saida/consorcio-completo-deck.html  16 slides — a de quem pede detalhe

    python3 scripts/gerar-deck-consorcio.py

**Um gerador só**: os dois decks saem do mesmo texto e das mesmas fontes,
então nunca divergem — o que muda é quais slides entram. A padrão corta a mecânica do grupo,
a parcela, o lance em detalhe, o caminho do crédito, os limites, as três perguntas e a saída;
e traz a faixa de crédito dentro do slide de modalidades.

**A padrão é "o" consórcio; a completa é a exceção**, no nome do arquivo também.

Estrutura: público **geral**; **só mecanismo** (nenhum número de custo, nenhuma simulação);
comparação com financiamento **fora** (fica com a skill `/comparativo-credito`).

Regras, as mesmas dos outros geradores:

1. **O design vem do design.py e do deck_base.py** — CSS, ícones e fotos importados de
   scripts/deck_base.py. Controles de scripts/controles_deck.py.
2. **Nenhum número de custo.** Nem taxa de administração, nem fundo de reserva, nem parcela,
   nem custo total. Onde a régua exige número, a peça diz *que* ele tem de estar aberto na
   proposta, em tabela (Regra 3.1/3.3). O número que entra é de outra natureza: a faixa de
   crédito por linha, lida de config/consultor.json (`produto.linhas.*.credito_min/max`, com
   a fonte em `produto._fonte`).
3. **Identidade e produto vêm de config/consultor.json** via scripts/config.py: nome e site do
   consultor (`consultor.*`, com o vínculo em `consultor.vinculo`), faixas e índice de reajuste
   por linha (`produto.linhas.*`, nos rótulos da divisão da config). Campo
   vazio para o script com aviso — nunca vira estimativa.
4. **Compliance** (conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md): sem
   data, prazo ou probabilidade de contemplação, inclusive por implicatura (2.1); lance como
   dedução do próprio crédito (2.4) e redutor de parcela, nunca de prazo (2.5); contemplação
   não é carta liberada (2.6); nunca "recebe tudo de volta" (6.1); sem prazo de devolução ao
   excluído (§6, pendência); identificação do consultor com o vínculo declarado em
   `consultor.vinculo` (8.1) e nenhuma marca em posição institucional (8.2).
5. **O que a peça não afirma, por falta de fonte:** prazo mínimo e máximo por linha, percentual
   máximo de lance embutido e histórico de contemplação (checklist de bolso B-2/B-3, em
   conhecimento/regras-e-compliance/04-checklist-de-bolso.md). Onde o dado falta, o slide manda
   perguntar — não preenche com estimativa.
6. **O título da capa não compara.** "O crédito mais acessível" seria alegação **comparativa**:
   a régua permite comparar, mas exige informar as diferenças entre as modalidades de crédito
   (Res. BCB 155/2021, art. 5º, §3º) e põe o ônus da prova em quem afirma (CDC, art. 38), e
   nenhum slide desta peça sustenta a comparação. "Ferramenta para compra planejada" descreve o
   produto sem comparar — não depende de lastro que a peça não tem.
7. **Fotos** em saida/fotos/ . Foto que falta não para o deck: o
   slide sai sem ela.
"""
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
from config import carregar, exigir, valor

# ─────────────────────────────────────────────────────────────────────────────
# 0. CONFIGURAÇÃO — lida antes de tudo: faltando campo, para aqui com aviso
# ─────────────────────────────────────────────────────────────────────────────
CFG = carregar()
NOME = exigir(CFG, "consultor.nome")
VINCULO = exigir(CFG, "consultor.vinculo")
SITE = valor(CFG, "consultor.site")
# (chave em produto.linhas, rótulo, o que entra) — os rótulos seguem a divisão da config; o que
# cada grupo aceita comprar é do regulamento, por isso o texto de cada linha não detalha o bem.
LINHAS = [
    ("imovel", "Imóveis", "imóvel, nas finalidades que o regulamento do grupo prevê"),
    ("auto", "Automóveis", "veículo leve, nas condições que o regulamento do grupo prevê"),
    ("pesados", "Pesados", "veículo pesado, nas condições que o regulamento do grupo prevê"),
    ("moto", "Motos", "motocicleta, nas condições que o regulamento do grupo prevê"),
    ("servicos", "Serviços", "serviço contratado, nas condições que o regulamento do grupo prevê"),
]
ROTULO = {k: r for k, r, _oq in LINHAS}
FAIXAS = [(rotulo, oq, float(exigir(CFG, f"produto.linhas.{k}.credito_min")),
           float(exigir(CFG, f"produto.linhas.{k}.credito_max"))) for k, rotulo, oq in LINHAS]
FAIXAS_FONTE = exigir(CFG, "produto._fonte")
INDICE = {k: exigir(CFG, f"produto.linhas.{k}.indice_reajuste") for k in ("imovel", "auto", "servicos")}

import design, controles_deck

import deck_base as H
brl, brl2, esc = H.brl, H.brl2, H.esc
anim, cab, datauri, icone = H.anim, H.cab, H.datauri, H.icone

DESTINO = os.path.join(RAIZ, "saida", "consorcio-deck.html")
DESTINO_COMPLETO = os.path.join(RAIZ, "saida", "consorcio-completo-deck.html")


def assinatura():
    """Identificação do consultor, na capa e no fechamento (Regra 8.1)."""
    site = f", {esc(SITE)}" if SITE else ""
    return f"<b>{esc(NOME)}</b> · {esc(VINCULO)}{site}"

# ─────────────────────────────────────────────────────────────────────────────
# 1. MONTAGEM DO SLIDE — foto e painel por nome, não por índice: as duas versões
#    têm ordens diferentes, e índice fixo faria a foto cair no slide errado.
# ─────────────────────────────────────────────────────────────────────────────
def slide(corpo, grad="", capa=False, sky=False, foto=None, painel=None, foco="center"):
    """`veucheio`: o véu base dos decks foi desenhado para texto na esquerda e morre
    antes do terço direito. Aqui o conteúdo ocupa a largura toda — tabela, KPI, duas
    colunas —, então o slide de conteúdo com foto de fundo recebe um véu uniforme, e
    as caixas por cima ficam opacas (CSS_EXTRA). Capa e fechamento mantêm o véu
    original: lá a foto é a cena, e o texto está só à esquerda."""
    uri = datauri(foto) if foto else ""
    camadas = ""
    if uri:
        camadas = (f'<div class="foto" style="background-image:url({uri})"></div>'
                   f'<div class="foto-veu"></div>')
    elif sky:
        camadas = f'<div class="skywrap">{H.skyline()}</div>'
    camadas += '<div class="grade"></div><div class="ruido"></div>'
    lado = datauri(painel) if painel else ""
    if lado:
        corpo = (f'<div class="cols c6"><div>{corpo}</div>'
                 f'<div class="painel-foto" style="background-image:url({lado});'
                 f'background-position:{foco}">'
                 f'<span class="painel-veu"></span></div></div>')
    cls = " ".join(x for x in ("slide", grad, "capa" if capa else "",
                               "veucheio" if uri and not capa and not sky else "") if x)
    return f'<section class="{cls}">{camadas}<div class="inner">{corpo}</div></section>'


# ─────────────────────────────────────────────────────────────────────────────
# 2. FIGURA — o caminho entre a contemplação e o crédito na conta
# ─────────────────────────────────────────────────────────────────────────────
def caminho_do_credito():
    """Seis etapas em fila. Sem eixo de tempo, de propósito: régua com meses viraria
    expectativa de prazo (Regra 2.1). O que a figura mostra é ORDEM, não duração."""
    # Título e descrição são curtos por medida, não por estilo: a caixa tem 150px e a
    # descrição quebra em 17 caracteres. Texto maior vaza para a etapa vizinha.
    etapas = [
        ("Assembleia", "sorteio e, depois dele, o lance"),
        ("Homologação", "a administradora confirma"),
        ("Lance pago", "vence depois de pago"),
        ("Disponibilização", "até o 3º dia útil da homologação"),
        ("Análise", "crédito e garantias da administradora"),
        ("Uso do crédito", "no bem da linha contratada"),
    ]
    larg, cx, gap = 1000, 150, 20
    alt = 124
    # 17 caracteres é o que cabe em 150px com a mono de 11px e o recuo de 12px de cada lado.
    p = []
    for i, (titulo, texto) in enumerate(etapas):
        x = i * (cx + gap)
        if x + cx > larg:
            break
        cor = "var(--accent)" if i in (0, 5) else "rgba(255,255,255,.28)"
        p.append(f'<rect x="{x}" y="30" width="{cx}" height="80" rx="10" fill="rgba(255,255,255,.03)" '
                 f'stroke="{cor}" stroke-width="1"/>')
        p.append(f'<text x="{x + 12}" y="20" class="lb{" on" if i in (0, 5) else ""}">{esc(str(i + 1).zfill(2))}</text>')
        p.append(f'<text x="{x + 12}" y="52" class="et">{esc(titulo)}</text>')
        for j, linha in enumerate(_quebrar(texto, 17)):
            p.append(f'<text x="{x + 12}" y="{68 + j * 12}" class="ax">{esc(linha)}</text>')
        if i < len(etapas) - 1:
            mx = x + cx + gap / 2
            p.append(f'<path d="M{x + cx + 4} 70 L{x + cx + gap - 4} 70" stroke="rgba(255,255,255,.22)" '
                     f'stroke-width="1"/>')
            p.append(f'<path d="M{mx + 2} 66.5 L{mx + 6} 70 L{mx + 2} 73.5" fill="none" '
                     f'stroke="rgba(255,255,255,.4)" stroke-width="1"/>')
    return (f'<svg class="g" viewBox="0 0 {larg} {alt}" role="img" aria-label="Ordem das etapas '
            f'entre a assembleia e o uso do crédito">{"".join(p)}</svg>')


def _quebrar(texto, n):
    linhas, atual = [], ""
    for palavra in texto.split():
        if len(atual) + len(palavra) + 1 > n and atual:
            linhas.append(atual); atual = palavra
        else:
            atual = f"{atual} {palavra}".strip()
    if atual:
        linhas.append(atual)
    return linhas


CSS_EXTRA = """
svg .et{font:600 12px/1 var(--fonte-titulo);fill:#fff}
.faixas td.v{font-variant-numeric:tabular-nums;white-space:nowrap}
.faixas td.o{color:#9CA3AF;font:300 13.5px/1.45 var(--fonte-texto)}

/* Foto em slide de conteúdo: véu uniforme no lugar do véu-de-capa, que só escurece
   a esquerda. Sem isso o número cai sobre a parte clara da foto e some. */
.slide.veucheio>.foto-veu{background:
  linear-gradient(180deg,rgba(0,0,0,.80),rgba(0,0,0,.52) 42%,rgba(0,0,0,.78)),
  radial-gradient(ellipse 120% 95% at 50% 50%,rgba(0,0,0,.18),rgba(0,0,0,.62))}
/* O CSS base já opacifica .par e os itens de lista sobre foto; o que carrega
   número não estava previsto lá porque lá foto e número nunca dividem slide. */
.slide:has(>.foto) .fig,
.slide:has(>.foto) .kpi,
.slide:has(>.foto) pre.eq{background:rgba(10,10,10,.90);
  border-color:rgba(255,255,255,.14);backdrop-filter:blur(3px)}
.slide:has(>.foto) .kpi.on{background:__KPI_ON_BG__;border-color:__KPI_ON_BORDA__}
/* Ao lado do painel de foto sobra ~60% da largura: os quatro KPIs em auto-fit viravam
   três e um, com o rótulo quebrado. Em duas colunas eles ficam iguais. */
.cols.c6 .kpis{grid-template-columns:repeat(2,1fr)}
.cols.c6 .kpi .v{font-size:clamp(1.25rem,2.2vw,1.65rem)}
""".replace("__KPI_ON_BG__", design.rgba(design.ESPELHO["accent-900"], .92)) \
   .replace("__KPI_ON_BORDA__", design.rgba(design.ESPELHO["accent-400"], .34))


# ─────────────────────────────────────────────────────────────────────────────
# 3. OS SLIDES — um por função, para as duas versões escolherem quais entram
# ─────────────────────────────────────────────────────────────────────────────
def s_capa():
    return slide(f"""
<p class="eyebrow"{anim(0)}>Consórcio · como funciona</p>
<h1{anim(1)}>Consórcio — a sua <b class="hi">ferramenta</b> para compra planejada</h1>
<p class="lead"{anim(2)}>Consórcio é sistema de autofinanciamento em grupo para aquisição de bem ou
serviço, regido pela <b>Lei 11.795/2008</b> e supervisionado pelo <b>Banco Central</b>. Nesta
apresentação: como o grupo funciona, como se é contemplado, quais são as modalidades e o que conferir
em qualquer proposta — de qualquer administradora.</p>
<p class="nota"{anim(3)}>{assinatura()}. Não é material oficial da administradora. Nenhum número de custo aqui: custo se
apresenta em tabela, na proposta.</p>""", capa=True, foto="capa.jpg")


def s_produto():
    return slide(f"""
{cab("predio", "O produto", 0)}
<h2{anim(1)}>Consórcio é <b class="hi">compra em grupo</b> — não é empréstimo, não é aplicação</h2>
<pre class="eq"{anim(2)}>Art. 2º, Lei 11.795/2008 — "Consórcio é a reunião de pessoas naturais e
jurídicas em grupo, com prazo de duração e número de cotas previamente determinados,
promovida por administradora de consórcio, com a finalidade de propiciar a seus
integrantes, de forma isonômica, a aquisição de bens ou serviços, por meio de
<b>autofinanciamento</b>."</pre>
<ul class="lista num">
  <li{anim(3)}><div><b>O dinheiro é do grupo</b>não há banco emprestando: a carta de crédito sai do que os
  consorciados pagaram.</div></li>
  <li{anim(4)}><div><b>A finalidade legal é adquirir</b>por isso não existe rendimento prometido, nem
  valorização da cota como benefício.</div></li>
  <li{anim(5)}><div><b>Prazo e número de cotas são determinados antes</b>o grupo tem tamanho e duração
  definidos em contrato, e a administradora administra.</div></li>
</ul>""", grad="g2", foto="produto.jpg")


def s_grupo():
    """A mecânica e a natureza associativa num slide só: as peças do grupo de um lado, o que
    elas cobram do consorciado do outro."""
    return slide(f"""
{cab("camadas", "A mecânica do grupo", 0)}
<h2{anim(1)}>Você entra num <b class="hi">grupo</b>, não contrata um banco</h2>
<div class="cols c2" style="margin-top:26px">
  <div class="par"{anim(2)}><h3>{icone("camadas")} As peças</h3><ul>
    <li><b>Fundo comum</b>o caixa do grupo — é de onde sai a carta de crédito de quem é
    contemplado.</li>
    <li><b>Taxa de administração</b>o que a administradora cobra para administrar o grupo, prevista
    em contrato.</li>
    <li><b>Fundo de reserva e seguro</b>quando existem, com condição e forma de cobrança previstas
    em contrato.</li>
    <li><b>Assembleia</b>a reunião mensal do grupo. É nela que a contemplação acontece.</li>
  </ul></div>
  <div class="par nao"{anim(3)}><h3>{icone("alerta")} O que isso muda para você</h3><ul>
    <li><b>A carta vem do caixa do grupo</b>a contemplação está condicionada à existência de
    recursos suficientes nele.</li>
    <li><b>Estar em dia é condição</b>só concorre à contemplação o consorciado adimplente e com cota
    ativa.</li>
    <li><b>Sair não é resgatar</b>a saída segue o regulamento, com cálculo próprio — nunca é
    devolução automática do total pago.</li>
  </ul></div>
</div>
<p class="nota"{anim(4)}>Lei 11.795/2008, arts. 10, 23 e 30; Res. BCB 285/2023, art. 11, §1º. Quanto
cada peça custa vem na proposta, discriminado em tabela.</p>""",
        painel="mecanica.jpg")


def s_parcela():
    return slide(f"""
{cab("regua", "A parcela", 0)}
<h2{anim(1)}>O que você paga por mês tem <b class="hi">partes com nome</b></h2>
<div class="kpis">
  <div class="kpi on"{anim(2)}><span class="v">Fundo comum</span><span class="r">a sua parte no caixa que
  compra as cartas do grupo</span></div>
  <div class="kpi"{anim(3)}><span class="v">Taxa de adm.</span><span class="r">a remuneração da administradora,
  prevista em contrato</span></div>
  <div class="kpi"{anim(4)}><span class="v">Fundo de reserva</span><span class="r">quando existe, e com
  condição própria de devolução</span></div>
  <div class="kpi"{anim(5)}><span class="v">Seguro</span><span class="r">quando existe, com a forma de cobrança
  declarada</span></div>
</div>
<p class="sub"{anim(6)}>Peça sempre os quatro <b>com percentual</b>, mais o custo total expresso como
percentual sobre o crédito — considerando o total dos pagamentos previstos, não a parcela isolada — o
prazo do plano e a existência do reajuste. É obrigação da administradora apresentar isso em tabela.</p>
<p class="nota"{anim(7)}>Res. BCB 155/2021, art. 5º; Res. BCB 285/2023, arts. 2º e 49. O consórcio é
supervisionado pelo Banco Central (Lei 11.795/2008, art. 6º) — o que não o torna aplicação com
garantia de retorno.</p>""", painel="parcela.jpg")


def s_portas():
    return slide(f"""
{cab("cenarios", "Contemplação", 0)}
<h2{anim(1)}>Existem <b class="hi">duas portas</b>: sorteio e lance</h2>
<div class="cols c2" style="margin-top:26px">
  <div class="par"{anim(2)}><h3>{icone("aval")} Sorteio</h3><ul>
    <li><b>Acontece em toda assembleia</b>e concorrem os consorciados adimplentes e com cota ativa.</li>
    <li><b>Não há nada a fazer além de estar em dia</b>é o mecanismo isonômico do grupo.</li>
    <li><b>Vem antes do lance</b>o lance só ocorre depois das contemplações por sorteio — ou quando
    elas não ocorrem por falta de recursos.</li>
  </ul></div>
  <div class="par"{anim(3)}><h3>{icone("funcao")} Lance</h3><ul>
    <li><b>É uma oferta de antecipação</b>o consorciado oferece valor para amortizar prestações
    futuras.</li>
    <li><b>Vence conforme o regulamento do grupo</b>que define as modalidades e os limites.</li>
    <li><b>Só vence depois de recebido</b>o lance é considerado vencedor quando a administradora
    efetivamente recebe o valor ofertado.</li>
  </ul></div>
</div>
<p class="nota"{anim(4)}>Lei 11.795/2008, art. 22, §1º e §2º; Res. BCB 285/2023, arts. 11 e 12.
<b>Nenhuma data, prazo ou probabilidade de contemplação é afirmada nesta apresentação</b> — a lei não
as garante, e quem as promete está prometendo o que não pode.</p>""", grad="g2",
        foto="portas.jpg")


def s_lance():
    return slide(f"""
{cab("funcao", "Lance", 0)}
<h2{anim(1)}>Formas de dar lance — e uma delas <b class="hi">não sai do bolso</b></h2>
<ul class="lista num">
  <li{anim(2)}><div><b>Lance livre</b>o consorciado escolhe o valor que oferta. Concorre com as demais ofertas
  da assembleia.</div></li>
  <li{anim(3)}><div><b>Lance fixo</b>valor ou percentual definido no regulamento do grupo. Quem oferta o mesmo
  percentual concorre entre si pelo critério do regulamento.</div></li>
  <li{anim(4)}><div><b>Lance embutido</b>é <b>deduzido do próprio crédito</b>: não é dinheiro a mais saindo do
  bolso. O contemplado recebe a diferença entre a carta e o lance.</div></li>
</ul>
<p class="sub"{anim(5)}>As modalidades disponíveis, o limite do embutido e o critério de desempate são
do <b>regulamento do grupo</b> — pergunte por escrito antes de assinar, e peça o histórico de lance
vencedor daquele grupo.</p>
<p class="nota"{anim(6)}>Res. BCB 285/2023, art. 12, I e II, e art. 13, parágrafo único, I.</p>""",
        foto="lance.jpg")


def s_efeito():
    return slide(f"""
{cab("balanca", "O efeito do lance", 0)}
<h2{anim(1)}>O lance <b class="hi">reduz parcela</b>. Ele não devolve tempo</h2>
<div class="cols c2" style="margin-top:26px">
  <div class="par"{anim(2)}><h3>{icone("aval")} O que o lance faz</h3><ul>
    <li><b>Quita ou amortiza prestações vincendas</b>o valor vai contra parcelas futuras.</li>
    <li><b>Antecipa o acesso ao crédito</b>quem vence o lance é contemplado naquela assembleia.</li>
  </ul></div>
  <div class="par nao"{anim(3)}><h3>{icone("alerta")} O que o lance não faz</h3><ul>
    <li><b>Não encurta o prazo do plano</b>o contrato continua com a duração contratada.</li>
    <li><b>Não garante contemplação</b>ofertar lance é concorrer, não comprar posição.</li>
  </ul></div>
</div>
<p class="nota"{anim(4)}>Res. BCB 285/2023, art. 12, parágrafo único, na redação da Res. BCB 362/2023:
o lance vencedor é destinado à quitação ou à amortização parcial de prestações vincendas.</p>""",
        grad="g2", foto="efeito.jpg")


def s_caminho():
    return slide(f"""
{cab("relogio", "Depois da contemplação", 0)}
<h2{anim(1)}>Contemplado <b class="hi">não</b> é crédito liberado</h2>
<div class="fig"{anim(2)}>{caminho_do_credito()}</div>
<p class="sub"{anim(3)}>A figura mostra <b>ordem</b>, não duração. O crédito é colocado à disposição
até o 3º dia útil da homologação — e a liberação ainda depende da análise de crédito e das garantias
exigidas pela administradora.</p>
<p class="nota"{anim(4)}>Res. BCB 285/2023, art. 16. <b>Quais são os critérios de análise e quais
garantias são exigidas é pergunta para antes de assinar</b> — varia por administradora e por linha, e
nenhuma peça de venda pode dizer "contemplado, carta na mão".</p>""", grad="g3",
        foto="caminho.jpg")


def s_limites():
    return slide(f"""
{cab("alerta", "Os limites", 0)}
<h2{anim(1)}>O que <b class="hi">ninguém</b> pode te prometer</h2>
<ul class="lista">
  <li{anim(2)}><div><b>Data, mês ou prazo de contemplação</b>nem como exemplo, nem como "costuma sair por
  volta de". A contemplação é por sorteio ou lance e depende dos recursos do grupo.</div></li>
  <li{anim(3)}><div><b>Probabilidade de contemplação</b>histórico de um grupo é informação útil, e não é
  promessa aplicável ao seu caso.</div></li>
  <li{anim(4)}><div><b>"Se desistir, recebe tudo de volta"</b>a restituição é calculada com base no percentual
  amortizado, pelo regulamento — não é devolução do total pago.</div></li>
  <li{anim(5)}><div><b>Rendimento ou valorização da cota</b>consórcio não é aplicação financeira. A finalidade
  legal é a aquisição do bem.</div></li>
  <li{anim(6)}><div><b>Carta liberada no dia da contemplação</b>há homologação, prazo e análise de crédito
  antes.</div></li>
</ul>
<p class="nota"{anim(7)}>Tudo o que uma peça de venda afirma <b>integra o contrato</b> (CDC, art. 30).
É por isso que esta apresentação não afirma nada disso.</p>""", foto="limites.jpg")


def s_modalidades(com_faixas):
    """Na versão padrão, a faixa de crédito entra aqui e o slide dedicado sai. Na completa,
    este slide descreve as linhas e o seguinte traz a tabela de faixas."""
    if com_faixas:
        linhas = "".join(
            f'<tr><td class="v">{esc(nome)}</td><td class="o">{esc(oq)}</td>'
            f'<td class="v">{esc(brl(mn))}</td><td class="v hi">{esc(brl2(mx))}</td></tr>'
            for nome, oq, mn, mx in FAIXAS)
        return slide(f"""
{cab("camadas", "Modalidades e faixa de crédito", 0)}
<h2{anim(1)}>Cinco linhas, cada uma com <b class="hi">faixa própria</b></h2>
<div class="fig faixas"{anim(2)}><table>
  <thead><tr><th>Linha</th><th>O que entra</th><th>Crédito mínimo</th>
  <th class="hi">Crédito máximo</th></tr></thead>
  <tbody>{linhas}</tbody>
</table></div>
<p class="sub"{anim(3)}>É a faixa <b>dos grupos abertos no dia da consulta</b> — {esc(FAIXAS_FONTE)} — no
simulador oficial da administradora. Ela muda conforme os grupos em formação, e o valor de crédito que
existe para você é o do grupo em que a sua cota entrar.</p>
<p class="nota"{anim(4)}>Prazo do plano, condições do grupo e custos <b>não estão nesta
apresentação</b>: vêm na proposta, com a tabela de custos aberta.</p>""", grad="g3",
        foto="modalidades.jpg")

    itens = "".join(
        f'<li{anim(n + 2)}><div><b>{esc(rotulo)}</b>{esc(oq)}.</div></li>'
        for n, (_k, rotulo, oq) in enumerate(LINHAS))
    fim = len(LINHAS) + 2
    return slide(f"""
{cab("camadas", "Modalidades", 0)}
<h2{anim(1)}>Cinco linhas, cada uma com <b class="hi">regulamento próprio</b></h2>
<ul class="lista">
  {itens}
</ul>
<p class="nota"{anim(fim)}>O que cada grupo aceita comprar — e em que condição — está no
<b>regulamento do grupo</b>: confira o do seu antes de assinar.</p>""", grad="g2", foto="modalidades.jpg")


def s_faixas():
    linhas = "".join(
        f'<tr><td class="k">{esc(nome)}</td><td class="v">{esc(brl(mn))}</td>'
        f'<td class="v hi">{esc(brl2(mx))}</td></tr>'
        for nome, _oq, mn, mx in FAIXAS)
    return slide(f"""
{cab("etiqueta", "Faixa de crédito", 0)}
<h2{anim(1)}>Cada linha tem <b class="hi">faixa própria</b> de crédito</h2>
<div class="fig faixas"{anim(2)}><table>
  <thead><tr><th>Linha</th><th>Crédito mínimo</th><th class="hi">Crédito máximo</th></tr></thead>
  <tbody>{linhas}</tbody>
</table></div>
<p class="sub"{anim(3)}>É a faixa <b>dos grupos abertos no dia da consulta</b> — {esc(FAIXAS_FONTE)} — no
simulador oficial da administradora. Ela muda conforme os grupos em formação, e o valor de crédito que
existe para você é o do grupo em que a sua cota entrar.</p>
<p class="nota"{anim(4)}>Prazo do plano, condições do grupo e custos <b>não estão nesta
apresentação</b>: vêm na proposta, com a tabela de custos aberta.</p>""", grad="g3",
        painel="faixas.jpg")


def s_pagamento():
    return slide(f"""
{cab("regua", "Duas formas de pagar", 0)}
<h2{anim(1)}>Parcela <b class="hi">integral</b> ou <b class="hi">reduzida</b> até a contemplação</h2>
<div class="cols c2" style="margin-top:26px">
  <div class="par"{anim(2)}><h3>{icone("aval")} Integral</h3><ul>
    <li><b>Paga o fundo comum cheio desde o começo</b>a sua parte no caixa do grupo entra inteira em
    cada parcela.</li>
    <li><b>Depois da contemplação, a parcela cai</b>porque o que faltava de fundo comum é menor.</li>
  </ul></div>
  <div class="par"{anim(3)}><h3>{icone("queda")} Reduzida</h3><ul>
    <li><b>Paga parte do fundo comum, e a taxa integral</b>quanto do fundo comum fica para depois
    é do plano — vem na proposta.</li>
    <li><b>Depois da contemplação, a parcela sobe</b>o fundo comum que ficou para depois volta na
    parcela.</li>
  </ul></div>
</div>
<p class="nota"{anim(4)}>A reduzida <b>não é desconto</b>: é fundo comum adiado. Qual das duas serve
depende do seu caixa e do que você espera fazer depois da contemplação — e a comparação entre as duas,
com número, é conversa de proposta.</p>""", grad="g2", foto="pagamento.jpg")


def s_uso():
    return slide(f"""
{cab("aval", "Uso do crédito", 0)}
<h2{anim(1)}>Contemplado, o crédito tem <b class="hi">uso</b> e tem <b class="hi">prazo</b></h2>
<ul class="lista">
  <li{anim(2)}><div><b>Aquisição do bem ou serviço da linha contratada</b>é o uso natural da carta.</div></li>
  <li{anim(3)}><div><b>Ou quitação total de financiamento seu</b>desde que da mesma categoria do bem ou serviço
  do contrato. Nunca quitação parcial, nunca de categoria diferente — e na forma prevista no
  contrato.</div></li>
  <li{anim(4)}><div><b>180 dias</b>não usado o crédito nesse prazo desde a contemplação, o consorciado pode
  pedir o valor em espécie, quitadas as suas obrigações com o grupo e com a administradora.</div></li>
</ul>
<p class="nota"{anim(5)}>Res. BCB 285/2023, art. 15, incisos I e II, §1º e §2º. O regulamento do grupo
pode trazer condição adicional sobre a forma de quitação — confira o do seu grupo.</p>""",
        painel="chaves.jpg", foco="50% 80%")


def indices():
    """Índice de reajuste por linha, da config. Linhas com o mesmo índice saem juntas."""
    grupos = {}
    for k in ("imovel", "auto", "servicos"):
        grupos.setdefault(INDICE[k], []).append(esc(ROTULO[k].lower()))
    return "; ".join(f"{' e '.join(r)} pelo {esc(i)}" for i, r in grupos.items())


def s_perguntas():
    return slide(f"""
{cab("regua", "O que perguntar sempre", 0)}
<h2{anim(1)}>Três perguntas para <b class="hi">qualquer</b> proposta de consórcio</h2>
<ul class="lista num">
  <li{anim(2)}><div><b>Qual é o custo total, em percentual sobre o crédito?</b>considerando o total dos
  pagamentos previstos, não a parcela mensal isolada. Em tabela, com taxa de administração, fundo de
  reserva e seguro discriminados.</div></li>
  <li{anim(3)}><div><b>Qual índice reajusta o crédito, e com que periodicidade?</b>o crédito e a parcela são
  reajustados: {indices()}. Reajuste é correção do valor do bem
  — não é rendimento.</div></li>
  <li{anim(4)}><div><b>O seguro existe? É obrigatório? Desde quando é cobrado?</b>quando só incide após a
  contemplação, a proposta precisa informar a existência e a forma de cobrança.</div></li>
</ul>
<p class="nota"{anim(5)}>Res. BCB 155/2021, art. 5º e §2º; Res. BCB 285/2023, art. 2º. São perguntas
para fazer a <b>qualquer</b> administradora — inclusive à minha.</p>""", grad="g2",
        foto="perguntas.jpg")


def s_saida():
    return slide(f"""
{cab("escudo", "Saída", 0)}
<h2{anim(1)}>Desistir: existe saída, e ela <b class="hi">não é resgate</b></h2>
<ul class="lista">
  <li{anim(2)}><div><b>A restituição é calculada, não devolvida</b>o consorciado excluído tem direito a valor
  apurado com base no <b>percentual amortizado</b> do valor do bem vigente, acrescido dos rendimentos
  da aplicação do fundo — não é o total pago de volta.</div></li>
  <li{anim(3)}><div><b>Prazo e forma estão no regulamento do grupo</b>peça o artigo antes de assinar. Nenhuma
  apresentação — esta inclusive — deve afirmar prazo de devolução.</div></li>
  <li{anim(4)}><div><b>O fundo de reserva tem regra própria</b>pergunte em que condições ele é devolvido.</div></li>
  <li{anim(5)}><div><b>Existe a cessão da cota a terceiro</b>com anuência da administradora, aprovação do
  comprador e efeito tributário sobre eventual ganho.</div></li>
</ul>
<p class="nota"{anim(6)}>Lei 11.795/2008, art. 30. Desistir é a decisão mais cara do consórcio — é por
isso que a parcela precisa caber <b>antes</b> de assinar, e não depois.</p>""",
        foto="saida.jpg")


def s_fechamento():
    return slide(f"""
<p class="eyebrow"{anim(0)}>Próximo passo</p>
<h1{anim(1)}>Onde o consórcio é útil <b class="hi">para você</b>?</h1>
<p class="lead"{anim(2)}>Com o seu objetivo, o seu prazo e o seu caixa, a conversa deixa de ser sobre
o produto e passa a ser sobre a sua compra: qual linha, qual crédito, qual forma de pagar — e uma
proposta com os números discriminados em tabela.</p>
<div class="premissas"{anim(3)}>
  <p>{assinatura()}. Não é material oficial da administradora.</p>
  <p>Consórcio é sistema de autofinanciamento em grupo para aquisição de bem ou serviço, regido pela
  Lei 11.795/2008 e supervisionado pelo Banco Central. Não é aplicação financeira: não há rendimento
  ou valorização prometidos.</p>
  <p>Nenhuma data, prazo ou probabilidade de contemplação é afirmada aqui. Custos, prazo do plano e
  condições do grupo vêm na proposta, discriminados em tabela.</p>
</div>""", sky=True, foto="fechamento.jpg")


# ─────────────────────────────────────────────────────────────────────────────
# 4. AS DUAS VERSÕES
# ─────────────────────────────────────────────────────────────────────────────
def montar(completa):
    S = [s_capa(), s_produto()]
    if completa:
        S += [s_grupo(), s_parcela()]
    S.append(s_portas())
    if completa:
        S += [s_lance(), s_efeito(), s_caminho(), s_limites()]
    S.append(s_modalidades(com_faixas=not completa))
    if completa:
        S.append(s_faixas())
    S += [s_pagamento(), s_uso()]
    if completa:
        S += [s_perguntas(), s_saida()]
    S.append(s_fechamento())
    # `data-s` é o índice real na versão montada — a visão geral e o contador leem daqui.
    return [s.replace('<section class="', f'<section data-s="{i}" class="', 1)
            for i, s in enumerate(S)]


def pagina(S, titulo):
    total = len(S)
    return f"""<!doctype html>
<html lang="pt-BR" data-theme="dark"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titulo)}</title>
{design.FONTES}
<style>{design.TOKENS}{H.CSS}{CSS_EXTRA}</style>{controles_deck.css()}
</head><body>
<div class="deck">
  <div class="trilho" id="t">{"".join(S)}</div>
</div>
{controles_deck.html()}
<script>
(function(){{
  var total={total}, i=0, ouvintes=[],
      t=document.getElementById('t'), slides=[].slice.call(t.children);
  function ir(k){{
    i=Math.max(0,Math.min(total-1,k));
    t.style.transform='translateX(-'+(i*100)+'%)';
    slides.forEach(function(s,j){{ s.classList.toggle('on', j===i); if(j===i) s.scrollTop=0; }});
    ouvintes.forEach(function(f){{ f(); }});
  }}
  addEventListener('keydown',function(e){{
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){{e.preventDefault();ir(i+1)}}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){{e.preventDefault();ir(i-1)}}
    else if(e.key==='Home'){{e.preventDefault();ir(0)}}
    else if(e.key==='End'){{e.preventDefault();ir(total-1)}}
  }});
  var tq=null;
  t.addEventListener('touchstart',function(e){{
    tq={{x:e.touches[0].clientX,y:e.touches[0].clientY,trava:false}};
  }},{{passive:true}});
  t.addEventListener('touchmove',function(e){{
    if(!tq)return; var dx=e.touches[0].clientX-tq.x, dy=e.touches[0].clientY-tq.y;
    if(!tq.trava && Math.abs(dx)>Math.abs(dy)+6) tq.trava=true;
  }},{{passive:true}});
  t.addEventListener('touchend',function(e){{
    if(!tq)return; var dx=e.changedTouches[0].clientX-tq.x;
    if(tq.trava && Math.abs(dx)>48) ir(dx<0?i+1:i-1);
    tq=null;
  }},{{passive:true}});
  ir(0);
  window.deckControles={{total:total, atual:function(){{return i}}, ir:ir,
    ouvir:function(f){{ouvintes.push(f)}}, slides:function(){{return slides}}}};
}})();
</script>
{controles_deck.js()}
</body></html>"""


def main():
    for destino, completa, titulo in (
            (DESTINO, False, "Como funciona o consórcio · deck"),
            (DESTINO_COMPLETO, True, "Como funciona o consórcio · versão completa")):
        S = montar(completa)
        io.open(destino, "w", encoding="utf-8").write(pagina(S, titulo))
        print(f"ok → {os.path.relpath(destino, RAIZ)} · {len(S)} slides")


if __name__ == "__main__":
    main()
