#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera saida/roteiros.html — a página dos sete roteiros de abordagem.

    python3 scripts/gerar-roteiros.py

Duas coisas que este script protege, e que já se perderam uma vez:

1. **O design vem do design.py.** Cores, fontes e tokens não são escritos aqui. Mudou lá, roda
   isto e a página acompanha — sem reescrever conteúdo.
2. **O conteúdo vem da página.** A verdade dos roteiros é o bloco JSON dentro do próprio
   roteiros.html, que o modo de edição grava (POST /api/roteiros, ver servidor.py). Este
   script LÊ esse bloco e o devolve intacto. Só cai em roteiros_seed.py quando a página não
   existe ou está sem o bloco — ou seja: rodar isto NÃO apaga o que você editou na tela.

Na semente, nome e credencial do consultor vêm de config/consultor.json (consultor.nome,
consultor.nome_curto, consultor.credenciais) — ver roteiros_seed.dados. A administradora citada
no rodapé é administradora.nome, quando preenchida.
"""
import html, io, json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
import design
from config import carregar, valor

DESTINO = os.path.join(RAIZ, "saida", "roteiros.html")
ABRE = '<script type="application/json" id="dados">'
FECHA = "</script>"

CSS = """
.wrap{max-width:840px;margin:0 auto;padding:52px 24px 100px}
header.top{border-bottom:2px solid var(--ink);padding-bottom:22px;margin-bottom:30px}
.eyebrow{font:600 11px/1 "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);margin:0 0 12px}
h1{font:800 clamp(30px,5.2vw,46px)/1.05 Poppins,system-ui,sans-serif;letter-spacing:-.025em;
  margin:0 0 12px;text-wrap:balance}
.tese{margin:0;max-width:60ch;font-size:17px;color:var(--ink-2)}
.tese b{color:var(--ink);font-weight:600}
table.mapa{width:100%;border-collapse:collapse;margin:30px 0 8px;font-size:14px}
table.mapa th{font:600 10.5px/1 "IBM Plex Mono",monospace;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-3);text-align:left;padding:0 12px 9px 0;border-bottom:1px solid var(--rule)}
table.mapa td{padding:11px 12px 11px 0;border-bottom:1px solid var(--rule-2);vertical-align:top}
table.mapa td.q{font-weight:600;font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
table.mapa tr.sub td{color:var(--ink-3);font-size:13.5px;padding-top:6px;padding-bottom:6px}
table.mapa tr.sub td:first-child{padding-left:16px}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px;vertical-align:1px}
.dot.q{background:var(--quente)} .dot.m{background:var(--morno)} .dot.f{background:var(--frio)}
.alerta{margin:26px 0 0;padding:16px 18px;background:var(--surface);border:1px solid var(--rule);
  border-left:3px solid var(--accent);border-radius:3px;box-shadow:var(--shadow)}
.alerta p{margin:0;font-size:14.5px;color:var(--ink-2)}
.alerta b{color:var(--ink)}
code{font:500 12.5px/1.4 "IBM Plex Mono",monospace;color:var(--accent-2)}
h2{font:700 12px/1 "IBM Plex Mono",monospace;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-3);margin:52px 0 18px;padding-bottom:9px;border-bottom:1px solid var(--rule)}
.bloco{background:var(--surface);border:1px solid var(--rule);border-radius:3px;
  box-shadow:var(--shadow);margin-bottom:16px;overflow:hidden}
.cab{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding:18px 22px 0}
.cab h3{font:700 21px/1.2 Poppins,sans-serif;margin:0;letter-spacing:-.015em}
.tag{font:600 10.5px/1 "IBM Plex Mono",monospace;letter-spacing:.1em;text-transform:uppercase;
  padding:5px 9px;border-radius:2px}
.tag.q{background:var(--quente-bg);color:var(--quente)}
.tag.m{background:var(--morno-bg);color:var(--morno)}
.tag.f{background:var(--frio-bg);color:var(--frio)}
.quem{margin:8px 22px 0;font-size:14px;color:var(--ink-3)}
.fala{margin:16px 22px;padding:20px 22px;background:var(--surface-2);border:1px solid var(--rule-2);
  border-left:3px solid var(--rule);border-radius:3px}
.bloco.q .fala{border-left-color:var(--quente)}
.bloco.m .fala{border-left-color:var(--morno)}
.bloco.f .fala{border-left-color:var(--frio)}
.fala p{margin:0;font:400 17px/1.62 Inter,system-ui,sans-serif;color:var(--ink)}
.fala b{font-weight:600;box-shadow:inset 0 -.5em 0 var(--quente-bg)}
.bloco.m .fala b{box-shadow:inset 0 -.5em 0 var(--morno-bg)}
.bloco.f .fala b{box-shadow:inset 0 -.5em 0 var(--frio-bg)}
.notas{list-style:none;margin:0;padding:0 22px 20px;display:flex;flex-direction:column;gap:9px}
.notas li{font-size:14px;color:var(--ink-2);padding-left:20px;position:relative}
.notas li::before{content:"→";position:absolute;left:0;color:var(--ink-3);font-size:13px}
.notas li.nao::before{content:"⊘";color:var(--accent)}
.notas li b{color:var(--ink);font-weight:600}
ol.ordem{counter-reset:o;list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
ol.ordem li{counter-increment:o;display:grid;grid-template-columns:34px 1fr;gap:14px;
  background:var(--surface);border:1px solid var(--rule);border-radius:3px;padding:15px 18px}
ol.ordem li::before{content:counter(o);font:700 17px/1 Poppins,sans-serif;color:var(--accent);
  font-variant-numeric:tabular-nums}
ol.ordem b{display:block;margin-bottom:3px}
ol.ordem span{font-size:14px;color:var(--ink-2)}
footer{margin-top:56px;padding-top:20px;border-top:1px solid var(--rule);font-size:13px;color:var(--ink-3)}
footer p{margin:0 0 9px;max-width:72ch}
footer b{color:var(--ink-2);font-weight:600}

/* — sumário — */
nav.sumario{margin:0 0 34px}
nav.sumario ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px}
nav.sumario li{display:grid;grid-template-columns:26px 1fr;gap:12px;align-items:baseline;
  padding:11px 12px 11px 0;border-bottom:1px solid var(--rule-2)}
nav.sumario li:last-child{border-bottom:0}
nav.sumario .n{font:600 12px/1.5 "IBM Plex Mono",monospace;color:var(--ink-3);
  font-variant-numeric:tabular-nums}
nav.sumario a{font:600 17px/1.25 Poppins,system-ui,sans-serif;letter-spacing:-.012em;color:var(--ink);
  text-decoration:none;border-bottom:1.5px solid transparent}
nav.sumario a:hover{color:var(--accent);border-bottom-color:var(--accent)}
nav.sumario .oq{display:block;margin-top:4px;font-size:13.5px;color:var(--ink-2);max-width:62ch}
nav.sumario .tag{margin-left:9px;vertical-align:2px}

/* — abas de versão — */
.vtabs{display:flex;gap:6px;margin:15px 22px 0}
.vtabs button{font:600 10.5px/1 "IBM Plex Mono",monospace;letter-spacing:.09em;text-transform:uppercase;
  padding:8px 12px;border:1px solid var(--rule);background:var(--surface-2);color:var(--ink-3);
  border-radius:2px;cursor:pointer}
.vtabs button:hover{color:var(--ink)}
.vtabs button[aria-selected="true"]{background:var(--accent);color:var(--ground);border-color:var(--accent)}

/* — passos — */
a.volta{margin-left:auto;font:600 10.5px/1 "IBM Plex Mono",monospace;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-3);text-decoration:none}
a.volta:hover{color:var(--accent)}
ol.passos{list-style:none;margin:14px 0 0;padding:0 22px}
li.passo{padding:15px 0;border-top:1px solid var(--rule-2)}
li.passo:first-child{border-top:0;padding-top:2px}
.rot{margin:0;font:600 10.5px/1.4 "IBM Plex Mono",monospace;letter-spacing:.11em;
  text-transform:uppercase;color:var(--ink-3)}
.rot .num{color:var(--accent);font-weight:600;margin-right:7px}
li.passo .fala{margin:11px 0 0}
li.passo.skip .rot{color:var(--ink-3);opacity:.8}
.porque{margin:7px 0 0;font-size:13.5px;color:var(--ink-3);max-width:64ch}
.ram{margin:9px 0 0;padding:9px 0 0 14px;border-left:2px solid var(--rule)}
.ram .r{display:block;font:600 10.5px/1 "IBM Plex Mono",monospace;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-3);margin-bottom:5px}
.ram p{margin:0;font:400 15.5px/1.55 Inter,system-ui,sans-serif;color:var(--ink-2)}
.ram.sim{border-left-color:var(--good)} .ram.nao{border-left-color:var(--accent)}
.obj{margin:11px 0 0;padding:12px 14px;background:var(--surface-2);border:1px solid var(--rule-2);
  border-radius:3px}
.obj .q{margin:0 0 6px;font-size:14px;font-weight:600;color:var(--ink)}
.obj p.a{margin:0;font:400 15.5px/1.55 Inter,system-ui,sans-serif;color:var(--ink-2)}
.obj + .obj{margin-top:7px}

/* — barra de edição — */
.editbar{position:fixed;top:14px;right:14px;z-index:50;display:flex;align-items:center;gap:8px;
  background:var(--surface);border:1px solid var(--rule);border-radius:3px;padding:8px 10px;
  box-shadow:var(--shadow)}
.editbar button{font:600 10.5px/1 "IBM Plex Mono",monospace;letter-spacing:.09em;text-transform:uppercase;
  padding:8px 11px;border:1px solid var(--rule);background:var(--surface-2);color:var(--ink-2);
  border-radius:2px;cursor:pointer}
.editbar button:hover{color:var(--ink);border-color:var(--ink-3)}
.editbar button.on{background:var(--accent);border-color:var(--accent);color:var(--ground)}
.editbar .st{font:400 12px/1.3 "IBM Plex Mono",monospace;color:var(--ink-3);max-width:22ch}
.editbar .st.erro{color:var(--accent)}
body.editando [data-p]{outline:1px dashed var(--rule);outline-offset:4px;border-radius:2px}
body.editando [data-p]:hover{outline-color:var(--ink-3)}
body.editando [data-p]:focus{outline:2px solid var(--accent);outline-offset:4px;background:var(--surface-2)}
body.editando .vtabs button,body.editando a.volta{opacity:.55}
@media print{.editbar{display:none}}

@media (max-width:640px){
  .fala{margin:14px 16px;padding:16px 17px}
  .fala p{font-size:16.5px}
  .cab,.quem,.notas{padding-left:17px;padding-right:17px}
  ol.passos{padding-left:17px;padding-right:17px}
  .vtabs{margin-left:17px;margin-right:17px}
  nav.sumario a{font-size:16px}
  .editbar{top:auto;bottom:12px;right:12px}
}
"""

CORPO = """
<div class="editbar" id="editbar">
  <button id="btn-editar" type="button">editar</button>
  <button id="btn-salvar" type="button" hidden>salvar</button>
  <span class="st" id="st"></span>
</div>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Canal de contadores · abordagem por temperatura</p>
  <h1>O morno abre o frio</h1>
  <p class="tese">Os escritórios alcançáveis pela sua rede não são contatos mornos — <b>a ponte é</b>.
  Quem você conhece é um assistente contábil; o escritório e o sócio que decide seguem frios.
  Todo roteiro abaixo existe para transformar uma coisa na outra.</p>
</header>

<table class="mapa">
  <tr><th>Categoria</th><th>Quem é</th></tr>
  <tr><td><span class="dot q"></span><b>Quente</b></td>
      <td>Família e amigos próximos. Maior potencial de fechamento, segundo o próprio material de treinamento</td></tr>
  <tr><td><span class="dot m"></span><b>Morno</b></td>
      <td>Rede profissional — colegas, fornecedores, parceiros</td></tr>
  <tr class="sub"><td>ponte</td><td>Declaram contabilidade na empresa ou no cargo</td></tr>
  <tr class="sub"><td>comprador</td><td>O restante da rede</td></tr>
  <tr><td><span class="dot f"></span><b>Frio</b></td>
      <td>Escritórios mapeados · empresas em CNAE de tese</td></tr>
</table>

<div class="alerta">
  <p><b>Onde isto diverge do material de treinamento.</b> Os scripts do material abrem com “estou
  trabalhando com consórcio”.__CRED_FRASE__ Aqui a abertura é a
  conta do interlocutor — com número, não com teoria — e o fechamento é dizer <b>onde o consórcio
  perde</b>. E o corte tributário <b>não</b> abre conversa com contador: para ele é trivial. Uma
  ressalva: “não tem juros” dito sozinho fica incompleto — existe taxa de administração, e para um
  contador omitir isso sai caro.</p>
</div>

<h2 id="sumario">Os sete roteiros</h2>

<div class="alerta" style="border-left-color:var(--ink-3);margin-bottom:26px">
  <p><b>Os oito passos são sempre os mesmos.</b> Abertura · a ponte · qualificação · a conta · o
  desqualificador · o pedido · objeções · fechamento. Roteiro que não usa um passo <b>diz por que
  pulou</b>. E cada um tem <b>duas versões</b>: com indicação, quando alguém fez a ponte, e sem
  indicação, quando você chegou sozinho — só a abertura e a ponte mudam, o resto se mantém.</p>
</div>

<nav class="sumario"><ol id="sumario-lista"></ol></nav>

<div id="roteiros"></div>

<h2>A ordem de execução</h2>
<ol class="ordem">
  <li><b>Levantar os quentes</b><span>O exercício de nomes do material de treinamento. Maior
  fechamento, e é a única frente que ninguém faz por você.</span></li>
  <li><b>Disparar os mornos-ponte</b><span>Barato, e converte escritórios frios em conversas mornas.</span></li>
  <li><b>Escritórios de 1ª onda, em paralelo</b><span>Melhor encaixe da cidade. Exigem a sequência completa, sem atalho.</span></li>
  <li><b>Mornos compradores em ondas semanais</b><span>Volume sem queimar a lista.</span></li>
</ol>
<p style="margin:18px 0 0;font-size:14.5px;color:var(--ink-2);max-width:66ch">As frentes 2 e 3 rodam
juntas de propósito: o caminho quente converte melhor, o frio qualificado dá volume de lead
qualificado. O número do mês 1 precisa dos dois.</p>

<footer>
  <p><b>Compliance.</b> Consórcio é sistema de aquisição de bens, não investimento, e não produz
  rendimento. Não há data de contemplação garantida. Taxa de administração sempre aberta.</p>
  <p><b>Antes de ir a campo.</b> Validar os roteiros contra o material aprovado da __ADM__.</p>
  <p><b>Premissas.</b> Os números entre colchetes saem do calculista, com a taxa de administração e o
  prazo de config/consultor.json. Parâmetro ainda não confirmado com a __ADM__, em campo:
  “com as premissas que uso hoje; fecho os números reais essa semana”.</p>
  <p><b>O buraco.</b> Sem lista de quentes, falta a categoria de maior fechamento, segundo o
  material de treinamento.</p>
  <p><b>Edição.</b> O botão <b>editar</b> grava direto neste arquivo pelo servidor local
  (<code>bash scripts/servir.sh</code>). Aberto sem o servidor, a página só lê. O desenho vem de
  <code>scripts/design.py</code>; para reaplicá-lo sem tocar no texto, rode
  <code>python3 scripts/gerar-roteiros.py</code>.</p>
</footer>
</div>
"""

JS = r"""
const DADOS = JSON.parse(document.getElementById('dados').textContent);
const ORDEM = ['sem','com'];
const sel = {};            // id do roteiro -> versão visível
let editando = false, sujo = false;

const el = (t,c) => { const e = document.createElement(t); if(c) e.className = c; return e; };

function ed(no, caminho, html){ no.dataset.p = caminho; no.innerHTML = html || ''; return no; }
function porCaminho(p, val){
  const ps = p.split('.'); let o = DADOS.roteiros;
  for (let i=0;i<ps.length-1;i++) o = o[ps[i]];
  o[ps[ps.length-1]] = val;
}

function passoNo(passo, base){
  const li = el('li','passo' + (passo.skip ? ' skip' : ''));
  const rot = el('p','rot');
  const num = el('span','num'); num.textContent = passo.n; rot.appendChild(num);
  rot.appendChild(ed(el('span'), base+'.rot', passo.rot));
  li.appendChild(rot);

  if (passo.fala){
    const f = el('div','fala'); f.appendChild(ed(el('p'), base+'.fala', passo.fala)); li.appendChild(f);
  }
  (passo.rams||[]).forEach((r,k) => {
    const d = el('div','ram ' + (r.t||''));
    d.appendChild(ed(el('span','r'), base+'.rams.'+k+'.r', r.r));
    d.appendChild(ed(el('p'), base+'.rams.'+k+'.txt', r.txt));
    li.appendChild(d);
  });
  (passo.objs||[]).forEach((o,k) => {
    const d = el('div','obj');
    d.appendChild(ed(el('p','q'), base+'.objs.'+k+'.q', o.q));
    d.appendChild(ed(el('p','a'), base+'.objs.'+k+'.a', o.a));
    li.appendChild(d);
  });
  if (passo.porque) li.appendChild(ed(el('p','porque'), base+'.porque', passo.porque));
  return li;
}

function blocoNo(r, i){
  const v = sel[r.id], ver = r.versoes[v], base = i+'.versoes.'+v;
  const b = el('div','bloco ' + r.temp); b.id = r.id;

  const cab = el('div','cab');
  const h = el('h3'); h.appendChild(document.createTextNode(r.n + ' · '));
  h.appendChild(ed(el('span'), i+'.titulo', r.titulo));
  cab.appendChild(h);
  (r.tags||[]).forEach((t,k) => {
    const s = el('span','tag ' + r.temp); s.dataset.p = i+'.tags.'+k; s.innerHTML = t; cab.appendChild(s);
  });
  const volta = el('a','volta'); volta.href = '#sumario'; volta.textContent = 'índice'; cab.appendChild(volta);
  b.appendChild(cab);

  const tabs = el('div','vtabs');
  ORDEM.filter(k => r.versoes[k]).forEach(k => {
    const bt = el('button'); bt.type = 'button'; bt.textContent = r.versoes[k].rotulo;
    bt.setAttribute('aria-selected', k === v ? 'true' : 'false');
    bt.onclick = () => { sel[r.id] = k; render(); document.getElementById(r.id).scrollIntoView({block:'start'}); };
    tabs.appendChild(bt);
  });
  b.appendChild(tabs);

  b.appendChild(ed(el('p','quem'), base+'.quem', ver.quem));

  const ol = el('ol','passos');
  ver.passos.forEach((p,j) => ol.appendChild(passoNo(p, base+'.passos.'+j)));
  b.appendChild(ol);

  if ((ver.notas||[]).length){
    const ul = el('ul','notas');
    ver.notas.forEach((n,k) => {
      const li = el('li', n.tipo === 'nao' ? 'nao' : '');
      ul.appendChild(ed(li, base+'.notas.'+k+'.txt', n.txt));
    });
    b.appendChild(ul);
  }
  return b;
}

function render(){
  const lista = document.getElementById('sumario-lista'); lista.innerHTML = '';
  const alvo = document.getElementById('roteiros'); alvo.innerHTML = '';
  DADOS.roteiros.forEach((r,i) => {
    if (!sel[r.id]) sel[r.id] = r.padrao;
    const li = el('li');
    const n = el('span','n'); n.textContent = r.n; li.appendChild(n);
    const dir = el('span');
    const a = el('a'); a.href = '#' + r.id; a.innerHTML = r.titulo; dir.appendChild(a);
    (r.tags||[]).forEach(t => { const s = el('span','tag ' + r.temp); s.innerHTML = t; dir.appendChild(s); });
    dir.appendChild(ed(el('span','oq'), i+'.oq', r.oq));
    li.appendChild(dir); lista.appendChild(li);
    alvo.appendChild(blocoNo(r, i));
  });
  if (editando) marcarEditaveis(true);
}

function marcarEditaveis(on){
  document.querySelectorAll('#roteiros [data-p], #sumario-lista [data-p]')
    .forEach(n => n.contentEditable = on ? 'true' : 'false');
  document.body.classList.toggle('editando', on);
}

function st(txt, erro){
  const s = document.getElementById('st');
  s.textContent = txt || ''; s.classList.toggle('erro', !!erro);
}

document.addEventListener('input', e => {
  const n = e.target.closest('[data-p]');
  if (!n || !editando) return;
  porCaminho(n.dataset.p, n.innerHTML);
  sujo = true; st('não salvo');
});

document.getElementById('btn-editar').onclick = () => {
  editando = !editando;
  marcarEditaveis(editando);
  document.getElementById('btn-editar').classList.toggle('on', editando);
  document.getElementById('btn-editar').textContent = editando ? 'editando' : 'editar';
  document.getElementById('btn-salvar').hidden = !editando;
  st(editando ? (location.protocol === 'file:' ? 'sem servidor: não salva' : 'clique no texto') : '');
};

document.getElementById('btn-salvar').onclick = async () => {
  if (location.protocol === 'file:'){ st('abra pelo servidor local', true); return; }
  st('salvando…');
  try {
    const r = await fetch('/api/roteiros', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(DADOS)
    });
    const t = await r.text();
    if (!r.ok) throw new Error(t || r.status);
    sujo = false; st('salvo em ' + new Date().toLocaleTimeString('pt-BR').slice(0,5));
  } catch (err){ st('erro: ' + err.message, true); }
};

window.addEventListener('beforeunload', e => { if (sujo){ e.preventDefault(); e.returnValue = ''; } });

render();
"""


def dados_vigentes(cfg):
    """A verdade é o bloco JSON da página. A semente só entra quando ele não existe."""
    if os.path.exists(DESTINO):
        html = io.open(DESTINO, encoding="utf-8").read()
        i = html.find(ABRE)
        if i >= 0:
            j = html.find(FECHA, i)
            if j > i:
                try:
                    d = json.loads(html[i + len(ABRE):j])
                    if d.get("roteiros"):
                        return d, "página (edições preservadas)"
                except json.JSONDecodeError as e:
                    print(f"  ⚠️  bloco de dados ilegível ({e}); caindo na semente")
    from roteiros_seed import dados
    return dados(cfg), "roteiros_seed.py"


def main():
    cfg = carregar()
    dados, origem = dados_vigentes(cfg)
    corpo = CORPO.replace("__ADM__", valor(cfg, "administradora.nome") or "administradora")
    # sem credencial declarada, a frase sai inteira; com ela, entra o valor — nunca marcador
    creds = valor(cfg, "consultor.credenciais") or []
    cred_frase = (f" Correto para um vendedor sem credencial — e desperdiça o fato de você ser "
                  f"{html.escape(str(creds[0]))}." if creds else "")
    corpo = corpo.replace("__CRED_FRASE__", cred_frase)
    pagina = (
        '<meta charset="utf-8">\n<title>Roteiros por Temperatura</title>\n'
        + design.FONTES + "\n<style>" + design.TOKENS + CSS + "</style>\n"
        + corpo
        + "\n" + ABRE + "\n"
        + json.dumps(dados, ensure_ascii=False, indent=1)
        + "\n" + FECHA + "\n\n<script>\n" + JS + "\n</script>\n"
    )
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    io.open(DESTINO, "w", encoding="utf-8").write(pagina)
    n = len(dados["roteiros"])
    v = sum(len(r["versoes"]) for r in dados["roteiros"])
    print(f"→ saida/roteiros.html  ({len(pagina)//1024} KB)")
    print(f"   {n} roteiros · {v} versões · conteúdo de: {origem}")


if __name__ == "__main__":
    main()
