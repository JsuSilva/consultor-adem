# Preset — grupo de consórcio de serviços

Dizeres do card 22, montado a partir do preset de grupo novo.
Molde: `../exemplos/22-card-grupo-servicos.tpl.html` (campanha, 4:5, 1080×1350).

| Bloco | Texto |
| --- | --- |
| Rótulo | CONSÓRCIO DE **SERVIÇOS** |
| Título | GRUPO / `{número do grupo}` |
| Selo | PRIMEIRA ASSEMBLEIA FOI EM / `{MÊS}`! |
| Atributos | os quatro do preset de grupo novo, sem alteração |
| Frase | MAIS QUE UM SERVIÇO, / A REALIZAÇÃO / DE UM SONHO! |
| Etiqueta da linha | CRÉDITO · `{prazo}` MESES |
| Linha de crédito (×3) | R$ `{crédito}` · PARCELA DE R$ `{cheia}` · POR APENAS R$ `{reduzida}` / `{N}` MESES OU ATÉ A CONTEMPLAÇÃO |

**Ícone das linhas:** estrela, não a casa do preset de imóveis.

**O prazo vive na etiqueta.** O molde de grupo não tinha campo de prazo e a Regra 3.1 pede que ele
apareça; por isso "CRÉDITO" virou "CRÉDITO · `{prazo}` MESES".

**Foto:** gerada — avião decolando sobre mar turquesa, sem marca de companhia aérea. Conferir o
enquadramento: no automático (`cover`) o avião pode ficar atrás de "GRUPO"; nesse caso, posição
fixa no `.foto` em vez de `cover`. Uma mancha escura suave (`.veu-frase`) entra atrás da frase,
porque ali o céu é claro e o texto é branco.

**Lastro (Regra 7.4):** número do grupo, prazo, os três trios de crédito, parcela cheia e reduzida, e
por quantos meses a reduzida vale — todos da administradora, com lastro declarado pelo consultor.
