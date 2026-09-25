#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controles padrão das apresentações do consultor — um só jeito para todo deck.

O padrão de todas as apresentações:

    alto, à esquerda   marca: nome do consultor (config), link para o site dele se houver
    alto, à direita    contador "01 / 13"
    embaixo, centro    bolinhas de continuidade — a ativa alonga e acende
    embaixo, direita   três comandos discretos, menores e apagados:
                         visão geral (O) · tela cheia (F) · apresentador (P)
                       | anterior e próximo, botões redondos
    dica               "use as setas, as bolinhas ou arraste", some na 1ª navegação

O apresentador (notas e cronômetro) **some sozinho quando o deck não tem notas**. No Chrome e no
Edge, com monitor estendido, ele manda a apresentação em tela cheia para o outro monitor e abre as
notas na tela de quem apresenta (API de gerenciamento de janelas, com permissão pedida uma vez).
Sem segundo monitor, ou em outro navegador, abre só as notas e mostra como levar a apresentação
para a sala.

O módulo tem um núcleo (CSS, marcação e JS) e dois jeitos de ligar num deck:

    aplicar_marp(html)     deck exportado pelo Marp: esconde os controles nativos e liga
                           os comandos aos do Marp (visão geral e apresentador nativos)
    css() + html() + js()  deck feito à mão (o do consórcio): o deck publica
                           `window.deckControles = {total, atual, ir, ouvir, slides}` e o
                           núcleo faz o resto — a visão geral, aqui, é a grade do módulo

Cores de design.ESPELHO, como todo artefato do repo. Nome e site da marca vêm de
config/consultor.json (`consultor.nome_curto` ou `consultor.nome`, e `consultor.site`).
"""
import html as _html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design
from config import carregar, exigir, valor

E = design.ESPELHO
BRILHO, ACENTO, CINZA, CINZA_ESCURO = E["accent-400"], E["accent-500"], E["dark-400"], E["dark-500"]


def _marca():
    """Nome e link da marca no alto, à esquerda. Sem site na config, o nome entra sem link."""
    cfg = carregar()
    nome = valor(cfg, "consultor.nome_curto") or exigir(cfg, "consultor.nome")
    site = valor(cfg, "consultor.site")
    if not site:
        return f'<span class="marca">{_html.escape(nome)}</span>'
    url = site if site.startswith(("http://", "https://")) else "https://" + site
    return (f'<a class="marca" href="{_html.escape(url, quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{_html.escape(nome)}</a>')


def css():
    return '<style id="controles-deck">' + css_puro() + "</style>\n"


def css_puro():
    return f"""
.cd{{position:fixed;inset:0;z-index:40;pointer-events:none}}
.cd>*{{pointer-events:auto}}
.cd .top{{position:absolute;inset-inline:0;top:0;display:flex;align-items:center;justify-content:space-between;
  padding:20px clamp(22px,4vw,40px);pointer-events:none}}
.cd .top span,.cd .top .marca{{font:600 11.5px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.18em;
  text-transform:uppercase;color:{CINZA_ESCURO};text-shadow:0 1px 3px rgba(0,0,0,.95),0 0 16px rgba(0,0,0,.85)}}
/* Abre em aba nova de propósito: sair da apresentação encerraria a visita. */
.cd .top .marca{{pointer-events:auto;text-decoration:none;transition:color .2s}}
.cd .top .marca:hover{{color:{BRILHO}}}
.cd .top .n b{{color:{BRILHO};font-weight:700}}
.cd .pontos{{position:absolute;bottom:26px;left:50%;transform:translateX(-50%);display:flex;align-items:center;
  gap:10px;padding:11px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.10);
  background:rgba(0,0,0,.60);backdrop-filter:blur(6px)}}
.cd .pontos i{{display:block;width:8px;height:8px;border-radius:999px;cursor:pointer;background:rgba(255,255,255,.25);
  transition:width .5s cubic-bezier(.76,0,.24,1),background .3s,box-shadow .3s}}
.cd .pontos i:hover{{background:rgba(255,255,255,.45)}}
.cd .pontos i.on{{width:32px;background:linear-gradient(90deg,{ACENTO},{BRILHO});box-shadow:0 0 14px {design.rgba(BRILHO, .55)}}}
.cd nav{{position:absolute;bottom:20px;right:clamp(22px,4vw,40px);display:flex;align-items:center;gap:9px}}
.cd nav button{{width:44px;height:44px;border-radius:999px;border:1px solid rgba(255,255,255,.16);
  background:rgba(255,255,255,.04);color:#D1D5DB;cursor:pointer;display:grid;place-items:center;padding:0;
  font:400 17px/1 Inter,sans-serif;transition:border-color .2s,color .2s,background .2s,opacity .2s}}
.cd nav button:hover:not(:disabled){{border-color:{BRILHO};color:{BRILHO};background:{design.rgba(BRILHO, .08)}}}
.cd nav button:disabled{{opacity:.28;cursor:default}}
.cd nav button.mini{{width:32px;height:32px;border-color:rgba(255,255,255,.08);background:transparent;color:{CINZA};opacity:.5}}
.cd nav button.mini:hover{{opacity:1}}
.cd nav button.mini svg{{width:15px;height:15px}}
.cd nav button[hidden]{{display:none}}
.cd nav .sep{{width:1px;height:22px;background:rgba(255,255,255,.12);margin:0 3px}}
.cd .dica{{position:absolute;bottom:5.4rem;left:50%;transform:translateX(-50%);margin:0;white-space:nowrap;
  pointer-events:none;font:400 12px/1 Inter,system-ui,sans-serif;color:{CINZA_ESCURO};transition:opacity .5s}}
.cd .dica.off{{opacity:0}}
.cd .aviso{{position:absolute;bottom:84px;right:clamp(22px,4vw,40px);max-width:340px;margin:0;padding:12px 16px;
  border-radius:12px;border:1px solid {design.rgba(BRILHO, .35)};background:rgba(0,0,0,.85);backdrop-filter:blur(6px);
  font:400 13px/1.45 Inter,system-ui,sans-serif;color:#E5E7EB;transition:opacity .4s}}
.cd .aviso[hidden]{{display:none}}
@media (max-height:800px){{.cd .top,.cd nav{{transform:scale(.9)}}.cd .pontos{{transform:translateX(-50%) scale(.9)}}}}

/* Celular: em 375px as bolinhas centralizadas e a nav à direita se sobrepõem em
   quase 150px. Aqui as bolinhas encostam à esquerda, as setas ficam à direita e
   os botões de visão geral, tela cheia e apresentador saem — os três são de
   quem apresenta no computador, não de quem lê no telefone. Vem depois da
   regra de altura de propósito: em paisagem as duas valem, e aqui o transform
   precisa ganhar. */
@media (max-width:640px){{
  .cd .pontos{{left:clamp(16px,4vw,22px);transform:none;gap:7px;padding:9px 12px}}
  .cd .pontos i{{width:6px;height:6px}}
  .cd .pontos i.on{{width:22px}}
  .cd nav{{bottom:18px;right:clamp(16px,4vw,22px);gap:7px;transform:none}}
  .cd nav button.mini,.cd nav .sep{{display:none}}
  .cd nav button{{width:40px;height:40px}}
}}

/* Visão geral do módulo — para deck que não traz a sua. Miniaturas são cópias dos slides. */
.cd-visao{{position:fixed;inset:0;z-index:60;background:rgba(0,0,0,.92);overflow-y:auto;padding:48px clamp(22px,4vw,56px)}}
.cd-visao[hidden]{{display:none}}
.cd-visao .cd-lista{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px}}
.cd-visao .cd-miniatura{{position:relative;aspect-ratio:var(--proporcao,16/9);overflow:hidden;border-radius:10px;cursor:pointer;
  border:1px solid rgba(255,255,255,.12);background:#000;transition:border-color .2s}}
.cd-visao .cd-miniatura:hover,.cd-visao .cd-miniatura.on{{border-color:{BRILHO}}}
.cd-visao .cd-miniatura .cd-palco{{position:absolute;top:0;left:0;width:100vw;height:100vh;transform-origin:0 0;pointer-events:none}}
.cd-visao .cd-miniatura .cd-num{{position:absolute;left:10px;bottom:8px;z-index:2;font:600 11px/1 "IBM Plex Mono",monospace;
  color:#E5E7EB;text-shadow:0 1px 3px #000}}
body.cd-aberta .cd{{display:none}}
"""


_SVG = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'


def html():
    return f"""
<div class="cd" id="cd">
  <div class="top">
    {_marca()}
    <span class="n"><b id="cd-n">01</b> / <span id="cd-t">01</span></span>
  </div>
  <div class="pontos" id="cd-p" role="tablist" aria-label="Navegação da apresentação"></div>
  <p class="dica" id="cd-dica">use as setas, as bolinhas ou arraste</p>
  <p class="aviso" id="cd-aviso" hidden></p>
  <nav>
    <button class="mini" id="cd-visao" title="Visão geral (O)" aria-label="Visão geral">
      <svg {_SVG}><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg></button>
    <button class="mini" id="cd-cheia" title="Tela cheia (F)" aria-label="Tela cheia">
      <svg {_SVG}><path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"/></svg></button>
    <button class="mini" id="cd-apresentador" title="Apresentar: sala e notas (P)" aria-label="Apresentar em dois monitores" hidden>
      <svg {_SVG}><rect x="1.5" y="4" width="11" height="8" rx="1"/><path d="M5 15h4M7 12v3"/><rect x="11.5" y="8" width="11" height="8" rx="1"/><path d="M15 19h4M17 16v3"/></svg></button>
    <span class="sep"></span>
    <button id="cd-ant" aria-label="Slide anterior">&#8249;</button>
    <button id="cd-pro" aria-label="Próximo slide">&#8250;</button>
  </nav>
</div>
<div class="cd-visao" id="cd-grade" hidden><div class="cd-lista"></div></div>
"""


def js():
    """Núcleo. Espera `window.deckControles`:
         total, atual() → índice, ir(k), ouvir(fn) — chama fn a cada troca de slide,
         slides() → elementos que viram miniatura na visão geral do módulo;
       e, opcionais, quando o deck traz os seus: visao(), telaCheia(), apresentador(),
       temNotas. Sem temNotas verdadeiro, o botão do apresentador não aparece."""
    return "<script>" + js_puro() + "</script>\n"


def js_puro():
    return """
(function(){
  var d=window.deckControles, cd=document.getElementById('cd');
  if(!d||!d.total||!cd||cd.dataset.ligado) return;
  cd.dataset.ligado='1';
  var $=function(id){ return document.getElementById(id); };
  var n=$('cd-n'), p=$('cd-p'), dica=$('cd-dica'), ant=$('cd-ant'), pro=$('cd-pro'),
      grade=$('cd-grade'), primeira=null, tocou=false;
  var dois=function(x){ return String(x).padStart(2,'0'); };
  $('cd-t').textContent=dois(d.total);
  var pontos=[];
  for(var j=0;j<d.total;j++){ (function(j){
    var i=document.createElement('i'); i.setAttribute('role','tab'); i.title='Slide '+(j+1);
    i.onclick=function(){ d.ir(j); }; p.appendChild(i); pontos.push(i); })(j); }
  function pintar(){
    var i=d.atual();
    if(primeira===null) primeira=i; else if(i!==primeira && !tocou){ tocou=true; dica.classList.add('off'); }
    n.textContent=dois(i+1);
    pontos.forEach(function(el,j){ el.classList.toggle('on', j===i); el.setAttribute('aria-selected', j===i?'true':'false'); });
    ant.disabled=(i===0); pro.disabled=(i===d.total-1);
  }
  ant.onclick=function(){ d.ir(d.atual()-1); }; pro.onclick=function(){ d.ir(d.atual()+1); };

  function telaCheia(){
    if(d.telaCheia) return d.telaCheia();
    if(document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen();
  }
  function fecharGrade(){ grade.hidden=true; document.body.classList.remove('cd-aberta'); }
  function abrirGrade(){
    var caixa=grade.firstChild; caixa.innerHTML='';
    grade.style.setProperty('--proporcao', innerWidth+'/'+innerHeight);
    d.slides().forEach(function(s,j){
      var m=document.createElement('div'); m.className='cd-miniatura'+(j===d.atual()?' on':'');
      var palco=document.createElement('div'); palco.className='cd-palco';
      var c=s.cloneNode(true); c.classList.add('on'); c.removeAttribute('id');
      palco.appendChild(c); m.appendChild(palco);
      var num=document.createElement('span'); num.className='cd-num'; num.textContent=dois(j+1); m.appendChild(num);
      m.onclick=function(){ fecharGrade(); d.ir(j); };
      caixa.appendChild(m);
    });
    grade.hidden=false; document.body.classList.add('cd-aberta');
    [].forEach.call(caixa.children,function(m){ m.firstChild.style.transform='scale('+(m.clientWidth/innerWidth)+')'; });
  }
  function visao(){ if(d.visao) return d.visao(); if(grade.hidden) abrirGrade(); else fecharGrade(); }
  $('cd-visao').onclick=visao; $('cd-cheia').onclick=telaCheia;
  // Apresentar: as notas abrem primeiro, ainda dentro do clique (senão o bloqueador de janela
  // barra), e a apresentação vai em tela cheia para o outro monitor quando o navegador deixa.
  var avisoT=null;
  function avisar(txt){ var a=$('cd-aviso'); a.textContent=txt; a.hidden=false;
    clearTimeout(avisoT); avisoT=setTimeout(function(){ a.hidden=true; }, 9000); }
  var MANUAL='As notas abriram em outra janela. Arraste esta janela para o monitor da sala e aperte F.';
  async function apresentar(){
    d.apresentador();
    if(!('getScreenDetails' in window) || !window.screen.isExtended){ avisar(MANUAL); return; }
    var tela;
    try{ tela=await window.getScreenDetails(); }
    catch(e){
      avisar('O navegador não liberou o controle das telas. ' + MANUAL + ' Para automatizar, permita "gerenciar janelas" para este site.');
      return;
    }
    var outra=tela.screens.filter(function(t){ return t!==tela.currentScreen; })[0];
    if(!outra){ avisar(MANUAL); return; }
    try{ await document.documentElement.requestFullscreen({screen: outra}); }
    catch(e){
      // Na primeira vez, o pedido de permissão consome o clique: o segundo clique já vai direto.
      avisar('Permissão registrada. Clique de novo em Apresentar para levar esta janela ao monitor da sala.');
    }
  }
  if(d.temNotas && d.apresentador){
    $('cd-apresentador').hidden=false; $('cd-apresentador').onclick=apresentar;
    // P faz o mesmo que o botão, também nos decks do Marp, que têm o P próprio.
    addEventListener('keydown',function(e){
      if(e.metaKey||e.ctrlKey||e.altKey||!cd.isConnected) return;
      if(e.key==='p'||e.key==='P'){ e.preventDefault(); e.stopImmediatePropagation(); apresentar(); }
    }, true);
  }

  if(!d.visao){
    addEventListener('keydown',function(e){
      if(e.metaKey||e.ctrlKey||e.altKey||!cd.isConnected) return;
      if(e.key==='o'||e.key==='O'){ e.preventDefault(); visao(); }
      else if(e.key==='f'||e.key==='F'){ e.preventDefault(); telaCheia(); }
      else if(e.key==='Escape' && !grade.hidden){ fecharGrade(); }
    });
  }
  d.ouvir(pintar);
  pintar();
})();
"""


# ── Marp ────────────────────────────────────────────────────────────────────
_MARP_CSS = """
<style>
body[data-bespoke-view] .bespoke-marp-osc{display:none!important}
body:not([data-bespoke-view=""]) .cd{display:none}
body:has(.bespoke-marp-overview[data-open="1"]) .cd{display:none}
</style>
"""

_MARP_ADAPTADOR = """
<script>
(function(){
  var slides=[].slice.call(document.querySelectorAll('svg[data-marpit-svg]'));
  var osc=function(k){ var b=document.querySelector('.bespoke-marp-osc [data-bespoke-marp-osc="'+k+'"]'); if(b) b.click(); };
  var ouvintes=[];
  var avisar=function(){ ouvintes.forEach(function(f){ f(); }); };
  var obs=new MutationObserver(avisar);
  slides.forEach(function(s){ obs.observe(s,{attributes:true,attributeFilter:['class']}); });
  addEventListener('hashchange',avisar);
  window.deckControles={
    total:slides.length,
    atual:function(){ for(var j=0;j<slides.length;j++){ if(slides[j].classList.contains('bespoke-marp-active')) return j; } return 0; },
    ir:function(k){ k=Math.max(0,Math.min(slides.length-1,k)); location.hash='#'+(k+1); },
    ouvir:function(f){ ouvintes.push(f); },
    slides:function(){ return slides; },
    visao:function(){ osc('overview'); },
    telaCheia:function(){ osc('fullscreen'); },
    apresentador:function(){ osc('presenter'); },
    temNotas:[].some.call(document.querySelectorAll('.bespoke-marp-note'),function(n){ return n.textContent.trim()!==''; })
  };
})();
</script>
"""


def aplicar_marp(pagina):
    """Injeta o padrão num HTML do Marp, antes do </body>. Idempotente."""
    if 'id="controles-deck"' in pagina:
        return pagina
    fim = pagina.rfind("</body>")
    if fim == -1:
        raise ValueError("HTML sem </body> — não parece saída do Marp")
    return pagina[:fim] + css() + _MARP_CSS + html() + _MARP_ADAPTADOR + js() + pagina[fim:]
