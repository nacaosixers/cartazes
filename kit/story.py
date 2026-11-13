"""Nação Sixers · transforma um cartaz 1080x1350 em story 1080x1920 (para Instagram Stories e TikTok em modo foto).

Uso: python story.py cartaz.png story.png
O cartaz fica no centro, com faixas da mesma cor do papel em cima e embaixo, onde o Instagram põe a barra e a resposta.
"""
import sys
from PIL import Image

img = Image.open(sys.argv[1]).convert("RGB")
cor = img.getpixel((20, 20))
fundo = Image.new("RGB", (1080, 1920), cor)
fundo.paste(img.resize((1080, 1350)), (0, 285))
fundo.save(sys.argv[2])
print(sys.argv[2])
