# scripts/

Geradores de peça e utilitários de operação. Todo dado pessoal e todo número da administradora
entram por um lugar só: `config/consultor.json`, lido por `config.py`. Campo vazio faz o script
parar com aviso — nunca vira estimativa.

## Como rodar

Da raiz do repositório, com Python 3 (sem dependência para instalar):

```bash
python3 scripts/<script>.py            # a maioria grava em saida/ (fora do Git)
bash scripts/servir.sh                 # serve a raiz em http://localhost:9797/saida/
```

Sem `config/consultor.json`, os scripts leem o modelo `config/consultor.exemplo.json`, em que
tudo é null, e param com aviso. Quem preenche a config é a skill `configuracao`.

Dado de lead ou cliente fica em `dados/`; peça gerada, em `saida/`. As duas pastas ficam fora do
Git.

## Base

| Script | O que faz | O que lê da config |
|---|---|---|
| `config.py` | Carrega a config: `carregar()`, `valor(cfg, "a.b")`, `exigir(cfg, "a.b")` (para com aviso se vazio). Importado por todos. | o arquivo inteiro |
| `design.py` | Design system: `FONTES`, `TOKENS`, `ESPELHO`, `rgba()`, `TEMA_PADRAO`. Campo vazio cai no padrão neutro. | `identidade_visual.*` |
| `deck_base.py` | Base visual comum dos decks: CSS, ícones, arte de fundo, fotos embutidas de `saida/fotos/`, `brl`/`esc`. | indireto, via `design.py` |
| `controles_deck.py` | Controles padrão de toda apresentação (marca, contador, bolinhas, visão geral, tela cheia, apresentador). `aplicar_marp(html)` ou `css()` + `html()` + `js()`. | `consultor.nome_curto` ou `consultor.nome`, `consultor.site` |
| `telefone.py` | Forma canônica do telefone brasileiro (`canonico`, `suspeito`), regra única do repo. `python3 scripts/telefone.py <número>...` | — |

## Contas

| Script | O que faz | O que lê da config |
|---|---|---|
| `calcular.py` | Motor de break-even de taxa (% a.m. em que o financiamento empata com o consórcio) por linha, em 60/84/120/180/200 meses. Linha sem parâmetro aborta. `--linha auto`, `--print`. Grava `saida/motor-break-even-<linha>.md`. | `produto.linhas.<linha>.taxa_administracao`, `.fundo_reserva` |

## Geradores de peça

| Script | O que faz | O que lê da config |
|---|---|---|
| `gerar-deck-consorcio.py` | Deck "como funciona o consórcio", público geral, só mecanismo: `saida/consorcio-deck.html` (7 slides) e `saida/consorcio-completo-deck.html` (16). | `consultor.nome`, `consultor.vinculo`, `consultor.site`; `produto.linhas.*` (faixa de crédito e índice; rótulos das linhas na divisão da config), `produto._fonte` |
| `gerar-comparativo-construcao.py` | Card consórcio × financiamento Caixa de construção: `saida/comparativo-construcao.html`. Caso no bloco CASO; a curva do financiamento é recalculada com a taxa da config (mostrada em % a.m. e no equivalente composto em % a.a.), e os textos que dependem do resultado são condicionais. | `consultor.nome`, `consultor.assinatura`; `produto.linhas.imovel.taxa_administracao`, `.fundo_reserva`, `.prazo_meses`, `.indice_reajuste`; `mercado.juros_imobiliario_am`, `mercado.incc_12m`, `mercado._fonte` |
| `gerar-comparativo-troca-financiamento.py` | Card "vale trocar o financiamento pelo consórcio?", caso PF de veículo: `saida/comparativo-troca-financiamento.html` (`--png` gera a imagem). Casos nos blocos CASO e CONTA; a sugestão e a leitura do desembolso saem do resultado da conta. | `consultor.nome`, `consultor.assinatura`; `produto.linhas.auto.taxa_administracao`, `.fundo_reserva`, `.prazo_meses`, `.indice_reajuste` |
| `gerar-roteiros.py` (+ `roteiros_seed.py`) | Página dos sete roteiros de abordagem por temperatura, com modo de edição: `saida/roteiros.html`. Rodar de novo preserva o que foi editado na tela; a semente só entra quando a página não existe. Horário do pedido como `[dia] às [hora]`; sem credencial, a frase "sou …" sai da fala. | `consultor.nome`, `consultor.nome_curto`, `consultor.credenciais`, `administradora.nome` |

## Operação

| Script | O que faz | O que lê da config |
|---|---|---|
| `fila-ativacao.py` | Monta a fila de ativação por WhatsApp a partir de uma lista CSV do consultor em `dados/` (colunas no topo do script), já podada: sem telefone, fixo, repetido, já trabalhado (`--pular`), razão social no sócio. Grava `dados/fila-<segmento>-<data>.json`. Só imprime contagens. | — |
| `crm-xlsx.py` | Da fila, monta o XLSX de importação de leads do CRM Apollo (nome, celular, classificação, obs). `--fila`, `--tags`, `--somente-enviados`. Grava em `dados/`. Só imprime contagens. | — |
| `placar-dia.py` | Placar diário do consultor no formato do grupo: contatos do dia (`dados/ativacoes.csv`), reuniões agendadas e realizadas (calendário ICS), conferência contra o print do CRM. Envia por e-mail (Brevo); `--dry-run` só imprime. Segredos no `.env` da raiz. | `consultor.nome`, `administradora.nome`, `operacao.placar.grupo`, `.minimo_contatos`, `.minimo_agendadas`, `.formato` (opcional) |
| `link-rastreio.py` | Código de rastreio por pessoa, derivado do telefone com segredo local (`dados/.link-segredo`); `--cadencia` gera um por lead de `dados/cadencia.csv`, `--codigo` diz de quem é um código. A rota `/l/<código>` fica no site do consultor, fora deste repo. | — |
| `verificar-sites.py` | Verifica quais domínios de uma lista (`dados/dominios.csv`, coluna `dominio`) respondem como site. Cache em `dados/sites-cache.json`. | — |

## Servidor local

| Script | O que faz | O que lê da config |
|---|---|---|
| `servidor.py` | Servidor estático em 127.0.0.1 com UTF-8 e threads. Grava as edições dos roteiros (`POST /api/roteiros` → `saida/roteiros.html`) e da cadência (`POST /api/cadencia` → `dados/cadencia.csv`). `python3 scripts/servidor.py [porta]`. | — |
| `servir.sh` | Confere se a porta está livre e sobe o `servidor.py`. `bash scripts/servir.sh [porta]` (padrão 9797). | — |
