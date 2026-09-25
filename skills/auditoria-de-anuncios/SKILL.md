---
name: auditoria-de-anuncios
description: Audita as contas de anúncio (Meta, Google) com a skill de terceiro claude-ads, só em leitura, e cruza cada achado com a régua de conhecimento/anuncios/regras-de-anuncio-consorcio.md — devolve a lista de propostas ao consultor, sem mudar nada na conta. Invoque com /auditoria-de-anuncios quando o consultor quiser um diagnóstico das campanhas; não dispara sozinha, porque lê a conta de anúncio e a execução de qualquer mudança é das skills anuncios-meta e anuncios-google.
---

# Skill — `auditoria-de-anuncios`

> Diagnóstico das contas de anúncio usando uma skill **de terceiro**, `claude-ads`, e a régua de
> consórcio deste repositório. A auditoria **só lê**. Toda mudança que sair dela vira **proposta ao
> consultor** e, aprovada, é executada pelas skills `anuncios-meta` ou `anuncios-google`, com as
> travas delas.

## A dependência de terceiro

1. **Repositório:** `AgriciDaniel/claude-ads` — https://github.com/AgriciDaniel/claude-ads
2. **O que é:** uma skill (`SKILL.md`) de auditoria de anúncios que cobre 12 plataformas, entre
   elas Google e Meta; só leitura por padrão.
3. **Licença:** MIT. Uso, cópia e modificação livres, **sem garantia nenhuma** do autor.
4. **Aviso de dependência de terceiro:**
   4.1. Não é mantida por este repositório nem pela administradora. Pode mudar, quebrar ou sumir.
   4.2. A `SKILL.md` dela vira **instrução que o agente segue**. Ler a `SKILL.md` inteira antes do
        primeiro uso e antes de cada atualização.
   4.3. Ela **não conhece** a régua de consórcio: pode sugerir texto, promessa ou segmentação que a
        régua proíbe. A régua prevalece, sempre.
   4.4. Fixar uma versão (commit) e só atualizar depois de ler o que mudou.

## Instalação — clonar e ligar, sem executar instalador

O consultor faz os passos; o agente **não executa** instalador, script ou `setup` do repositório de
terceiro.

1. Clonar numa pasta **fora deste repositório** (o código de terceiro não entra no Git do consultor).
   Exemplo de pasta:

   ```bash
   git clone https://github.com/AgriciDaniel/claude-ads.git ~/.local/share/consultor-adem/terceiros/claude-ads
   ```

2. Registrar a versão e conferir a licença:

   ```bash
   git -C ~/.local/share/consultor-adem/terceiros/claude-ads log -1 --format='%H %cd'
   cat ~/.local/share/consultor-adem/terceiros/claude-ads/LICENSE
   ```

3. Achar a `SKILL.md` e ler. ⚠️ A posição dela dentro do repositório (raiz ou subpasta) não foi
   verificada; procurar:

   ```bash
   find ~/.local/share/consultor-adem/terceiros/claude-ads -name SKILL.md
   ```

4. Se o repositório trouxer script de instalação (`install.sh`, `setup`, `npm`, `pip`), **não
   rodar**. Ler e, se ele fizer algo além de copiar a skill, levar ao consultor antes.
5. Ligar no harness (Claude Code) com um atalho para a pasta que contém a `SKILL.md`, entre as
   skills pessoais:

   ```bash
   mkdir -p ~/.claude/skills
   ln -s <pasta-que-contém-a-SKILL.md> ~/.claude/skills/claude-ads
   ```

6. Abrir sessão nova e conferir que a skill aparece na lista de skills.
7. ⚠️ Outros harnesses que leem `AGENTS.md` (Codex, Cursor) têm pasta de skills própria, não
   verificada aqui.

**Atualizar:** `git -C <pasta> fetch` e `git -C <pasta> diff HEAD origin/HEAD` — ler o diff da
`SKILL.md` antes do `pull`. **Remover:** apagar o atalho em `~/.claude/skills/claude-ads`.

## Pré-requisitos

1. Conexões **de leitura** já feitas pelas skills `anuncios-meta` (Ads MCP, CLI ou Pipeboard) e
   `anuncios-google` (MCP oficial de leitura). Esta skill não configura acesso.
2. `config/consultor.json` → `anuncios.*` com os IDs das contas.
3. Régua lida: `conhecimento/anuncios/regras-de-anuncio-consorcio.md`.

## Regras

1. **Só leitura.** Durante a auditoria, nenhuma ferramenta de escrita é chamada. Se a `claude-ads`
   ou a sessão pedir uma, **negar** e registrar no relatório. Na Meta, são de escrita, entre
   outras: `ads_activate_entity`, `ads_update_entity`, `ads_boost_ig_post`, `ads_create_*`,
   `ads_update_custom_audience_users`, `ads_delete_custom_audience`, `ads_pixel_event_*`. No
   Google, o MCP oficial só lê; o script de escrita de `scripts/google-ads/` **não é usado** aqui.
2. **Não dispara sozinha.** Só roda com `/auditoria-de-anuncios` pedido pelo consultor.
3. **Nenhuma mudança na conta.** Achado vira proposta; proposta vai ao consultor; executar é das
   skills `anuncios-meta` / `anuncios-google`, com o "sim" do consultor naquela rodada e as travas
   delas (campanha pausada, teto de `anuncios.teto_diario_brl` confirmado, nada de público com dado
   pessoal sem aval).
4. **Relatório fora do Git.** O relatório bruto e a ficha vão para `saida/` — trazem IDs de conta,
   gasto e nomes de público.
5. **Nada de número inventado.** Benchmark que a `claude-ads` citar sem fonte entra como "citado
   pela ferramenta, sem fonte", não como fato.

## Passos

1. **Escopo com o consultor:** quais contas (Meta, Google), qual período. A skill não escolhe.
2. **Rodar a `claude-ads`** conforme a `SKILL.md` dela, restrita às contas e ao período, em leitura.
3. **Guardar o relatório bruto** em `saida/auditoria-anuncios-<data>.md`.
4. **Cruzar cada achado com a régua** e classificar:
   4.1. **Técnico** (estrutura de campanha, rastreamento de conversão, lances automáticos,
        orçamento, frequência) — vira proposta; mudança de orçamento sempre abaixo do teto e com
        "sim".
   4.2. **Texto ou criativo** — a sugestão passa pelo checklist do §9 da régua. Choque com a régua
        (promessa de prazo, urgência de contemplação, "investimento", "sem juros" sozinho, qualquer
        número em anúncio curto — número só na página de destino, com a tabela completa) →
        **descartada**, com a regra citada.
   4.3. **Segmentação** — idade 18+ e público com dado pessoal conferidos no §5 da régua; público
        com lista exige base legal e aval.
   4.4. **Anúncio já no ar que fere a régua** — sai como **alerta no topo** da ficha, com a regra
        violada. Pausar é proposta ao consultor, executada pela skill da plataforma.
   4.5. **Pendência de plataforma** (verificação de serviços financeiros do Google, política da
        Meta) — remete ao §6–§8 da régua e às perguntas à administradora.
5. **Devolver a ficha** (abaixo) ao consultor e parar.

## Saída — a ficha

Em `saida/auditoria-anuncios-<data>-ficha.md` e resumida na resposta, em bullets numerados:

1. **Alertas de régua** — anúncio no ar que fere a régua: anúncio, trecho, regra, proposta.
2. **Propostas técnicas** — achado, o que a `claude-ads` sugeriu, o que muda, skill que executaria.
3. **Sugestões descartadas** — sugestão e a regra da régua que a barra.
4. **Pendências** — o que depende da administradora ou de política de plataforma.
5. **Decisões** — uma linha por proposta, com as opções, para o consultor aprovar ou recusar.

## Limites

- Não escreve anúncio: texto novo sai pela `roteirista` e passa pelo checklist da régua.
- Não executa nenhuma proposta, nem as "pequenas e óbvias".
- Não configura conexão com Meta ou Google.
- Não julga compliance de peça sozinha como parecer final: aponta o choque com a régua; quem decide
  é o consultor.
