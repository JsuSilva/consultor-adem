---
name: reproduzir-card
description: Reproduz o card de venda de outra marca com a identidade e a identificação do consultor — mesmo layout, textos e números; troca marca, cores, contato e foto, lidos de config/consultor.json. Use quando o consultor mandar a imagem de um card pedindo para reproduzir, ajustar a identidade ou pôr a marca dele.
---

# Skill — `reproduzir-card`

> O padrão de resultado é o card de grupo em andamento: molde em
> `exemplos/01-card-grupo-em-andamento.tpl.html`. A identidade do consultor não mora aqui: vem de
> `config/consultor.json` (`consultor.*`, `identidade_visual.*`), preenchida pela skill
> `configuracao`. Ver `identidade.md`.

## O contrato

O pedido típico: o card exatamente como está, sem a marca original, com a identidade e a
identificação do consultor.

- **Réplica fiel:** layout, ordem dos blocos, todos os textos e todos os números da referência.
- **Troca:** marca, cores, identificação, contato e foto — pela tabela de `identidade.md`.
- **Ajuste de texto** só quando o consultor pedir, um por vez.

## Onde a skill lê e grava

| Onde | O que a skill busca ou grava lá |
| --- | --- |
| `config/consultor.json` | a identidade: nome, cargo, assinatura, telefone, site, cores, fontes, logo |
| `saida/cards/` | destino dos cards (`NN-card-<slug>.png` e `.html`) e das fotos geradas |
| `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md` | régua de compliance |
| `AGENTS.md` | regras de trabalho |

## O que precisa existir na máquina

```bash
ls -d "/Applications/Google Chrome.app" >/dev/null && echo "chrome ok"      # render do PNG
which magick                                                                # recortes da conferência
curl -sI https://fonts.googleapis.com | head -1                             # fontes da config e Dancing Script
```

Sem rede, o Google Fonts não carrega e o card sai na fonte do sistema — outro desenho, mesmo texto.
Sem `magick`, a conferência em recorte não roda.

## Os dois registros

O apelo visual muda com o que a peça vende, e as duas famílias se dividem assim.

| | **Campanha** (consórcio) | **Site** |
| --- | --- | --- |
| Quando | Produto com preço, grupo, prazo — cards 01 a 03 | Post sem oferta — card 08 |
| Título | fonte de título 800, caixa alta | fonte de título 300, caixa baixa, uma palavra em degradê do acento |
| Letra cursiva, itálico pesado, pincel | Sim | Não |
| Faixa e pílula | Inclinadas, com chanfro | Nenhuma: a frase vira uma linha de texto |
| Cantos e riscos diagonais | Sim | Não |
| Divisórias | Barras brancas a 30% | Régua de 1px que nasce e morre transparente |
| Botão | Contorno no acento sobre preto | Sólido no acento, texto preto, canto de 10px |
| Foto | Máscara em diagonal | Véu preto por cima |
| Texto corrido | fonte de título | fonte de texto 300 |

**O que não muda nos dois:** o monograma com as iniciais (ou o logo), a paleta do consultor, a fonte de título nos títulos e o rodapé
com nome e cargo. É o que mantém as duas famílias como a mesma pessoa.

## Presets de grupo

Card de grupo de consórcio de imóveis com o mesmo layout parte do preset, que já traz os dizeres e
o molde — só entram número, selo e créditos:

- `presets/grupo-em-andamento.md` — grupo com assembleias correndo (card 01).
- `presets/grupo-novo.md` — grupo antes da primeira assembleia (card 02).
- `presets/consorcio-imovel-permite.md` — lista de usos do consórcio de imóvel (card 05).
- `presets/consorcio-veiculos-permite.md` — a mesma lista para a linha de veículos (card 17).
- `presets/vencimento-boleto.md` — aviso de vencimento, nas versões imóveis e veículos (cards 06 e 07).
- `presets/frase.md` — post de presença, só uma frase, sem oferta (card 08).

## As marcações do molde

- `{{consultor.*}}` e `{{identidade_visual.*}}` — lidos da config pelo `montar-card.py`.
- `{{card.*}}` e `{{cor.*}}` — derivados da config pelo `montar-card.py` (nome em caixa alta,
  monograma ou logo, cargo, site, tons do acento). Não se editam no molde.
- `[[descrição]]` — valor do card: número do grupo, crédito, parcela, prazo, caminho da foto.
  Preenchido numa cópia do molde; o script **para** se sobrar algum.

## Passos

1. **Inventário da referência.** Listar os blocos na ordem, com posição aproximada em px num quadro
   de 1080 de largura e altura na proporção da imagem. Pronto quando todo texto da imagem está
   transcrito literal, números com centavos inclusive.
2. **Mapa de marca.** Passar cada elemento do inventário pela tabela de `identidade.md`. Pronto
   quando nenhum logo, nome, slogan, cor ou contato da marca original sobra no inventário.
3. **Molde.** Escolher o registro na tabela acima e copiar para `saida/cards/` o exemplo daquela
   família —
   `exemplos/01-card-grupo-em-andamento.tpl.html` (campanha, 4:5, tabela de ofertas),
   `exemplos/03-card-parabens-cliente.tpl.html` (campanha, 9:16, texto e chamada),
   `exemplos/05-card-consorcio-permite.tpl.html` (campanha, fundo claro, lista de itens) ou
   `exemplos/06-card-vencimento-imoveis.tpl.html` (campanha, quadrado, painel claro sobre foto)
   ou `exemplos/08-card-frase.tpl.html` (site, 9:16, frase sem oferta):
   mesmos tokens, gradientes, fontes e posicionamento absoluto; foto como `__FOTO:caminho__`.
   Preencher na cópia cada `[[...]]` com o valor da referência.
4. **Render.**
   ```bash
   python3 skills/reproduzir-card/montar-card.py <molde> saida/cards/NN-card-<slug> [LxA]
   ```
   `NN` é o próximo número livre em `saida/cards/`. Campo de identidade vazio na config para o
   script com aviso — é pergunta ao consultor, não valor a inventar. A exceção são cores e fontes
   de `identidade_visual`: vazias, o card sai no tema neutro de `scripts/design.py` e o script
   avisa — repassar o aviso ao consultor na entrega.
5. **Conferência visual, em loop.** Read no PNG inteiro e depois em recortes de cada faixa densa
   (`sips --cropToHeightWidth`). Passar a lista de armadilhas de `identidade.md`, corrigir no molde,
   renderizar de novo. Pronto quando nenhum recorte mostra texto sobreposto, cortado ou quebrado
   fora do lugar.
6. **Compliance, em card de consórcio.** Passar os textos pela régua
   `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`, checklist da §10.
   Onde a peça bater na régua, **não escrever frase de aviso**: ou a estrutura carrega a informação
   (como "ATÉ A CONTEMPLAÇÃO" dentro do selo do card 05), ou o ponto vai ao bloco de Decisões para o
   consultor resolver. Todo número publicado precisa de lastro declarado por ele (Regra 7.4). Pronto
   quando cada item do checklist foi verificado contra o texto do card.
7. **Entrega.** `SendUserFile` com `display: render`. Resposta em bullets numerados: arquivos, o que
   saiu da marca original, e — no bloco **Decisões** — cada ponto em que a referência não resolveu
   sozinha e houve escolha (a foto sempre entra aqui).
