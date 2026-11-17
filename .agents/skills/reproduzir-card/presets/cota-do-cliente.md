# Preset — card da cota do cliente

Peça que acompanha a carta de parabéns: os dados do plano que o cliente acabou de contratar.
Molde: `../exemplos/36-card-cota.tpl.html` (1080×1080, registro escuro, mesmo formato da carta
para os dois irem no mesmo envio).

| Bloco | Conteúdo |
| --- | --- |
| Marca | monograma · nome do consultor · cargo, centralizado |
| Rótulo | CONSÓRCIO DE `[[modalidade, em caixa alta]]` |
| Painel | CRÉDITO CONTRATADO e o valor em degradê do acento |
| Pares | GRUPO `[[grupo]]` · COTA `[[cota]]` |
| Administradora | ADMINISTRADORA / `administradora.nome`, da config |
| Assinatura | nome, cargo e o WhatsApp |
| Foto | casa à noite, bem escurecida ao fundo — do acervo do consultor ou gerada, pela linha "Foto" de `identidade.md` |

**O nome da administradora entra como dado, em texto** — não como logotipo nem assinatura
institucional. É informação do contrato (CDC art. 31), e não uso de marca, que segue vedado por
precaução enquanto o E-5 estiver aberto. Quem assina a peça continua sendo o consultor (Regra 8.1).

**Grupo e cota identificam o contrato de um cliente.** A peça preenchida nunca vai para o Git
(LGPD, `AGENTS.md`): grava em `dados/cota-<grupo>-<cota>.png`. O molde com os campos em branco é a
parte versionável.
