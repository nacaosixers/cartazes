"""Nação Sixers · grade de revisão: junta as capas de vários posts numa imagem só, para conferir de uma vez.

Uso: python grade.py grade.png arquivo1.png video.mp4 ...
Vídeo entra pelo quadro de 0,5 s (a capa). Olhe a grade antes de agendar: duas capas parecidas no mesmo canal,
texto cortado, faixa ou letra borrada = refaça.
"""
import pathlib, subprocess, sys, tempfile
from PIL import Image, ImageDraw

LARG, COLS = 270, 5


def miniatura(caminho, tmp):
    p = pathlib.Path(caminho)
    if p.suffix.lower() in (".mp4", ".mov"):
        quadro = pathlib.Path(tmp) / (p.stem + ".png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "0.5", "-i", str(p), "-frames:v", "1", str(quadro)], check=True)
        p = quadro
    im = Image.open(p).convert("RGB")
    return im.resize((LARG, int(im.height * LARG / im.width)))


def main():
    saida, arquivos = sys.argv[1], sys.argv[2:]
    with tempfile.TemporaryDirectory() as tmp:
        mins = [(pathlib.Path(a).name, miniatura(a, tmp)) for a in arquivos]
    alt = max(m.height for _, m in mins) + 28
    linhas = (len(mins) + COLS - 1) // COLS
    grade = Image.new("RGB", (COLS * (LARG + 12) + 12, linhas * (alt + 12) + 12), "white")
    d = ImageDraw.Draw(grade)
    for i, (nome, m) in enumerate(mins):
        x, y = 12 + (i % COLS) * (LARG + 12), 12 + (i // COLS) * (alt + 12)
        grade.paste(m, (x, y))
        d.text((x, y + m.height + 6), nome[:44], fill="black")
    grade.save(saida)
    print(saida, len(mins), "capas")


if __name__ == "__main__":
    main()
