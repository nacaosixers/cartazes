"""Nação Sixers · reels no estilo cartaz (MP4 1080x1920, 30 fps, com faixa de áudio silenciosa).

Uso: python reel.py roteiro.json saida.mp4

roteiro.json:
{
  "cenas": [
    {"papel": "amarelo", "kicker": "Raio-X",
     "linhas": [["Raio-X", "as", "vermelho", 380], ["76ers 101 x 123 Celtics", "an", "azul", 170]],
     "texto": "3 números que explicam a derrota.", "dur": 2.6},
    {"papel": "branco", "kicker": "1 de 3", "numero": "33",
     "rotulo": "pontos de diferença na bola de três", "texto": "Celtics 22 de 49. 76ers 11 de 37.", "dur": 3.0}
  ],
  "cta": true
}

Cada cena tem "linhas" (lista de [texto, fonte an|as, cor azul|vermelho|creme|amarelo, tamanho máximo])
ou "numero" + "rotulo". "texto" e "kicker" são opcionais. "dur" em segundos (padrão 3).
Número só com dígitos (ex.: "33") sobe contando de 0. "cta": true fecha com "Segue a Nação".
O conteúdo fica dentro da área segura do Reels/TikTok (longe do topo, do rodapé e dos botões da direita).
Nunca use travessão nos textos.
"""
import json, pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cartaz as C  # noqa: E402

W, H, FPS = 1080, 1920, 30
AMARELO = "#FFD71F"
COR = {"azul": C.AZUL, "vermelho": C.VERMELHO, "creme": C.CREME, "amarelo": AMARELO}


def cena_html(k, c):
    papel = c.get("papel", "branco")
    paper = C.PAPEL[papel]
    azul = papel == "azul"
    ink, acc = (C.CREME, AMARELO) if azul else (C.AZUL, C.VERMELHO)
    E = C.E
    body = ""
    if "numero" in c:
        num = str(c["numero"])
        conta = f' data-conta="{num}"' if num.isdigit() else ""
        shadow = "" if azul else f"text-shadow:12px 12px 0 {C.AZUL};"
        body += f'<span class="as ln fill anim"{conta} data-max="620" style="color:{acc};{shadow}margin-bottom:22px">{E(num)}</span>'
        body += f'<div class="an grow anim" data-max="118" data-h="360" style="line-height:1.02">{E(c.get("rotulo", ""))}</div>'
    for ln in c.get("linhas", []):
        txt, font, cor, mx = (list(ln) + ["", "an", "azul", 300])[:4]
        col = COR.get(cor, ink)
        if azul and cor == "azul":
            col = C.CREME
        sh = f"text-shadow:10px 10px 0 {C.AZUL};" if (font == "as" and cor == "vermelho" and not azul) else ""
        body += f'<span class="{font} ln fill anim" data-max="{mx}" style="color:{col};{sh}margin:6px 0">{E(txt)}</span>'
    if c.get("texto"):
        body += f'<div class="fx anim" style="margin-top:40px;font-weight:700;font-size:56px;line-height:1.26;border-left:12px solid {acc};padding-left:28px">{E(c["texto"])}</div>'
    kicker = E(c.get("kicker", "76ers em português"))
    return f"""<div class="cena" id="c{k}" style="background:{paper};color:{ink}">
<div class="zoom">
<div style="position:absolute;left:64px;right:64px;top:150px;display:flex;justify-content:space-between;align-items:center">
<span class="an" style="font-size:56px;line-height:1">Nação <span style="color:{acc}">Sixers</span></span>
<span class="up" style="font-weight:800;font-size:28px;letter-spacing:.1em">{kicker}</span></div>
<div style="position:absolute;left:64px;right:64px;top:232px;height:10px;background:{ink}"></div>
<div class="mbox" id="m{k}" style="position:absolute;left:64px;top:290px;width:952px;height:1120px;display:flex;flex-direction:column;justify-content:center">{body}</div>
<div style="position:absolute;left:64px;right:64px;top:1440px;height:10px;background:{ink}"></div>
<div class="up" style="position:absolute;left:64px;top:1470px;font-weight:800;font-size:30px;letter-spacing:.1em;color:{acc}">@nacaosixers</div>
</div>
<div class="wipe" style="background:{C.VERMELHO if papel != 'amarelo' else C.AZUL}"></div>
</div>"""


JS = """
const scenes = [...document.querySelectorAll('.cena')];
const durs = window.DURS; const starts = []; let acc = 0;
durs.forEach(d => { starts.push(acc); acc += d; });
function fitScene(sc) {
  const m = sc.querySelector('.mbox');
  const fills = [...sc.querySelectorAll('.fill')], fxs = [...sc.querySelectorAll('.fx')], grows = [...sc.querySelectorAll('.grow')];
  fxs.forEach(e => e.dataset.base = parseFloat(getComputedStyle(e).fontSize));
  function over() {
    const r = m.getBoundingClientRect(); let t = 1e9, b = -1e9;
    m.querySelectorAll('*').forEach(c => { const q = c.getBoundingClientRect(); if (!q.width || !q.height) return; t = Math.min(t, q.top); b = Math.max(b, q.bottom); });
    return t < r.top - 1 || b > r.bottom + 1;
  }
  function apply(s) {
    fills.forEach(el => { el.style.fontSize = '100px'; const w = el.getBoundingClientRect().width;
      el.style.fontSize = Math.min(+el.dataset.max * s, 100 * 952 / w) + 'px'; });
    fxs.forEach(e => e.style.fontSize = (e.dataset.base * s) + 'px');
    grows.forEach(el => { let fs = +el.dataset.max * s; el.style.fontSize = fs + 'px';
      while ((el.offsetHeight > +el.dataset.h * s || el.scrollWidth > el.clientWidth + 1) && fs > 24) { fs *= 0.97; el.style.fontSize = fs + 'px'; } });
  }
  let s = 1, n = 0; apply(s);
  while (over() && n < 30) { s *= 0.96; apply(s); n++; }
  return !over();
}
window.fitAll = () => { scenes.forEach(sc => sc.style.visibility = 'visible'); const ok = scenes.map(fitScene).every(Boolean); return ok; };
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
window.setT = (t) => {
  let idx = scenes.length - 1;
  for (let i = 0; i < scenes.length; i++) if (t < starts[i] + durs[i]) { idx = i; break; }
  scenes.forEach((s, i) => s.style.visibility = i === idx ? 'visible' : 'hidden');
  const sc = scenes[idx], lt = t - starts[idx];
  sc.querySelector('.zoom').style.transform = `scale(${1 + 0.025 * Math.min(lt / durs[idx], 1)})`;
  sc.querySelectorAll('.anim').forEach((el, i) => {
    const p = ease((lt - 0.10 - i * 0.16) / 0.30);
    el.style.opacity = p;
    el.style.transform = `translateY(${(1 - p) * 70}px) scale(${1 + (1 - p) * 0.10})`;
    if (el.dataset.conta) { const q = ease((lt - 0.10 - i * 0.16) / 0.85); el.textContent = String(Math.round(+el.dataset.conta * q)); }
  });
  const w = sc.querySelector('.wipe'), rem = starts[idx] + durs[idx] - t;
  w.style.transform = (idx < scenes.length - 1 && rem < 0.24) ? `translateX(${(rem / 0.24) * 100}%)` : 'translateX(100%)';
};
"""


def main():
    roteiro = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = sys.argv[2]
    cenas = list(roteiro["cenas"])
    if roteiro.get("cta", True):
        cenas.append({"papel": "amarelo", "kicker": "Siga", "linhas": [["Segue a", "an", "azul", 240], ["Nação", "as", "vermelho", 400], ["@nacaosixers", "an", "azul", 150]],
                      "texto": "O 76ers em português, todo dia.", "dur": 2.4})
    for c in cenas:
        for v in [c.get("texto", ""), c.get("rotulo", ""), c.get("kicker", "")] + [str(x) for ln in c.get("linhas", []) for x in ln]:
            if "—" in str(v) or " – " in str(v):
                sys.exit("Texto com travessão. Troque por vírgula, dois-pontos ou ponto.")
    durs = [float(c.get("dur", 3)) for c in cenas]
    C.ensure_fonts()
    css = C.css() + """
body{margin:0;background:#000}
#v{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:AR}
.cena{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.zoom{position:absolute;inset:0;transform-origin:50% 45%}
.anim{opacity:0}
.wipe{position:absolute;inset:0;transform:translateX(100%)}
.ov{position:absolute;inset:0;pointer-events:none;will-change:transform}
"""
    html = f"""<html><head><meta charset='utf-8'><style>{css}</style></head><body><div id="v">
{''.join(cena_html(k, c) for k, c in enumerate(cenas))}
<div class="ov">{C.OVERLAYS}</div></div>
<script>window.DURS = {json.dumps(durs)};{JS}</script></body></html>"""
    total = sum(durs)
    n = int(round(total * FPS))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-vcodec", "mjpeg", "-i", "-",
                           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000", "-shortest",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", str(FPS),
                           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(html)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        if not pg.evaluate("window.fitAll()"):
            b.close(); ff.kill()
            sys.exit("Algum texto não coube no reel mesmo com a letra menor. Encurte o texto e gere de novo.")
        el = pg.locator("#v")
        for f in range(n):
            pg.evaluate(f"window.setT({f / FPS:.4f})")
            ff.stdin.write(el.screenshot(type="jpeg", quality=90))
        # capa: último quadro da primeira cena, para conferir
        pg.evaluate(f"window.setT({max(durs[0] - 0.3, 0):.3f})")
        el.screenshot(path=str(pathlib.Path(out).with_suffix(".capa.png")))
        b.close()
    ff.stdin.close(); ff.wait()
    if ff.returncode != 0:
        sys.exit("ffmpeg falhou ao montar o vídeo.")
    print(out, f"{total:.1f}s", f"{n} quadros")


if __name__ == "__main__":
    main()
