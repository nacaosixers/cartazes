"""Nação Sixers · cartazes no estilo lambe-lambe de gráfica (1080x1350).

Duas tintas (azul e vermelho) sobre papel amarelo, branco ou azul, com textura de impressão.
Cada linha de título é esticada até a largura do cartaz, como nos cartazes de rua.

Uso:
  python cartaz.py prejogo --mandante "76ers" --visitante "Celtics" --data "Ter 10/11" \
      --horario "22h" --onde "Prime Video" --out prejogo.png
  python cartaz.py placar --mandante "Bulls" --visitante "76ers" --pm 121 --pv 127 --data "Dom 8/11" \
      --frase "O que decidiu, em uma ou duas frases com números reais." --out placar.png
  python cartaz.py direto --citacao "Frase traduzida" --autor "Nome" --contexto "Quem é e sobre o quê" \
      --fonte "Veículo, data" --out direto.png
  python cartaz.py manchete --selo Notícia --titulo "..." --texto "..." --fonte "..." --out manchete.png
      (selo: Notícia, Rumor ou Opinião)
  python cartaz.py lista --chip "Pós-jogo" --titulo "3 pontos do jogo" --item "..." --item "..." --fonte "..." --out lista.png
  python cartaz.py agenda --periodo "10/11 a 23/11" --jogo "TER 10/11|76ers x Celtics|22h" --jogo "..." --out agenda.png
  python cartaz.py cartaz --papel amarelo --linha "O 76ers|as|vermelho|300" --linha "agora em|an|azul|200" \
      --texto "Texto de apoio" --out cartaz.png   (fonte: an ou as; cor: azul, vermelho ou creme)
  python cartaz.py numero --chip "Bola de três" --numero "33" --rotulo "pontos de diferença na linha de três" \
      --texto "Celtics 22 de 49. 76ers 11 de 37." --fonte "Box score da NBA" --papel branco --kicker "Raio-X · 2 de 5" --out n.png
      (número do dia, slides do Raio-X e "neste dia na história"; papel: branco, amarelo ou azul)
  python cartaz.py perfil --pasta img        (foto de perfil, capa do X e capas de destaque)

O 76ers sai sempre em vermelho, os adversários em azul. Se o texto for longo, a letra diminui sozinha;
se mesmo assim não couber, o comando termina com erro: encurte o texto. Nunca use travessão.
Requer python playwright (Chromium já instalado) e npm (baixa as fontes na primeira execução).
"""
import argparse, base64, html, pathlib, re, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
FONT_DIR = HERE / "fonts"
AZUL, VERMELHO = "#1E3DA8", "#E3232C"
PAPEL = {"branco": "#F1F0EB", "amarelo": "#FFD71F", "azul": "#1E3DA8"}
CREME = "#F4F1E6"
COR = {"azul": AZUL, "vermelho": VERMELHO, "creme": CREME}
NOME, ARROBA = "Nação Sixers", "@nacaosixers"
CASA = ("76ers", "sixers", "philadelphia", "filadélfia")
E = html.escape

FONTS = {
    "anton": ["anton-latin-400-normal.woff2"],
    "alfa-slab-one": ["alfa-slab-one-latin-400-normal.woff2"],
    "archivo": ["archivo-latin-500-normal.woff2", "archivo-latin-700-normal.woff2", "archivo-latin-800-normal.woff2"],
}


def ensure_fonts():
    FONT_DIR.mkdir(exist_ok=True)
    for pkg, files in FONTS.items():
        if all((FONT_DIR / f).exists() for f in files):
            continue
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["npm", "pack", f"@fontsource/{pkg}", "--silent"], cwd=td, check=True, capture_output=True)
            tgz = next(pathlib.Path(td).glob("*.tgz"))
            subprocess.run(["tar", "xzf", str(tgz), "-C", td], check=True)
            for f in files:
                (FONT_DIR / f).write_bytes((pathlib.Path(td) / "package/files" / f).read_bytes())


def du(name):
    return "data:font/woff2;base64," + base64.b64encode((FONT_DIR / name).read_bytes()).decode()


def css():
    return f"""
@font-face{{font-family:AN;src:url({du('anton-latin-400-normal.woff2')}) format('woff2')}}
@font-face{{font-family:AS;src:url({du('alfa-slab-one-latin-400-normal.woff2')}) format('woff2')}}
@font-face{{font-family:AR;src:url({du('archivo-latin-500-normal.woff2')}) format('woff2');font-weight:500}}
@font-face{{font-family:AR;src:url({du('archivo-latin-700-normal.woff2')}) format('woff2');font-weight:700}}
@font-face{{font-family:AR;src:url({du('archivo-latin-800-normal.woff2')}) format('woff2');font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#888}}
.c{{position:relative;overflow:hidden;font-family:AR}}
.an{{font-family:AN;text-transform:uppercase;line-height:.92;font-weight:400}}
.as{{font-family:AS;text-transform:uppercase;line-height:.96;font-weight:400}}
.ln{{display:block;white-space:nowrap;width:max-content;max-width:none}}
.ink{{filter:url(#ink)}}
.up{{text-transform:uppercase}}
"""


# Filtro de tinta: borda levemente irregular e densidade desigual, como impressão em tipo de madeira.
DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="ink" x="-2%" y="-2%" width="104%" height="104%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="2" seed="9" result="m"/>
<feColorMatrix in="m" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .32 .8" result="dens"/>
<feComposite in="d" in2="dens" operator="in"/>
</filter></defs></svg>"""

# Papel: granulação que escurece de leve e pontinhos claros que gastam a tinta.
OVERLAYS = """<svg width="100%" height="100%" style="position:absolute;inset:0;mix-blend-mode:multiply;opacity:.55;pointer-events:none">
<filter id="gr" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="3" seed="5"/>
<feColorMatrix type="matrix" values="0 0 0 0 .42  0 0 0 0 .40  0 0 0 0 .36  0 0 0 .6 -.2"/></filter>
<rect width="100%" height="100%" filter="url(#gr)"/></svg>
<svg width="100%" height="100%" style="position:absolute;inset:0;mix-blend-mode:multiply;opacity:.22;pointer-events:none">
<filter id="mo" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".004" numOctaves="2" seed="21"/>
<feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .52  0 0 0 0 .48  0 0 0 .5 -.12"/></filter>
<rect width="100%" height="100%" filter="url(#mo)"/></svg>
<svg width="100%" height="100%" style="position:absolute;inset:0;mix-blend-mode:screen;opacity:.6;pointer-events:none">
<filter id="sp" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.05" numOctaves="1" seed="11"/>
<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 24 -18.2"/></filter>
<rect width="100%" height="100%" filter="url(#sp)"/></svg>"""


def is_home(name):
    return any(t in name.lower() for t in CASA)


def tag(text, bg=VERMELHO, fg=None, outline=False):
    fg = fg or PAPEL["branco"]
    if outline:
        return f'<span class="up" style="display:inline-block;border:4px solid {bg};color:{bg};padding:6px 16px 4px;font-weight:800;font-size:28px;letter-spacing:.12em;line-height:1">{E(text)}</span>'
    return f'<span class="up" style="display:inline-block;background:{bg};color:{fg};padding:10px 18px 8px;font-weight:800;font-size:28px;letter-spacing:.12em;line-height:1">{E(text)}</span>'


def frame(paper, kicker, foot, main, extra="", ink=AZUL, accent=VERMELHO):
    return f"""<div id="a" class="c" style="width:1080px;height:1350px;background:{paper};color:{ink}">{DEFS}
<div class="ink" style="position:absolute;inset:0">
<div style="position:absolute;left:64px;right:64px;top:44px;display:flex;justify-content:space-between;align-items:center;gap:24px">
<span class="an" style="font-size:48px;letter-spacing:.02em;line-height:1;white-space:nowrap">Nação <span style="color:{accent}">Sixers</span></span>
<span class="up" style="font-weight:800;font-size:24px;letter-spacing:.1em;white-space:nowrap">{E(kicker)}</span></div>
<div style="position:absolute;left:64px;right:64px;top:116px;height:8px;background:{ink}"></div>
{main}
<div style="position:absolute;left:64px;right:64px;top:1226px;height:8px;background:{ink}"></div>
<div class="up" style="position:absolute;left:64px;right:64px;top:1254px;display:flex;justify-content:space-between;gap:24px;font-weight:800;font-size:22px;letter-spacing:.08em;line-height:1.2">
<span style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{E(foot)}</span><span style="color:{accent};white-space:nowrap">{ARROBA}</span></div>
{extra}</div>{OVERLAYS}</div>"""


def main_box(inner, jc="center", gap=0):
    return f'<div id="m" style="position:absolute;left:64px;top:156px;width:952px;height:1044px;display:flex;flex-direction:column;justify-content:{jc};gap:{gap}px">{inner}</div>'


def prejogo(a):
    casa = is_home(a.mandante)
    adv = a.visitante if casa else a.mandante
    hora = re.sub(r"\s*de bras[ií]lia", "", a.horario, flags=re.I).strip()
    inner = f"""<span class="an ln fill" data-max="190">{E(a.quando)}</span>
<span class="as ln fill" data-max="330" style="color:{VERMELHO};text-shadow:9px 9px 0 {AZUL};margin:6px 0 14px">76ers</span>
<span class="an ln fill" data-max="150">contra o {E(adv)}</span>
<div style="display:flex;align-items:flex-end;gap:30px;border-top:8px solid {AZUL};padding-top:26px;margin-top:22px">
<span class="an ln fill" data-w="500" data-max="250" style="color:{VERMELHO};line-height:.8">{E(hora)}</span>
<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:10px;padding-bottom:4px">
<span class="up fx" style="font-weight:800;font-size:44px;line-height:1.02">de Brasília</span>
<span class="up fx" style="font-weight:800;font-size:44px;line-height:1.02">{E(a.onde)}</span>
<span class="up fx" style="font-weight:700;font-size:26px;letter-spacing:.08em;line-height:1.2;color:{VERMELHO}">{'Em casa' if casa else 'Fora de casa'} · {E(a.data)}</span>
</div></div>"""
    foot = f"{a.liga} · {a.contexto}" if a.contexto else f"{a.liga} · 76ers em português"
    return frame(PAPEL["amarelo"], "Dia de jogo", foot, main_box(inner))


def placar(a):
    pm, pv = int(a.pm), int(a.pv)
    s_pts = pm if is_home(a.mandante) else pv if is_home(a.visitante) else None
    o_pts = pv if is_home(a.mandante) else pm
    win = s_pts is not None and s_pts > o_pts

    def row(n, p, other):
        op = "opacity:.36;" if p < other else ""
        font, col = ("as", VERMELHO) if is_home(n) else ("an", AZUL)
        return f"""<div style="display:flex;align-items:center;justify-content:space-between;gap:24px;border-bottom:8px solid {AZUL};padding:10px 0 16px">
<span class="{font} ln fill" data-w="470" data-max="150" style="color:{col};{op}">{E(n)}</span>
<span class="an" style="font-size:300px;line-height:.86;{op}">{p}</span></div>"""
    label = "Vitória" if win else "Derrota" if s_pts is not None else "Final"
    sc = VERMELHO if win else AZUL
    stamp = f"""<div class="an" style="transform:rotate(-7deg);border:8px solid {sc};outline:3px solid {sc};outline-offset:7px;padding:8px 26px 4px;color:{sc};font-size:92px;letter-spacing:.05em;line-height:1;margin-right:14px">{label}</div>"""
    frase = f"""<div class="fx" style="margin-top:44px;font-weight:700;font-size:40px;line-height:1.28;border-left:10px solid {VERMELHO};padding-left:26px">{E(a.frase)}</div>""" if a.frase else ""
    inner = f"""<div style="display:flex;justify-content:space-between;align-items:center;gap:24px;padding-bottom:34px">
<div style="display:flex;flex-direction:column;gap:8px"><span class="an" style="font-size:96px;line-height:.9">Placar</span>
<span class="up" style="font-weight:800;font-size:26px;letter-spacing:.1em">{E(a.liga)} · {E(a.contexto or 'Fim de jogo')}</span></div>{stamp}</div>
{row(a.mandante, pm, pv)}{row(a.visitante, pv, pm)}{frase}"""
    return frame(PAPEL["branco"], a.data or "Placar final", "Placar final · horário de Brasília", main_box(inner))


def direto(a):
    q = a.citacao.strip().strip('"“”')
    size = 124 if len(q) <= 50 else 104 if len(q) <= 90 else 86 if len(q) <= 140 else 70
    inner = f"""<div>{tag('Direto da Filadélfia')}</div>
<div class="as" style="font-size:300px;line-height:1;height:160px;margin-top:24px;color:{VERMELHO}">“</div>
<div class="an grow" data-max="160" data-h="620" style="line-height:1.02">{E(q)}</div>
<div style="margin-top:46px;display:flex;flex-direction:column;gap:10px">
<span class="as fx" style="font-size:54px;line-height:1;color:{VERMELHO}">{E(a.autor)}</span>
<span class="fx" style="font-weight:700;font-size:32px;line-height:1.25">{E(a.contexto)}</span></div>"""
    return frame(PAPEL["branco"], a.data or "Aspas", f"Fonte: {a.fonte}" if a.fonte else "76ers em português", main_box(inner, "flex-start"))


def manchete(a):
    t = a.titulo.strip()
    size = 136 if len(t) <= 30 else 114 if len(t) <= 55 else 94 if len(t) <= 85 else 78
    s = a.selo.strip().lower()
    selo = tag(a.selo, AZUL) if s == "rumor" else tag(a.selo, AZUL, outline=True) if s.startswith("opini") else tag(a.selo)
    texto = f"""<div class="fx" style="margin-top:40px;font-weight:700;font-size:40px;line-height:1.3;border-left:10px solid {VERMELHO};padding-left:26px">{E(a.texto)}</div>""" if a.texto else ""
    inner = f"""<div>{selo}</div><div class="an grow" data-max="190" data-h="820" style="margin-top:44px;line-height:1.02">{E(t)}</div>{texto}"""
    return frame(PAPEL["branco"], a.data or "Direto da Filadélfia", f"Fonte: {a.fonte}" if a.fonte else "76ers em português", main_box(inner, "flex-start"))


def lista(a):
    fs = 46 if len(a.item) <= 3 else 42
    rows = "".join(f"""<div style="display:grid;grid-template-columns:96px minmax(0,1fr);gap:18px;align-items:start;border-top:4px solid {AZUL};padding:32px 0 28px">
<span class="as" style="font-size:92px;line-height:.82;color:{VERMELHO}">{i}</span>
<span class="fx" style="font-weight:700;font-size:{fs}px;line-height:1.26">{E(x)}</span></div>""" for i, x in enumerate(a.item, 1))
    inner = f"""<div>{tag(a.chip)}</div>
<span class="an ln fill" data-max="170" style="margin:34px 0 26px">{E(a.titulo)}</span>
<div style="border-bottom:4px solid {AZUL}">{rows}</div>"""
    return frame(PAPEL["branco"], a.data or a.chip, f"Fonte: {a.fonte}" if a.fonte else "76ers em português", main_box(inner, "flex-start"))


def agenda(a):
    n = len(a.jogo)
    if n > 8:
        sys.exit("A agenda aceita até 8 jogos por cartaz.")
    pad = {8: 11, 7: 15, 6: 20}.get(n, 26)
    rows = ""
    for raw in a.jogo:
        d, jogo, hora = [x.strip() for x in raw.split("|")]
        parts = [p.strip() for p in jogo.split(" x ")]
        casa = is_home(parts[0])
        adv = parts[1] if casa else parts[0]
        rows += f"""<div style="display:grid;grid-template-columns:200px minmax(0,1fr) auto;gap:22px;align-items:center;border-top:3px solid rgba(244,241,230,.4);padding:{pad}px 0">
<span class="an" style="font-size:46px;line-height:1">{E(d)}</span>
<div style="display:flex;align-items:baseline;gap:16px;min-width:0"><span class="an" style="font-size:58px;line-height:1;white-space:nowrap">x {E(adv)}</span>
<span class="up" style="font-weight:800;font-size:20px;letter-spacing:.12em;color:#FFD71F;white-space:nowrap">{'Em casa' if casa else 'Fora'}</span></div>
<span class="an" style="font-size:58px;line-height:1;color:#FFD71F">{E(hora)}</span></div>"""
    inner = f"""<span class="an ln fill" data-max="250" style="color:#FFD71F">Agenda</span>
<span class="up" style="font-weight:800;font-size:32px;letter-spacing:.08em;margin:18px 0 22px">{E(a.periodo)} · horário de Brasília</span>
<div style="border-bottom:3px solid rgba(244,241,230,.4)">{rows}</div>"""
    return frame(PAPEL["azul"], "Agenda da semana", "Todos os jogos no NBA League Pass", main_box(inner), ink=CREME, accent="#FFD71F")


def cartaz(a):
    paper = PAPEL[a.papel]
    ink = CREME if a.papel == "azul" else AZUL
    lines = ""
    for spec in a.linha:
        p = (spec.split("|") + ["", "an", "azul", "300"])[:4]
        txt, font, cor, mx = p[0], p[1] or "an", p[2] or "azul", p[3] or "300"
        shadow = f"text-shadow:9px 9px 0 {AZUL};" if (font == "as" and cor == "vermelho" and a.papel != "azul") else ""
        lines += f'<span class="{font} ln fill" data-max="{mx}" style="color:{COR.get(cor, AZUL)};{shadow}margin:4px 0">{E(txt)}</span>'
    texto = f"""<div class="fx" style="margin-top:34px;border-top:8px solid {ink};padding-top:28px;font-weight:700;font-size:42px;line-height:1.3">{E(a.texto)}</div>""" if a.texto else ""
    return frame(paper, a.kicker, a.rodape, main_box(lines + texto), ink=ink, accent=VERMELHO if a.papel != "azul" else "#FFD71F")


def numero(a):
    paper = PAPEL[a.papel]
    azul = a.papel == "azul"
    ink, acc = (CREME, "#FFD71F") if azul else (AZUL, VERMELHO)
    chip = tag(a.chip, "#FFD71F", fg=AZUL) if azul else tag(a.chip)
    shadow = "" if azul else f"text-shadow:10px 10px 0 {AZUL};"
    texto = f"""<div class="fx" style="margin-top:34px;font-weight:700;font-size:40px;line-height:1.3;border-left:10px solid {acc};padding-left:26px">{E(a.texto)}</div>""" if a.texto else ""
    inner = f"""<div>{chip}</div>
<span class="as ln fill" data-max="520" style="color:{acc};{shadow}margin:34px 0 18px">{E(a.numero)}</span>
<div class="an grow" data-max="104" data-h="330" style="line-height:1.02">{E(a.rotulo)}</div>{texto}"""
    foot = f"Fonte: {a.fonte}" if a.fonte else "76ers em português"
    return frame(paper, a.kicker or a.data or a.chip, foot, main_box(inner), ink=ink, accent=acc)


def sheet(w, h, paper, inner, ink=AZUL):
    return f"""<div id="a" class="c" style="width:{w}px;height:{h}px;background:{paper};color:{ink}">{DEFS}
<div class="ink" style="position:absolute;inset:0">{inner}</div>{OVERLAYS}</div>"""


def perfil_jobs():
    av = lambda px: sheet(px, px, PAPEL["amarelo"], f"""<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{px*.012:.0f}px">
<span class="as ln fill" data-w="{px*.76:.0f}" data-max="999" style="color:{VERMELHO};text-shadow:{px*.008:.1f}px {px*.008:.1f}px 0 {AZUL}">Nação</span>
<span class="an ln fill" data-w="{px*.76:.0f}" data-max="999">Sixers</span></div>""")
    capa = sheet(1500, 500, PAPEL["azul"], f"""
<div style="position:absolute;right:80px;top:40px;width:1000px;display:flex;flex-direction:column;align-items:flex-end">
<span class="as ln fill" data-w="1000" data-max="190" style="color:#FFD71F;text-shadow:7px 7px 0 {VERMELHO}">O 76ers</span>
<span class="an ln fill" data-w="1000" data-max="170" style="color:{CREME};margin-top:24px">em português</span>
<div class="up" style="width:1000px;margin-top:16px;border-top:6px solid {CREME};padding-top:14px;display:flex;justify-content:space-between;font-weight:800;font-size:22px;letter-spacing:.08em;color:{CREME}">
<span>Dia de jogo</span><span style="color:#FFD71F">·</span><span>Placar</span><span style="color:#FFD71F">·</span><span>Notícia com fonte</span><span style="color:#FFD71F">·</span><span style="color:#FFD71F">Horário de Brasília</span></div></div>""", ink=CREME)
    dest = []
    for i, (w, font, cor) in enumerate([("Jogos", "as", VERMELHO), ("Placar", "an", AZUL), ("Notícias", "an", AZUL), ("Agenda", "as", VERMELHO)], 6):
        sh = f"text-shadow:12px 12px 0 {AZUL};" if cor == VERMELHO else ""
        dest.append((f"{i:02d}-Destaque-{w.replace('í', 'i')}.png", sheet(1080, 1920, PAPEL["amarelo"], f"""<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">
<span class="{font} ln fill" data-w="860" data-max="999" style="color:{cor};{sh}">{w}</span></div>""")))
    return [("01-X-foto-de-perfil.png", av(400), 2), ("02-X-capa.png", capa, 1), ("03-Instagram-foto-de-perfil.png", av(1080), 1)] + [(n, m, 1) for n, m in dest]


FIT_JS = """() => {
  const m = document.getElementById('m');
  const fills = [...document.querySelectorAll('.fill')], fxs = [...document.querySelectorAll('.fx')], grows = [...document.querySelectorAll('.grow')];
  fxs.forEach(e => e.dataset.base = parseFloat(getComputedStyle(e).fontSize));
  function over() {
    if (!m) return false;
    const r = m.getBoundingClientRect(); let t = 1e9, b = -1e9, l = 1e9, rr = -1e9;
    m.querySelectorAll('*').forEach(c => { const q = c.getBoundingClientRect(); if (!q.width || !q.height) return;
      t = Math.min(t, q.top); b = Math.max(b, q.bottom); l = Math.min(l, q.left); rr = Math.max(rr, q.right); });
    return t < r.top - 1 || b > r.bottom + 1 || rr > r.right + 3 || l < r.left - 3;
  }
  function apply(s) {
    fills.forEach(el => {
      const W = +(el.dataset.w || el.parentElement.clientWidth), max = +(el.dataset.max || 400) * s;
      el.style.fontSize = '100px';
      const w = el.getBoundingClientRect().width;
      el.style.fontSize = Math.min(max, 100 * W / w) + 'px';
    });
    fxs.forEach(e => e.style.fontSize = (e.dataset.base * s) + 'px');
    grows.forEach(el => {
      let fs = +(el.dataset.max || 160) * s; const H = +(el.dataset.h || 500) * s;
      el.style.fontSize = fs + 'px';
      while ((el.offsetHeight > H || el.scrollWidth > el.clientWidth + 1 || over()) && fs > 24) { fs *= 0.97; el.style.fontSize = fs + 'px'; }
    });
  }
  let s = 1, n = 0; apply(s);
  while (over() && n < 30) { s *= 0.96; apply(s); n++; }
  return over() ? 'overflow' : 'ok';
}"""


def render_many(jobs):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for out, markup, scale in jobs:
            pg = b.new_page(viewport={"width": 1600, "height": 2000}, device_scale_factor=scale)
            pg.set_content(f"<html><head><meta charset='utf-8'><style>{css()}</style></head><body>{markup}</body></html>")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(200)
            if pg.evaluate(FIT_JS) == "overflow":
                b.close()
                sys.exit(f"{out}: o texto não coube mesmo com a letra menor. Encurte o texto e gere de novo.")
            pg.locator("#a").screenshot(path=str(out))
            pg.close()
            print(out)
        b.close()


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    def add(name, req=(), opt=(), lists=()):
        p = sp.add_parser(name)
        for k in req: p.add_argument("--" + k, required=True)
        for k, d in opt: p.add_argument("--" + k, default=d)
        for k in lists: p.add_argument("--" + k, action="append", required=True)
        return p
    add("prejogo", ("mandante", "visitante", "data", "horario", "onde", "out"), (("liga", "NBA"), ("contexto", "Temporada regular"), ("quando", "Hoje tem")))
    add("placar", ("mandante", "visitante", "pm", "pv", "out"), (("liga", "NBA"), ("contexto", ""), ("frase", ""), ("data", "")))
    add("direto", ("citacao", "autor", "out"), (("contexto", ""), ("fonte", ""), ("data", ""), ("tag", "")))
    add("manchete", ("selo", "titulo", "out"), (("texto", ""), ("fonte", ""), ("data", ""), ("tag", "")))
    add("lista", ("chip", "titulo", "out"), (("fonte", ""), ("data", ""), ("tag", "")), ("item",))
    add("agenda", ("periodo", "out"), (), ("jogo",))
    add("numero", ("numero", "rotulo", "out"), (("chip", "Número do dia"), ("texto", ""), ("fonte", ""), ("data", ""), ("papel", "branco"), ("kicker", "")))
    add("cartaz", ("out",), (("papel", "amarelo"), ("texto", ""), ("kicker", "76ers em português"), ("rodape", "Perfil de fã · não oficial")), ("linha",))
    pp = sp.add_parser("perfil"); pp.add_argument("--pasta", default="img")
    a = ap.parse_args()
    for v in vars(a).values():
        for s in (v if isinstance(v, list) else [v]):
            if isinstance(s, str) and ("—" in s or " – " in s):
                sys.exit("Texto com travessão. Troque por vírgula, dois-pontos ou ponto.")
    ensure_fonts()
    if a.cmd == "perfil":
        pasta = pathlib.Path(a.pasta); pasta.mkdir(parents=True, exist_ok=True)
        render_many([(pasta / n, m, s) for n, m, s in perfil_jobs()])
        return
    fn = {"prejogo": prejogo, "placar": placar, "direto": direto, "manchete": manchete, "lista": lista, "agenda": agenda, "cartaz": cartaz, "numero": numero}[a.cmd]
    render_many([(a.out, fn(a), 1)])


if __name__ == "__main__":
    main()
