---
name: configuracao
description: Personaliza esta cópia do repositório para o consultor — pergunta dados pessoais, identidade visual, administradora e os números do produto, e grava em config/consultor.json (fora do Git). Invoque com /configuracao no primeiro uso, ou quando um dado mudar (telefone novo, nova tabela da administradora, nova faixa de comissão).
---

# Skill — `configuracao`

> O repositório é universal; a configuração é o que o torna **seu**. Todo script, card, deck e
> agente lê daqui — nome, contato, cores, administradora, taxas, comissão. Nada disso fica em
> arquivo versionado.

## Quando usar

- **Primeiro uso**, logo depois de clonar.
- **Algo mudou:** telefone, identidade visual, unidade, tabela da administradora, comissão.
- Um script parou com `ERRO: ... não preenchido em config/consultor.json` — a mensagem diz o campo.

## Regras

1. **Pergunta, não presume.** Nenhum campo é preenchido por dedução, exemplo ou "valor comum de
   mercado". Não sabe? Fica `null` — o script que precisar dele para com aviso.
2. **Número da administradora exige fonte.** Taxa, fundo de reserva, prazo, faixa de crédito e
   comissão só entram com o documento de origem e a data (tabela, regulamento, contrato, portal).
   A fonte vai em `produto._fonte` e `comissao._fonte`.
3. **Percentual em fração:** 18% vira `0.18`; 0,9% ao mês vira `0.009`. Confirme a conversão com o
   consultor antes de gravar.
4. **Uma seção por vez**, e confirma o bloco antes de gravar. Mostra o JSON da seção, espera o "ok".
5. **Nunca versionar.** `config/consultor.json` está no `.gitignore`. Se `git status` mostrar o
   arquivo, pare e avise.

## Passo a passo

1. **Arquivo.** Se `config/consultor.json` não existe, copie `config/consultor.exemplo.json` para
   ele. Se existe, leia e pergunte **quais seções** o consultor quer atualizar — não refaça tudo.
2. **Você (`consultor`).** Nome completo, nome curto (como assina), cargo (a linha sob o nome nos
   cards), vínculo com a administradora como deve aparecer nas peças (ex.: representante comercial
   autônomo, PJ ou PF — a régua de compliance exige o vínculo real), telefone com DDD, e-mail,
   cidade/UF, site e Instagram (opcionais), credenciais que usa como prova (formação, registros,
   trajetória — o `roteirista` usa isso), a frase de assinatura. Foto: peça o caminho do arquivo e
   copie para `config/foto.<ext>` (também fora do Git).
3. **Administradora (`administradora`).** Nome da administradora e da unidade/escritório. Usa o CRM
   Apollo? Se sim, a URL da unidade (a skill `crm-apollo` só funciona com ela).
4. **Identidade visual (`identidade_visual`).** Cor de acento e uma variação mais clara (hex), fundo
   padrão (escuro ou claro), fonte de título e de texto (Google Fonts), logo (caminho → copie para
   `config/logo.<ext>`). Sem resposta, os geradores usam o tema neutro — diga isso ao consultor.
5. **Produto (`produto`).** Por linha — imóvel, auto, pesados, moto, serviços — só as que o
   consultor vende: taxa de administração total, fundo de reserva (0 quando não houver), prazo em
   meses, índice de reajuste, crédito mínimo e máximo. Depois: seguro, taxa de adesão, modalidades
   de lance que a administradora oferece e o limite do lance embutido. **Fonte e data obrigatórias.**
6. **Comissão (`comissao`).** As faixas (nome, percentual, condição para mudar de faixa) e em
   quantas parcelas é paga. Fonte obrigatória. Se o consultor não quiser registrar, deixe `null` —
   o `calculista` só não fará a conta da carteira.
7. **Mercado (`mercado`).** Juros de referência do concorrente (financiamento imobiliário, CDC de
   veículo, CDC de pesados, Finame), ao mês, e o INCC acumulado em 12 meses (`incc_12m`, em
   fração), com fonte e data da consulta. Opcional — o
   `pesquisador` pode buscar depois, com fonte.
8. **Operação (`operacao`).** Se o consultor usa o `placar-dia.py`: nome do grupo, horário, mínimo
   diário de contatos e de reuniões agendadas, e o formato do texto (opcional — sem ele, sai o padrão).
9. **Anúncios (`anuncios`).** Só se o consultor anuncia. O teto diário de verba em R$ — as skills
   de anúncio recusam qualquer orçamento acima dele e, mesmo abaixo, pedem confirmação a cada
   ativação. Os ids das contas (Meta, Google, WhatsApp oficial) costumam ser preenchidos depois,
   pelas skills `anuncios-meta`, `anuncios-google` e `whatsapp-oficial`. **Credencial nenhuma
   entra aqui** — token, client secret e refresh token ficam em `.env` ou
   `~/.config/consultor-adem/`.
10. **Régua de compliance.** Apresente `conhecimento/regras-e-compliance/02-compliance-e-limites-do-discurso.md`
    em resumo e peça o aval do consultor. Com o aval, registre em `governanca/decisions-log.md` como
    `D-001 — Adota a régua de compliance`, citando a data e a frase do consultor. Sem aval, a régua
    segue como referência de trabalho e a pendência vai para o `governanca/BACKLOG.md`.
11. **Fechamento.** Valide o JSON (`python3 -c "import json;json.load(open('config/consultor.json'))"`),
   rode `git status` para confirmar que o arquivo não aparece e liste, em bullets, os campos que
   ficaram `null` e qual peça cada um trava.

## Primeiro uso — o que vem depois

- Registrar em `governanca/decisions-log.md` as escolhas de posicionamento que o consultor fizer.
- Formular a primeira tese com `conhecimento/teses/README.md`.
- Montar o próprio caminho de prospecção no agente `prospector`.
