# -*- coding: utf-8 -*-
"""
Conteúdo semente dos roteiros — sete roteiros, cada um em duas versões (com e sem indicação).

⚠️  Isto é SEMENTE, não fonte da verdade. Depois que a página existe, a verdade é o bloco JSON
    dentro de saida/roteiros.html, que o modo de edição da própria página grava.
    gerar-roteiros.py só usa este arquivo quando a página ainda não tem bloco de dados.

Quem é o consultor sai de config/consultor.json: `dados(cfg)` troca {NOME} por consultor.nome,
{NOME_CURTO} por consultor.nome_curto (ou o nome) e {CRED} pela primeira de
consultor.credenciais. Os números do caso ficam entre colchetes: saem da conta do calculista,
com os parâmetros de produto.linhas.*, nunca daqui.
"""

def p(n, rot, fala=None, porque=None, rams=None, objs=None, skip=False):
    d = {"n": n, "rot": rot}
    if skip: d["skip"] = True
    if fala: d["fala"] = fala
    if porque: d["porque"] = porque
    if rams: d["rams"] = rams
    if objs: d["objs"] = objs
    return d

def ram(t, r, txt): return {"t": t, "r": r, "txt": txt}
def obj(q, a): return {"q": q, "a": a}

# ── falas reaproveitadas entre versões ───────────────────────────────────────
CONTA_VEICULO = (
 "“Vou te dar um caso real. Carro de [R$ valor]: o cara deu [R$ entrada] de entrada e financiou os [R$ saldo] restantes em [n] vezes de [R$ parcela]. Fiz a conta reversa — dá <b>[i]% ao mês, [i anual]% ao ano</b>. Ele vai desembolsar [R$ total] num carro de [R$ valor]: <b>[R$ juros] só de custo de crédito</b>.<br><br>Rodei o mesmo caso no consórcio — a mesma entrada dele entrando na compra, o mesmo crédito de [R$ saldo]. Taxa de administração, fundo de reserva e seguro somam <b>[custo total]% sobre o crédito</b>, e eu abro isso: não existe crédito de graça. Dá <b>[R$ custo no consórcio] contra os [R$ juros] dele — [R$ diferença] de diferença no mesmo carro.</b><br><br>A parcela, <b>nos mesmos [n] meses do banco</b>, sai [R$ parcela no consórcio] contra os [R$ parcela] dele. No prazo cheio do grupo, [R$ parcela no prazo do grupo].<br><br>E a pergunta que todo mundo faz, ‘e se eu não for contemplado’: <b>essa diferença não depende da data da contemplação</b> — é a mesma no mês 3 ou no mês 90. O que a data muda é quando o carro chega, não quanto você paga. Contemplação eu não prometo; ninguém pode.”")
CONTA_PORQUE = (
 "O número que abre é a <b>diferença de custo do crédito</b>, não a parcela: não depende de prazo, de reajuste nem de índice, já traz a taxa aberta dentro dele e o cliente confere na calculadora enquanto você fala. A comparação está no <b>mesmo crédito dos dois lados</b> — o saldo financiado, com a entrada de bolso em ambos —, e é isso que torna a parcela comparável; por isso a parcela no prazo do banco vem antes da parcela no prazo do grupo. ⚠️ Taxa, fundo de reserva, seguro e prazo do grupo vêm de config/consultor.json → produto.linhas.auto, e a conta sai do calculista. Parâmetro ainda não confirmado com a administradora: “com os parâmetros que uso hoje”.")
DESQ = ("“E vou te falar de saída: <b>se a conta disser financiamento, eu digo financiamento.</b> "
  "Já mandei cliente para o banco. Não vivo de vender cota, vivo de acertar a decisão.”")
PEDIDO_15 = ("“Consegue me dar <b>15 minutos</b> para eu te mostrar a planilha? Tenho terça às 16h30 "
  "ou quinta às 10h30. Qual fica melhor?”")
PEDIDO_PORQUE = "Duas opções, nunca três — e nunca “quando fica bom pra você?” antes de oferecer."
OBJ_INTERESSE = obj("“No momento não tenho interesse.”",
  "“Entendo, [Nome]. Só para eu entender e não te incomodar à toa: é questão de <b>tempo</b> ou de "
  "<b>recurso</b> disponível hoje?”")
OBJ_TEMPO = obj("→ Tempo",
  "“Qual momento você acha apropriado para eu te chamar? São 15 minutos, e eu vou com a conta pronta "
  "— você só olha e me diz se faz sentido.”")
OBJ_RECURSO = obj("→ Recurso",
  "“Se o recurso estivesse disponível hoje, você toparia conhecer? <i>[Sim]</i> Então te proponho o "
  "seguinte: conheça o modelo agora, veja como estão fazendo isso sem mexer no capital de giro, e se "
  "fizer sentido você me chama quando o caixa permitir. Me permite 15 minutos?”")
OBJ_RENDE = obj("“Quanto rende? É melhor que investimento X?”",
  "“Não é investimento e eu não vendo como tal — é planejamento de compra, regulado pelo Banco "
  "Central. Quem promete rendimento em consórcio está te vendendo errado. O que eu comparo é "
  "<b>custo de aquisição</b>: quanto você paga a mais para ter o bem hoje, ontem ou daqui a cinco anos.”")
OBJ_WPP = obj("“Me manda por WhatsApp / e-mail.”",
  "“Mando, mas mando <b>depois</b> da conversa e com o seu número dentro. Planilha genérica não serve "
  "para decisão sua — em 15 minutos eu pego seus dados e te devolvo o comparativo dos três caminhos "
  "já preenchido.”")
OBJ_CONTATO = obj("“Como você conseguiu meu contato?”",
  "“Dado público — [Receita Federal / LinkedIn]. <b>Não comprei lista.</b>”")
FECHA_MEU = ("“Fechado. Anotei [dia/hora]. Se acontecer alguma coisa, <b>eu te ligo</b> e a gente "
  "remarca — não te deixo com essa tarefa.”")
FECHA_CURTO = "“Anotei [dia/hora]. Se acontecer alguma coisa, <b>eu te ligo</b>.”"
NOTA_LIGA = {"tipo": "nao", "txt": "Nunca termine com “me liga quando puder”. Quem persegue o próximo contato é você."}
NOTA_INDICADOR = {"tipo": "ok", "txt": "A ligação seguinte é para o <b>indicador</b>: “falei com o [Nome], obrigado.” Indicador que não tem retorno não indica de novo."}

QUALIF_COMPRA = ("“Antes de eu tomar seu tempo: tem alguma <b>compra grande no radar</b> aí nos "
  "próximos 12 meses? Imóvel, veículo, equipamento, frota.”")
RAM_QUALIF = [
  ram("sim", "R: Sim · R: não sei, depende", "Segue para o passo 4. “Depende” é sim."),
  ram("nao", "R: Não", "“Sem problema. Então deixo só uma pergunta plantada: quando aparecer, me chama "
      "<b>antes</b> de assinar qualquer coisa no banco. A conta comparada eu faço em um dia, e é de "
      "graça.” — encerra cordial e registra para retomar em 90 dias."),
]
PONTE_PORQUE = ("Quem prova que você é {CRED} é o passo 4 — o número, a taxa aberta, a conta que "
  "fecha. Credencial recitada na abertura faz o interlocutor classificar você em dois segundos.")

ROTEIROS = []

# ── 01 · INDICAÇÃO ───────────────────────────────────────────────────────────
ROTEIROS.append({
 "id":"indicacao","n":"01","titulo":"Indicação","temp":"q","tags":["confiança emprestada"],
 "oq":"Alguém da rede passou o contato. É o roteiro completo — os outros seis são recortes dele.",
 "padrao":"com",
 "versoes":{
  "com":{
   "rotulo":"com indicação",
   "quem":"Alguém da sua rede passou o contato. Você não é um estranho — é o conhecido de um conhecido, e isso vale os primeiros trinta segundos. Todo o resto você tem que ganhar.",
   "passos":[
    p("1","Abertura · 0–15s",
      fala="“Alô, [Nome], tudo bem? Aqui é {NOME}. Quem me passou o seu contato foi o "
           "<b>[Indicador]</b>, [vínculo: que trabalhou comigo na X / que cuida "
           "da contabilidade da Y].<br><br>Ele te comentou que eu ligaria?”",
      rams=[ram("nao","R: Não","“Tranquilo, pode ter sido a correria.”"),
            ram("sim","R: Sim","“Ótimo, então você já sabe que não é ligação de vendedor. Vou ser rápido.”")]),
    p("2","A ponte · por que ele te indicou",
      fala="“Eu sou {CRED}. Passei a trabalhar com consórcio como instrumento de crédito para PJ e "
           "pessoa física — e o que eu faço <b>não é vender cota</b>. É rodar a comparação antes: "
           "consórcio, financiamento e capital próprio, com o efeito no caixa e no resultado.<br><br>"
           "<i>[se o indicado for contador: “É a conta que o teu cliente te pede e que você não tem "
           "tempo de fazer.”]</i><br><br>O [Indicador] comentou que [gatilho: vocês estão para renovar "
           "frota / você tem uma compra grande no radar / você é quem decide o investimento aí], e foi "
           "por isso que ele me lembrou de você.”",
      porque=PONTE_PORQUE),
    p("3","Qualificação · uma pergunta, não três", fala=QUALIF_COMPRA, rams=RAM_QUALIF),
    p("4","A conta · 30 segundos, número, não teoria", fala=CONTA_VEICULO, porque=CONTA_PORQUE),
    p("5","O desqualificador", fala=DESQ),
    p("6","O pedido", fala=PEDIDO_15, porque=PEDIDO_PORQUE),
    p("7","Objeções", objs=[OBJ_INTERESSE,OBJ_TEMPO,OBJ_RECURSO,OBJ_RENDE,OBJ_WPP]),
    p("8","Fechamento · a responsabilidade é minha", fala=FECHA_MEU),
   ],
   "notas":[NOTA_INDICADOR, NOTA_LIGA],
  },
  "sem":{
   "rotulo":"sem indicação",
   "quem":"O mesmo perfil de interlocutor, só que você chegou nele sozinho — LinkedIn, evento, lista. Não há confiança emprestada: o lugar dela tem que ser ocupado por um motivo concreto, dito nos primeiros trinta segundos.",
   "passos":[
    p("1","Abertura · 0–15s",
      fala="“Alô, [Nome], tudo bem? Aqui é {NOME}, sou {CRED}. A gente não se conhece — "
           "te achei [no LinkedIn / no evento X / pela atividade da empresa]. <b>Me dá trinta segundos "
           "para eu dizer por que liguei</b>, e você decide se vale continuar?”",
      porque="Pedir os trinta segundos é o que substitui a licença que o indicador daria. Sem isso "
             "você está falando com alguém que já decidiu desligar."),
    p("2","A ponte · por que liguei para você",
      fala="“Passei a trabalhar com consórcio como instrumento de crédito para PJ e pessoa física — e "
           "o que eu faço <b>não é vender cota</b>. É rodar a comparação antes: consórcio, "
           "financiamento e capital próprio, com o efeito no caixa e no resultado.<br><br>"
           "Liguei para você porque [motivo concreto: a empresa está no mesmo endereço há [X] anos / "
           "vocês renovam frota / o setor de vocês compra equipamento pesado].”",
      porque="O motivo concreto é o que ocupa o lugar do indicador. “Estou ligando para empresários "
             "da região” não é motivo — é lista, e soa como lista."),
    p("3","Qualificação · uma pergunta, não três", fala=QUALIF_COMPRA, rams=RAM_QUALIF),
    p("4","A conta · 30 segundos, número, não teoria", fala=CONTA_VEICULO, porque=CONTA_PORQUE),
    p("5","O desqualificador", fala=DESQ),
    p("6","O pedido", fala=PEDIDO_15, porque=PEDIDO_PORQUE),
    p("7","Objeções", objs=[OBJ_CONTATO,OBJ_INTERESSE,OBJ_TEMPO,OBJ_RECURSO,OBJ_RENDE,OBJ_WPP]),
    p("8","Fechamento · a responsabilidade é minha", fala=FECHA_MEU),
   ],
   "notas":[{"tipo":"ok","txt":"Sem indicador não há a quem agradecer depois — o retorno vira registro no pipeline, e é você que lembra do próximo toque."},
            NOTA_LIGA],
  },
 }})

# ── 02 · QUENTE ──────────────────────────────────────────────────────────────
OBJ_CONTEMPLADO = obj("“Conheço gente que ficou anos sem ser contemplada.”",
  "“Acontece, e ninguém pode te garantir data — quem garante está mentindo. O que dá para calcular é "
  "o outro lado: <b>quanto tempo a economia de juros paga</b> enquanto você espera. É essa conta que "
  "eu quero te mostrar.”")
OBJ_INVEST = obj("“Isso não é aquele negócio de investimento?”",
  "“Não é — e se alguém te vender assim, corre. É planejamento de compra.”")

CONTA_QUENTE = ("“Fiz as contas dos três caminhos — financiar, juntar e consórcio. Te dou um caso real: carro de [R$ valor], [R$ entrada] de entrada e [n] parcelas de [R$ parcela] sobre os [R$ saldo] restantes. Isso é <b>[R$ juros] de juros</b>. O mesmo crédito no consórcio, com a mesma entrada indo para a compra, custa <b>[R$ custo no consórcio]</b> entre taxa de administração, fundo de reserva e seguro — tudo aberto na planilha. <b>[R$ diferença] de diferença</b>, e a parcela nos mesmos [n] meses cai de [R$ parcela] para [R$ parcela no consórcio].”")

ROTEIROS.append({
 "id":"quente","n":"02","titulo":"Quente","temp":"q","tags":["sem construção"],
 "oq":"Quem já confia. Pula ponte e qualificação: você já sabe o gatilho.",
 "padrao":"sem",
 "versoes":{
  "sem":{
   "rotulo":"sem indicação",
   "quem":"Quem já confia em você. Não precisa provar credibilidade — precisa ser direto e não abusar da confiança.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], você comentou que quer [trocar de carro / sair do aluguel]. Tenho cinco minutos "
           "de conversa útil sobre isso — posso?”"),
    p("2","A ponte — pulado", skip=True,
      porque="Quem já confia não pede explicação de quem você é. Entrar por credencial com um amigo "
             "soa falso e muda o registro da conversa."),
    p("3","Qualificação — pulado", skip=True,
      porque="O gatilho você já sabe — é justamente o que torna este contato quente. Perguntar o que "
             "você já sabe faz a conversa parecer script."),
    p("4","A conta",
      fala=CONTA_QUENTE),
    p("5","O desqualificador", fala="“<b>Se não for o consórcio, eu te falo também.</b>”",
      porque="É a frase que faz o roteiro. O desqualificador na versão pessoal."),
    p("6","O pedido",
      fala="“Te mando a planilha hoje e a gente olha junto — [dia] à noite ou sábado de manhã?”"),
    p("7","Objeções", objs=[OBJ_CONTEMPLADO,OBJ_INVEST]),
    p("8","Fechamento", fala="“Combinado. Te mando hoje e te chamo [dia].”"),
   ],
   "notas":[{"tipo":"nao","txt":"Não empurre por proximidade. Queimar um quente custa mais do que a venda vale."}],
  },
  "com":{
   "rotulo":"com indicação",
   "quem":"Alguém do seu círculo próximo te passou o nome de alguém do círculo dele. A confiança é emprestada de quem indicou — e errar aqui custa dois relacionamentos, não um.",
   "passos":[
    p("1","Abertura",
      fala="“Alô [Nome], tudo bem? Aqui é o {NOME_CURTO}, sou [amigo / primo / cunhado] do <b>[Indicador]</b>. "
           "Ele me falou que você está [querendo trocar de carro / de olho em sair do aluguel] e mandou "
           "eu te procurar.<br><br>Ele te avisou?”",
      rams=[ram("nao","R: Não","“Tranquilo, a gente conversou de passagem — ele deve ter esquecido.”"),
            ram("sim","R: Sim","“Ótimo, então já sabe do que se trata.”")]),
    p("2","A ponte",
      fala="“Eu sou {CRED}. Faço a conta dos três caminhos antes de indicar qualquer coisa — "
           "financiar, juntar ou consórcio.”",
      porque="Uma linha e sai. Com ponte quente, credencial longa parece que você está se vendendo "
             "para quem já foi convencido pelo [Indicador]."),
    p("3","Qualificação",
      fala="“O [Indicador] me falou de [gatilho] — é isso mesmo, ou já mudou?”"),
    p("4","A conta",
      fala=CONTA_QUENTE),
    p("5","O desqualificador", fala="“<b>Se não for o consórcio, eu te falo também.</b>”"),
    p("6","O pedido",
      fala="“Te mando a planilha hoje e a gente olha junto — [dia] à noite ou sábado de manhã?”"),
    p("7","Objeções", objs=[OBJ_CONTEMPLADO,OBJ_INVEST]),
    p("8","Fechamento",
      fala="“Combinado. Te mando hoje e te chamo [dia]. E dou retorno pro [Indicador] também.”"),
   ],
   "notas":[NOTA_INDICADOR,
            {"tipo":"nao","txt":"Não empurre por proximidade — a proximidade aqui nem é sua, é emprestada."}],
  },
 }})

# ── 03 · MORNO COMPRADOR ─────────────────────────────────────────────────────
CONTA_EXEMPLO = ("“Segue o caso que te falei: [o caso da tese que você usa, em cinco linhas], com a taxa "
  "de administração aberta. Se quiser, <b>troco os números pelos seus</b>.”")
DESQ_BANCO = "“Esse mesmo comparativo já mandou cliente meu para o banco. Se for o seu caso, eu digo.”"
PEDIDO_TROCA = ("“Vale 15 minutos para eu trocar os números pelos seus? Terça 16h30 ou quinta 10h30.”")
OBJ_RADAR = obj("“Não tenho nada no radar agora.”",
  "“Perfeito. Te chamo daqui uns três meses só para saber se mudou — e se aparecer antes, me chama "
  "<b>antes</b> de assinar no banco.”")
OBJ_ESCRITO = obj("“Me manda por escrito.”",
  "“Mando — mas o que vale é a planilha com um caso seu dentro. Me dá 15 minutos e ela vai pronta.”")

ROTEIROS.append({
 "id":"morno-comprador","n":"03","titulo":"Morno comprador","temp":"m","tags":[],
 "oq":"A rede profissional fora da contabilidade. Convida para uma análise, não para uma compra.",
 "padrao":"sem",
 "versoes":{
  "sem":{
   "rotulo":"sem indicação",
   "quem":"A rede profissional que não é da contabilidade. Não vender — convidar para uma análise.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], tudo certo? [vínculo: a gente trabalhou junto na X / faz tempo desde a Y].”"),
    p("2","A ponte",
      fala="“Estou estruturando uma operação de crédito planejado para PJ e pessoa física, com foco em "
           "<b>fazer a conta antes de indicar qualquer coisa</b>.”"),
    p("3","Qualificação",
      fala="“Se você ou a empresa tiverem alguma <b>compra grande no radar</b> — imóvel, frota, "
           "equipamento — eu monto o comparativo sem compromisso. Quer que eu mande um exemplo?”",
      porque="“Compra grande” já filtra o ticket que interessa, sem você ter que perguntar quanto a pessoa tem."),
    p("4","A conta · o exemplo enviado", fala=CONTA_EXEMPLO),
    p("5","O desqualificador", fala=DESQ_BANCO),
    p("6","O pedido", fala=PEDIDO_TROCA),
    p("7","Objeções", objs=[OBJ_RADAR,OBJ_ESCRITO]),
    p("8","Fechamento", fala="“Anotei [dia/hora]. Qualquer coisa <b>eu te chamo</b>.”"),
   ],
   "notas":[{"tipo":"ok","txt":"Pede permissão para mostrar trabalho, não para vender."},
            {"tipo":"nao","txt":"Não dispare a lista toda de uma vez. Ondas semanais — lista queimada não se recupera."}],
  },
  "com":{
   "rotulo":"com indicação",
   "quem":"Mesmo perfil, mas alguém da rede fez a ponte. Sai do disparo em onda e vira conversa individual — trate como tal.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], tudo certo? Aqui é {NOME}. Quem me passou o seu contato foi o "
           "<b>[Indicador]</b>, [vínculo].<br><br>Ele te comentou que eu ligaria?”",
      rams=[ram("nao","R: Não","“Tranquilo, pode ter sido a correria.”"),
            ram("sim","R: Sim","“Ótimo, então vou direto ao ponto.”")]),
    p("2","A ponte",
      fala="“Estou estruturando uma operação de crédito planejado para PJ e pessoa física, com foco em "
           "<b>fazer a conta antes de indicar qualquer coisa</b>. O [Indicador] comentou que [gatilho], "
           "e por isso me lembrou de você.”"),
    p("3","Qualificação",
      fala="“É isso mesmo, ou o radar de vocês mudou? Se tiver alguma <b>compra grande</b> à vista — "
           "imóvel, frota, equipamento — eu monto o comparativo sem compromisso.”"),
    p("4","A conta · o exemplo enviado", fala=CONTA_EXEMPLO),
    p("5","O desqualificador", fala=DESQ_BANCO),
    p("6","O pedido", fala=PEDIDO_TROCA),
    p("7","Objeções", objs=[OBJ_RADAR,OBJ_ESCRITO]),
    p("8","Fechamento",
      fala="“Anotei [dia/hora]. Qualquer coisa <b>eu te chamo</b> — e aviso o [Indicador] que a gente falou.”"),
   ],
   "notas":[NOTA_INDICADOR,
            {"tipo":"nao","txt":"Este não entra no disparo em onda. Contato com ponte é individual, ou você queima a ponte junto."}],
  },
 }})

# ── 04 · MORNO PONTE ─────────────────────────────────────────────────────────
PONTE_ANALISE = ("“Estou trabalhando com crédito planejado para PJ e montei uma análise de consórcio "
  "versus financiamento com o corte por regime tributário — que muda bastante no Simples.”")
SKIP_PONTE = ("Este roteiro não vende. Não tem conta, não tem oferta e não tem objeção a virar. Se você "
  "se pegar contornando objeção aqui, está no roteiro errado — a venda é dois passos adiante, com o sócio.")
NOTAS_PONTE = [
  {"tipo":"ok","txt":"Repare no que ele <b>não</b> faz: não pede indicação, não pede lista de cliente, não vende."},
  {"tipo":"ok","txt":"O que devolve: o nome de quem decide. A ligação seguinte deixa de ser fria."},
  {"tipo":"nao","txt":"Não peça “me apresenta pro teu chefe”. Cria obrigação e expõe a pessoa."},
]

ROTEIROS.append({
 "id":"morno-ponte","n":"04","titulo":"Morno ponte","temp":"m","tags":["não é venda"],
 "oq":"Quem trabalha em escritório contábil. O objetivo é um nome, não um negócio.",
 "padrao":"sem",
 "versoes":{
  "sem":{
   "rotulo":"sem indicação",
   "quem":"Quem trabalha em escritório de contabilidade e está na sua rede. O objetivo aqui é <b>um nome</b>, não um negócio.",
   "passos":[
    p("1","Abertura", fala="“[Nome], tudo bem? Faz tempo. Você ainda está na [escritório]?”"),
    p("2","A ponte", fala=PONTE_ANALISE),
    p("3","A pergunta · ocupa o lugar da qualificação",
      fala="“Queria a leitura técnica de vocês. <b>Quem cuida de parceria aí no escritório?</b>”",
      porque="Um assistente responde isso sem se expor — e o sigilo profissional do CFC não é "
             "acionado, porque não se pediu nome de cliente nenhum."),
    p("4–7","Conta, desqualificador, pedido e objeções — pulados", skip=True, porque=SKIP_PONTE),
    p("8","Fechamento",
      fala="“Perfeito, obrigado. Falo com ele — <b>posso dizer que foi você que sugeriu?</b>”",
      porque="Pedir a permissão protege a pessoa e é exatamente o que converte a próxima ligação de fria em morna."),
   ],
   "notas":NOTAS_PONTE,
  },
  "com":{
   "rotulo":"com indicação",
   "quem":"Alguém já te apontou a pessoa certa dentro do escritório. Você não está procurando o nome — está confirmando se é ele mesmo.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], tudo bem? Aqui é {NOME}. Falei com a <b>[Indicador]</b> e ela disse que "
           "você é a pessoa certa pra eu conversar aí no escritório.”",
      porque="O nome da ponte na primeira frase muda o registro: você deixa de ser alguém que ligou "
             "e passa a ser alguém que foi mandado."),
    p("2","A ponte", fala=PONTE_ANALISE),
    p("3","A pergunta · ocupa o lugar da qualificação",
      fala="“Queria a leitura técnica de vocês. <b>É com você mesmo que eu falo, ou seria melhor "
           "com outra pessoa?</b>”"),
    p("4–7","Conta, desqualificador, pedido e objeções — pulados", skip=True, porque=SKIP_PONTE),
    p("8","Fechamento", fala="“Perfeito, obrigado. Digo pra [Indicador] que você me ajudou.”"),
   ],
   "notas":NOTAS_PONTE + [{"tipo":"nao","txt":"Não invente a ponte nem estique o que ela disse. Escritório é lugar pequeno — confere-se em uma sala."}],
  },
 }})

# ── 05 · FRIO RECEPÇÃO ───────────────────────────────────────────────────────
SKIP_RECEP = ("A recepção não decide nada. O único objetivo é chegar no sócio — ou descobrir quando ele "
  "está. Vender aqui só entrega o argumento a quem vai repeti-lo errado.")
NOTAS_RECEP = [
  {"tipo":"ok","txt":"Se ele não estiver: <b>“Qual horário ele costuma estar mais tranquilo? Eu ligo de novo.”</b>"},
  {"tipo":"nao","txt":"Não deixe recado. Recado devolve a decisão para quem ainda não tem motivo para te ligar."},
]

ROTEIROS.append({
 "id":"frio-recepcao","n":"05","titulo":"Frio · recepção","temp":"f","tags":["o primeiro filtro"],
 "oq":"Dois passos e ponto. A recepção não decide nada — só dá ou nega passagem.",
 "padrao":"sem",
 "versoes":{
  "sem":{
   "rotulo":"sem indicação",
   "quem":"Pegue o nome do sócio no QSA antes de ligar. Pedir “o contador” num escritório com três sócios não passa daqui.",
   "passos":[
    p("1","Abertura", fala="“Boa tarde, aqui é {NOME}, sou {CRED}. O <b>[nome do sócio]</b> está?”"),
    p("2","A ponte · só se perguntarem do que se trata",
      fala="“Montei uma análise comparativa de crédito para clientes no Simples e queria a leitura técnica dele.”"),
    p("3–8","Todo o resto — pulado", skip=True, porque=SKIP_RECEP),
   ],
   "notas":NOTAS_RECEP,
  },
  "com":{
   "rotulo":"com indicação",
   "quem":"Você tem o nome de quem mandou. É a diferença entre ser anunciado e ser filtrado.",
   "passos":[
    p("1","Abertura",
      fala="“Boa tarde, aqui é {NOME}, sou {CRED}. Falei com a <b>[ponte]</b> e ela sugeriu que "
           "eu procurasse o <b>[nome do sócio]</b>. Ele está?”",
      porque="O nome da ponte na primeira frase é o que faz a recepção parar de tratar você como fornecedor."),
    p("2","A ponte · só se perguntarem do que se trata",
      fala="“É sobre uma análise comparativa de crédito para clientes no Simples — a [ponte] achou que "
           "valia a leitura técnica dele.”"),
    p("3–8","Todo o resto — pulado", skip=True, porque=SKIP_RECEP),
   ],
   "notas":NOTAS_RECEP + [{"tipo":"nao","txt":"Não invente ponte. A recepção confere — e o custo é o escritório inteiro fechado."}],
  },
 }})

# ── 06 · FRIO SÓCIO ──────────────────────────────────────────────────────────
PONTE_SOCIO = ("“Passei a trabalhar com consórcio como instrumento de crédito para PJ, e o que eu faço "
  "não é vender cota — é <b>rodar a comparação que o cliente pede pra você e você não tem tempo de "
  "fazer</b>: consórcio, financiamento e capital próprio, com efeito no caixa e no resultado.”")
PONTE_SOCIO_PORQUE = ("A oferta é <b>capacidade</b>, não conhecimento. Ele sabe fazer a conta; o que ele "
  "não tem é a hora para fazê-la.")
CONTA_SOCIO = ("“Um exemplo do que sai: cliente que paga [R$ aluguel] de aluguel. A parcela de um consórcio "
  "de [R$ crédito] em [n] meses fica em [R$ parcela] — [comparação com o aluguel]. A pergunta imediata é ‘e se não for "
  "contemplado’ — e é aí que fica interessante: <b>a economia de juros banca [N] meses de aluguel</b>. "
  "Ele pode ser contemplado no mês [M] e ainda sair na frente do financiamento.”")
CONTA_SOCIO_PORQUE = ("Escolha o exemplo pela carteira dele. Escritório com muitas transportadoras: abra pela "
  "conta de frota, não pela de aluguel. Mapeie o perfil de cada escritório antes de ligar.")
PEDIDO_SOCIO = ("“Queria te mostrar a planilha, <b>ouvir onde ela está frágil</b>, e te propor uma coisa: "
  "você me passa um caso, sem me dizer quem é, e eu te devolvo o parecer pronto para você entregar. "
  "Terça 16h30 ou quinta 10h30?”")
PEDIDO_SOCIO_PORQUE = ("Duas opções de horário, e sem “quando fica bom pra você?” antes — abrir e fechar a "
  "mesma pergunta soa inseguro e convida o “me manda um e-mail”.")
OBJS_SOCIO = [
  obj("“Qual é a taxa?” — e vai perguntar.",
      "“Não vou chutar. <b>Anoto, confirmo e te mando por escrito hoje.</b>” — para quem se "
      "apresenta pela conta isso é coerente, e cria um segundo contato legítimo."),
  obj("“Me manda um e-mail.”",
      "“Mando — mas o que vale é a planilha com um caso de vocês dentro. Me dá 15 minutos e ela vai pronta.”"),
  obj("“Já trabalho com uma administradora.”",
      "“Melhor ainda — você já sabe ler o produto. Não vim trocar de cota: vim trazer o comparativo "
      "que a administradora não faz, que é consórcio <b>contra</b> financiamento e <b>contra</b> capital próprio.”"),
  obj("Recusou as duas datas.", "“Me diz um dia da semana mais tranquilo que eu me encaixo.”"),
]
NOTAS_SOCIO = [{"tipo":"nao","txt":"Se marcar, tenha o que mostrar. Se a conta usa premissa ainda não "
  "confirmada — “com as premissas que uso hoje; fecho os números reais essa semana” é melhor que soar "
  "preciso e ser corrigido."}]
QUALIF_SOCIO = p("3","Qualificação", fala="“A carteira de vocês é mais Simples, ou tem bastante Lucro Real?”",
  porque="Uma pergunta que faz duas coisas: escolhe qual exemplo você vai dar no passo 4 e já prepara o "
         "desqualificador do passo 5.")
DESQ_SOCIO = p("5","O desqualificador",
  fala="“E onde eu <b>não</b> recomendo: Lucro Real com lucro alto. Aí o banco ganha — e eu digo isso na "
       "frente do cliente.”",
  porque="É o corte tributário invertido: não como aula, mas como recusa. Mesma tese, função oposta.")

ROTEIROS.append({
 "id":"frio-socio","n":"06","titulo":"Frio · sócio do escritório","temp":"f","tags":[],
 "oq":"A conversa entre pares. Oito passos, e o pedido é um caso para você devolver o parecer.",
 "padrao":"sem",
 "versoes":{
  "sem":{
   "rotulo":"sem indicação",
   "quem":"Não abra pelo corte tributário — para quem faz a apuração todo mês, é o primeiro dia de faculdade. Abra pela conta feita e pelo break-even de tempo.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], boa tarde. {NOME}, sou {CRED}. Vou ser direto — a gente não se conhece, e "
           "eu te dou o motivo da ligação em trinta segundos.”"),
    p("2","A ponte", fala=PONTE_SOCIO, porque=PONTE_SOCIO_PORQUE),
    QUALIF_SOCIO,
    p("4","A conta", fala=CONTA_SOCIO, porque=CONTA_SOCIO_PORQUE),
    DESQ_SOCIO,
    p("6","O pedido", fala=PEDIDO_SOCIO, porque=PEDIDO_SOCIO_PORQUE),
    p("7","Objeções", objs=OBJS_SOCIO),
    p("8","Fechamento", fala=FECHA_CURTO),
   ],
   "notas":NOTAS_SOCIO,
  },
  "com":{
   "rotulo":"com indicação",
   "quem":"Alguém do escritório — a ponte — sugeriu que você procurasse este sócio. A única coisa que muda é a abertura; e é a que decide se ele fica na linha.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], boa tarde. {NOME}, sou {CRED}. <b>Falei com a [ponte] e ela sugeriu te "
           "procurar.</b> Vou ser direto.”",
      porque="A ponte substitui os trinta segundos de licença. Diga o nome dela antes de qualquer "
             "coisa sobre você."),
    p("2","A ponte", fala=PONTE_SOCIO, porque=PONTE_SOCIO_PORQUE),
    QUALIF_SOCIO,
    p("4","A conta", fala=CONTA_SOCIO, porque=CONTA_SOCIO_PORQUE),
    DESQ_SOCIO,
    p("6","O pedido", fala=PEDIDO_SOCIO, porque=PEDIDO_SOCIO_PORQUE),
    p("7","Objeções", objs=OBJS_SOCIO),
    p("8","Fechamento", fala=FECHA_CURTO),
   ],
   "notas":NOTAS_SOCIO + [{"tipo":"ok","txt":"Depois da ligação, retorno para a ponte. Ela se expôs internamente ao te indicar."}],
  },
 }})

# ── 07 · FRIO COMPRADOR FINAL ────────────────────────────────────────────────
PONTE_CF = ("“Fiz uma conta que raramente alguém mostra: <b>quanto o aluguel desses anos teria "
  "construído de patrimônio</b>, e o que muda pelo regime tributário de vocês.”")
CONTA_CF = ("“São dois minutos: [valores do caso]. E a taxa de administração está dentro da conta — "
  "não é comparação maquiada.”")
DESQ_CF = "“<b>Se a conta não fechar para o seu caso, eu digo.</b>”"
PEDIDO_CF = "“Vale 15 minutos com os números de vocês dentro? Terça 16h30 ou quinta 10h30.”"
OBJ_SEM_INT = obj("“Não tenho interesse.”",
  "“Entendo. Só para eu não te incomodar à toa: é questão de <b>tempo</b> ou de <b>recurso</b> hoje?” "
  "— e segue pelos dois braços do roteiro 01.")

ROTEIROS.append({
 "id":"frio-comprador","n":"07","titulo":"Frio · comprador final","temp":"f","tags":[],
 "oq":"Empresas em CNAE de tese. Entra pela conta do endereço, não pelo produto.",
 "padrao":"sem",
 "versoes":{
  "sem":{
   "rotulo":"sem indicação",
   "quem":"Empresas em CNAE de tese. A abordagem é a conta, não o produto.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], boa tarde. {NOME}, sou {CRED}. Vi que a [empresa] opera no mesmo endereço desde [ano].”"),
    p("2","A ponte", fala=PONTE_CF),
    p("3","Qualificação", fala="“O ponto segue alugado até hoje, certo?”"),
    p("4","A conta", fala=CONTA_CF),
    p("5","O desqualificador", fala=DESQ_CF),
    p("6","O pedido", fala=PEDIDO_CF),
    p("7","Objeções", objs=[OBJ_CONTATO,OBJ_SEM_INT]),
    p("8","Fechamento", fala=FECHA_CURTO),
   ],
   "notas":[],
  },
  "com":{
   "rotulo":"com indicação",
   "quem":"Um contador parceiro, um cliente ou alguém da rede apontou esta empresa. O gancho do endereço continua valendo — só deixa de ser a primeira coisa que você diz.",
   "passos":[
    p("1","Abertura",
      fala="“[Nome], boa tarde. {NOME}, sou {CRED}. Quem me falou de vocês foi o "
           "<b>[Indicador]</b>, [vínculo: contador de vocês / cliente meu que trabalha com vocês].<br><br>"
           "Ele te comentou que eu ligaria?”",
      rams=[ram("nao","R: Não","“Tranquilo, pode ter sido a correria.”"),
            ram("sim","R: Sim","“Ótimo, então vou direto ao ponto.”")]),
    p("2","A ponte",
      fala="“Vi que a [empresa] opera no mesmo endereço desde [ano]. " + PONTE_CF.strip("“”") + "”"),
    p("3","Qualificação", fala="“O ponto segue alugado até hoje, certo?”"),
    p("4","A conta", fala=CONTA_CF),
    p("5","O desqualificador", fala=DESQ_CF),
    p("6","O pedido", fala=PEDIDO_CF),
    p("7","Objeções", objs=[OBJ_SEM_INT]),
    p("8","Fechamento", fala=FECHA_CURTO),
   ],
   "notas":[NOTA_INDICADOR],
  },
 }})

DADOS = {"roteiros": ROTEIROS}


def _troca(obj, trocas):
    if isinstance(obj, str):
        for de, para in trocas.items():
            obj = obj.replace(de, para)
        return obj
    if isinstance(obj, list):
        return [_troca(x, trocas) for x in obj]
    if isinstance(obj, dict):
        return {k: _troca(v, trocas) for k, v in obj.items()}
    return obj


def dados(cfg):
    """A semente com o consultor dentro. Nome é obrigatório; sem credencial declarada, o lugar
    dela fica marcado entre colchetes, como os outros campos a preencher."""
    from config import exigir, valor
    nome = exigir(cfg, "consultor.nome")
    creds = valor(cfg, "consultor.credenciais") or []
    return _troca(DADOS, {
        "{NOME_CURTO}": valor(cfg, "consultor.nome_curto") or nome,
        "{NOME}": nome,
        "{CRED}": str(creds[0]) if creds else "[sua credencial]",
    })
