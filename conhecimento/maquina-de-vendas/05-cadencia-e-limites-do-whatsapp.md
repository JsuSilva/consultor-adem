# 05 — Cadência de prospecção e os limites do WhatsApp

> **Intervalos e rampa de referência** — o consultor ajusta e aprova os dele antes de usar. Nasceu
> de um pedido concreto: *"preciso de um estudo para que eu possa fazer diariamente novos ativos e
> manter a cadência sem que tenha queda da minha conta do whatsapp pelo volume de iniciativas."*
> Os números de campo citados abaixo são de uma operação real de prospecção fria. Os limites da
> Meta vêm de fontes externas listadas no fim — **a Meta não publica os números**.

## 1. A cadência que está sendo dimensionada

A sequência: **WhatsApp → follow-up → ligação → pega-ratão → novo follow-up → encerramento**. Os
textos estão no repertório da skill `roteirista`.

Para um lead que **nunca responde**, isso são **5 mensagens de WhatsApp** (entrada, follow-up,
pega-ratão, novo follow-up e encerramento) e **1 ligação**, que sai pela linha telefônica e não
consome nada do WhatsApp.

## 2. Três limites diferentes, que não se somam

| Limite | O que dispara | O que se sabe | Fonte |
|---|---|---|---|
| **A · iniciar conversa nova** | muita conversa nova com quem não tem o número salvo, em janela curta | Caso de campo: uma conta ficou 24h sem poder iniciar chat, mantendo resposta e ligação recebida. O limiar não é publicado; relatos de mercado falam em 20 a 30 contatos novos em janela curta | caso de campo; relatos de mercado |
| **B · mensagens sem resposta no mês** | toda mensagem a quem não respondeu conta, **inclusive follow-up** | Teste anunciado em 17/10/2025. Resposta da pessoa tira as mensagens do contador. O número não foi divulgado; o app mostra aviso perto do teto | TechCrunch; Engadget; MacRumors |
| **C · transmissão (lista de divulgação)** | envio para lista de transmissão | Cota mensal de transmissões em teste desde 2025, variando por país | TechCrunch (mar/2025); relatos de mercado |

**O limite B é o que muda o desenho.** Com a taxa de resposta humana que se viu na prospecção fria
(zero em 228 primeiros contatos, no caso de campo), quase toda mensagem da cadência conta.

**O limite C importa no encerramento**, que manda o lead para a lista de divulgação: mesmo que seja
outro número, a lista também tem cota.

## 3. Quanto a cadência pesa por dia e por mês

Com **N contatos novos por dia**, depois de ~14 dias úteis a cadência entra em regime: cada dia tem
N entradas, N follow-ups, N pega-ratões, N novos follow-ups e N encerramentos. Mensagens sem resposta
por mês = 5 × N × 22 dias úteis × (1 − taxa de resposta).

| N novos/dia | Conversas novas/dia (limite A) | WhatsApp/dia em regime | Ligações/dia | Sem resposta/mês, resposta 0% (limite B) | com 10% de resposta |
|---:|---:|---:|---:|---:|---:|
| 5 | 5 | 25 | 5 | 550 | 495 |
| **8** | **8** | **40** | **8** | **880** | **792** |
| 10 | 10 | 50 | 10 | 1.100 | 990 |
| 12 | 12 | 60 | 12 | 1.320 | 1.188 |

**Leitura:** o limite A se controla com N; o limite B cresce 5 vezes mais rápido que N, porque cada
lead calado gera 5 mensagens. É por isso que o teto diário conta **todos** os toques de WhatsApp do
dia, não só os novos.

## 4. Intervalos (de referência — dias úteis depois da etapa anterior)

| Etapa | Canal | Intervalo | Por quê |
|---|---|---:|---|
| WhatsApp | WhatsApp | dia 0 | entrada + abertura |
| Follow-up | WhatsApp | +2 | tempo de ler sem soar cobrança |
| Ligação | telefone | +2 | muda de canal antes de insistir — é o toque que não consome cota |
| Pega-ratão | WhatsApp | +3 | espaça a terceira mensagem sem resposta; só sai com a condição real do dia |
| Novo follow-up | WhatsApp | +2 | pergunta sobre a "última oportunidade" enquanto ela está fresca |
| Encerramento | WhatsApp | +5 | o maior espaço antes do último toque, para reduzir denúncia |

Ciclo completo: **14 dias úteis, cerca de três semanas.** Fim de semana e feriado não contam, e todo
toque respeita a janela de envio (9h–12h e 14h–17h, dia útil).

## 5. Regras que reduzem o risco sem cortar volume

1. **Ligar antes de insistir.** A ligação na etapa 3 é o único toque que não soma nos limites A e B.
2. **Número que nunca entregou não recebe o próximo WhatsApp.** Mensagem parada em um tique só, dias
   depois, indica número sem WhatsApp ou bloqueio: o lead pula para a ligação ou sai da cadência.
3. **Toda mensagem termina numa pergunta de uma palavra.** Resposta tira as mensagens do contador do
   limite B — a entrada ("eu falo com Dr(a). [Nome]?") já faz isso.
4. **Alternar as aberturas.** Texto idêntico em volume é padrão de disparo em massa.
5. **O teto diário é trava, não meta.** Toque que passa do teto é marcado como "passa do teto" e é
   adiado, não disparado.
6. **Aviso de limite próximo no WhatsApp:** parar os follow-ups do dia, manter só respostas, e
   registrar a data — é o único sinal concreto do número que a Meta esconde.
7. **Parada de rodada:** 20 envios sem nenhuma resposta humana param a rodada.

## 6. Rampa (de referência)

- **Fase 1, duas semanas:** N = 8 novos por dia, teto de 40 WhatsApp por dia.
- **Fase 2:** N = 10 e teto de 50, **se** nas duas semanas não houver aviso de limite nem restrição, e
  houver resposta humana.
- **Não passar de 12 novos por dia.**

## 7. O que este estudo não sabe

- **O número do limite B**, e se o teste já chegou ao Brasil e a cada conta.
- **Se ligação feita pelo WhatsApp** conta como iniciativa — por isso a proposta é ligar pela linha.
- **Quanto a lista de divulgação do encerramento aguenta por mês.**

## Fontes

- TechCrunch, 17/10/2025 — [WhatsApp will curb the number of messages people and businesses can send without a response](https://techcrunch.com/2025/10/17/whatsapp-will-curb-the-number-of-messages-people-and-businesses-can-send-without-a-response)
- Engadget — [WhatsApp will test a monthly cap on messages ignored by recipients](https://www.engadget.com/social-media/whatsapp-will-test-a-monthly-cap-on-messages-ignored-by-recipients-164024928.html)
- MacRumors, 17/10/2025 — [WhatsApp Testing Message Limits to Combat Spam](https://www.macrumors.com/2025/10/17/whatsapp-message-limits-spam/)
- Gulf News — [New WhatsApp limits could block messages to people who don't reply](https://gulfnews.com/technology/new-whatsapp-limits-could-block-messages-to-people-who-dont-reply-1.500312721)
- TechCrunch, 18/03/2025 — [WhatsApp will soon limit number of broadcast messages](https://techcrunch.com/2025/03/18/whatsapp-will-soon-limit-number-of-broadcast-messages-users-and-businesses-can-send/)
- Relatos de mercado sobre restrição por volume de contatos novos (sem fonte oficial): [Picky Assist](https://pickyassist.com/blog/whatsapp-restriction-causes-fixes/), [Privyr](https://www.privyr.com/blog/your-account-is-restricted-right-now-whatsapp-notification/)
