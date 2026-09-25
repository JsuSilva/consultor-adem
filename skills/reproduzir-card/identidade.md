# Identidade do consultor para cards — de onde cada campo é lido

Referência dos passos 2 e 3 de `SKILL.md`. Nenhum valor mora aqui: todos vêm de
`config/consultor.json`, que a skill `configuracao` preenche. Nos moldes, cada campo aparece como
marcação `{{...}}` e o `montar-card.py` a troca pelo valor da config; campo vazio para o script com
aviso.

## Campos lidos da config

| Campo da config | Marcação no molde | Onde aparece no card |
| --- | --- | --- |
| `consultor.nome` | `{{card.nome_caixa_alta}}` · `{{card.iniciais}}` | nome no bloco de marca e no rodapé; o monograma usa a inicial do primeiro e do último nome |
| `consultor.assinatura` | `{{consultor.assinatura}}` · `{{card.assinatura_caixa_alta}}` | a linha sob o nome ("cargo"), em caixa baixa no bloco de marca e em caixa alta no rodapé |
| `consultor.telefone` | `{{consultor.telefone}}` | contato com o ícone do WhatsApp, no formato em que estiver na config |
| `consultor.site` | `{{consultor.site}}` · `{{card.site_caixa_alta}}` · `{{card.site_nome_caixa_alta}}` + `{{card.site_sufixo}}` | assinatura do rodapé; no card 03, o segundo logo (nome do site em cima, domínio embaixo) |
| `consultor.cidade` | `{{consultor.cidade}}` | rodapé do card 04 |
| `identidade_visual.acento` | `{{cor.acento}}` e os tons escuros derivados | destaque sólido, ícones, faixas, degradês |
| `identidade_visual.acento_brilho` | `{{cor.acento_brilho}}` · `{{cor.acento_claro}}` | ponto de luz dos degradês |
| `identidade_visual.fonte_titulo` | `'{{identidade_visual.fonte_titulo}}'` e o link do Google Fonts | títulos e, nos cards de campanha, o texto todo |
| `identidade_visual.fonte_texto` | `'{{identidade_visual.fonte_texto}}'` e o link do Google Fonts | texto corrido do registro do site (card 04) |
| `identidade_visual.logo` | — | não entra nos moldes; ver a linha "Logo da marca" abaixo |
| `consultor.foto` | — | não entra nos moldes; ver a linha "Foto" abaixo |

## Os tons do acento

As duas cores da config viram a escala inteira dos moldes. Cada tom escuro é o `acento` escurecido
em direção ao preto; o claro é o `acento_brilho` clareado em direção ao branco. As proporções estão
em `ESCALA` e `CLARO` no `montar-card.py`.

| Marcação | Derivação | Uso típico |
| --- | --- | --- |
| `{{cor.acento_claro}}` | `acento_brilho` 41% em direção ao branco | topo do degradê principal |
| `{{cor.acento_medio}}` | `acento` × 0,93 | topo do degradê escuro sobre fundo claro |
| `{{cor.acento_escuro}}` | `acento` × 0,80 | pé do degradê principal, riscos, brilhos |
| `{{cor.acento_profundo}}` | `acento` × 0,62 | pé do degradê escuro sobre fundo claro |
| `{{cor.acento_faixa}}` · `{{cor.acento_sombra}}` · `{{cor.acento_noite}}` · `{{cor.acento_breu}}` | `acento` × 0,47 · 0,33 · 0,19 · 0,12 | faixas e selos escuros na cor da marca |

Cada tom tem também a versão `_rgb` (`{{cor.acento_rgb}}`), para uso em `rgba(...)`.

## Tabela de troca

| Na referência | No card do consultor |
| --- | --- |
| Logo da marca | Bloco de marca: iniciais na fonte de título 900 com gradiente 160deg `acento_brilho → acento → acento_escuro`; abaixo o nome em caixa alta, fonte de título 800, branco; abaixo a assinatura, fonte de título 500 `#E5E7EB`, com espaçamento entre letras calculado para ocupar a mesma largura do nome (script no molde 05). Se o consultor tiver logo próprio em `identidade_visual.logo`, o uso dele no lugar do monograma é pergunta ao consultor |
| Cor principal da marca (o vermelho no card 01) | Acento: gradiente 180deg `acento_claro 0% · acento_brilho 30% · acento 58% · acento_escuro 100%`; destaque sólido `acento` |
| Faixa ou selo escuro na cor da marca | `linear-gradient(90deg, acento_sombra, acento_faixa 55%, acento_noite)` com borda `acento_brilho` a 70% |
| Texto branco sobre a cor principal | Tinta `#0F1419` sobre o acento |
| Texto na cor da marca sobre fundo claro | Degradê escuro 180deg `acento_medio → acento_escuro → acento_profundo`; o tom claro some no branco — card 05 |
| Prata, branco e preto de fundo | Ficam; prata = gradiente 180deg `#FFF · #F3F4F6 40% · #9CA3AF 52% · #E5E7EB 70% · #FFF` |
| Riscos de luz coloridos | Mesmos riscos em `acento` a 75% |
| Nome e cargo do vendedor | `consultor.nome` e `consultor.assinatura`, em caixa alta |
| Telefone | `consultor.telefone` |
| Contato, em todo card | **Obrigatório**: ícone do WhatsApp e o número legíveis na imagem, porque o card circula por print. Entra na linha que o card já tem — dentro da chamada (03), no botão ao lado (04), na assinatura do rodapé (05) ou sob o nome (06, 07) — sem criar bloco novo. O site acompanha quando couber |
| Slogan ou assinatura da marca | nome em caixa alta `|` site em caixa alta, com o site em `acento` |
| Frases genéricas ("Fale com quem entende!", "Seu sonho mais perto") | Ficam; a palavra em destaque vai para `acento` |
| Segundo logo da marca no rodapé, ao lado do nome do vendedor | iniciais + nome do site em fonte de título 800 sobre o domínio em fonte de título 400 — card 03 |
| Ícones | SVG inline, traço `acento` |
| Fontes | `fonte_titulo` em tudo (400–900, itálico 700/800); letra cursiva em Dancing Script 700 |
| Foto | Não sai da referência. Primeiro, uma imagem do acervo do consultor que sirva ao tema (card 01: cidade à noite). Sem uma que sirva, **gerar** uma imagem descrevendo a cena da referência sem copiar a foto, fechando o prompt com `Sem texto, sem logotipo, sem pessoas. Arquitetura genérica, não reproduzir nenhum edifício existente identificável.`; grava em `saida/cards/NN-foto-<slug>.png` (card 03: chaves com chaveiro de casa) |

## Formato

Quadro na proporção da referência, renderizado em 2×. Card 01: 1080×1350 → PNG 2160×2700.

## Armadilhas vistas nos cards 01, 03, 05, 06 e 07

- **Faixa colorida da direita cobrindo a coluna do meio.** Medir as três colunas antes de escrever.
  Card 01: crédito 0–426, divisor em 426, parcela 428–642, faixa de 356 px com chanfro de 32 px.
  Reduzir a fonte do valor antes de encolher a faixa.
- **Rodapé quebrando em várias linhas.** `white-space: nowrap` no contêiner; letter-spacing largo
  consome largura rápido (nome a 21 px com .28em coube). Nome longo na config pede conferência do
  rodapé e do bloco de marca.
- **Texto cursivo inclinado cortado na borda de baixo.** A rotação aumenta a altura ocupada; o bloco
  termina pelo menos 60 px acima da borda.
- **Fonte ausente no PNG.** O `--virtual-time-budget` do `montar-card.py` dá tempo para o Google
  Fonts carregar; se o texto sair em fonte de sistema, a rede falhou — renderizar de novo. Fonte da
  config que não tenha os pesos pedidos no link também sai em fonte de sistema.
- **Acento sumindo sob faixa da mesma cor.** Palavra no acento logo abaixo de faixa no acento perde o
  acento gráfico atrás dela (card 03, "ÚNICA" sob "OPORTUNIDADE"). A palavra desce até o acento
  ficar no preto.
- **Palavras grandes vizinhas se tocando.** Título em itálico pesado ao lado de outra palavra (card 03,
  "ÚNICA" e "HOJE!"): reduzir a fonte da maior até sobrar vão entre as duas.
- **Ícone que lembra outra coisa.** Relógio com três ponteiros vira o logo da Mercedes; relógio leva dois
  ponteiros, 12h e 3h. Capacete de obra desenhado só como domo vira campainha de balcão; leva aba e
  frisos (card 05). Olhar cada ícone perguntando se lembra algum logo ou outro objeto.
- **Borda reta da foto.** Máscara em diagonal deixa o canto de baixo da foto opaco e a borda aparece;
  a máscara de baixo vai em 180deg. Foto gerada costuma trazer faixa preta na base: a máscara termina
  antes dela (card 03: foto a 610px de largura, `-250px` no topo, `#000 60%` → `transparent 73%`).
- **Acento cortado em texto com degradê.** `background-clip: text` só pinta dentro da caixa do
  elemento; com `line-height: 1`, o acento de maiúscula (Ó, Ú) fica acima da caixa e some (card 05,
  "CONSÓRCIO"). Dar `padding-top` de ~30% da fonte e subir o `top` na mesma medida.
- **Título grande encostando no bloco da marca.** Medir onde a palavra mais larga termina contra onde
  a marca começa; reduzir a fonte antes de mover a marca (card 05: 112 → 100px).
- **Faixa invadindo a lista.** Pílula com sombra logo acima de lista de itens encosta no primeiro item;
  a lista desce até sobrar vão (card 05).
- **Objeto da foto atrás da faixa do rodapé.** O foco da foto (as chaves no card 05) precisa terminar
  acima da faixa; posicionar a foto pela altura do foco, não pelo topo da imagem.
- **Degradê cortando a letra embaixo.** O mesmo recorte do acento vale para a cauda de ç, g, j e p:
  em "Atenção" (card 06) a cedilha sumiu. Dar `padding-bottom` além do `padding-top`.
- **Foto gerada com marca reconhecível.** O primeiro carro saiu um BMW, com grade dupla e emblema
  (card 07). Pedir carroceria genérica, de perfil, sem grade frontal, sem emblema e sem placa — e
  conferir a imagem antes de usar.
- **Foto gerada com moldura branca.** O gerador às vezes devolve a cena dentro de uma borda branca;
  conferir as dimensões e cortar com `magick ... -crop LxA+X+Y +repage` antes de embutir.
- **Foto escura demais sob o véu.** Com véu na cor do acento por cima, foto já escura vira borrão sem
  assunto (card 06 com a foto do 03). Escolher ou gerar imagem com massas claras — fachada
  iluminada, céu de fim de tarde — e aliviar o véu até o assunto aparecer.
