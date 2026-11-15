"""Nação Sixers · trilha original para os reels (batida leve, gerada do zero, sem direito autoral).

Uso: python trilha.py duracao_em_segundos saida.wav [semente] [estilo]
Estilos (cada um com instrumentos, ritmo e andamento próprios): pop, drumline, trap, lofi, house, arena.
Sem estilo, a semente escolhe um. O motor registra o estilo usado e nunca repete os 2 últimos.
Volume pensado para ficar de fundo, sem competir com a leitura.
"""
import sys, wave
import numpy as np
from scipy.signal import lfilter

SR = 48000
PROGRESSOES = [
    ([57, 53, 48, 55], 92),   # Am F C G
    ([50, 46, 53, 48], 88),   # Dm Bb F C
    ([52, 48, 55, 50], 96),   # Em C G D
    ([57, 55, 53, 52], 90),   # Am G F E
]


def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a, d):
    t = np.arange(n) / SR
    e = np.exp(-t * d)
    k = max(1, int(a * SR))
    e[:k] *= np.linspace(0, 1, k)
    return e


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    return lfilter([1 - a], [1, -a], x)


def kick():
    n = int(0.38 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 8.5)


def snare(rng):
    n = int(0.22 * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    body = lowpass(nz, 5200) - lowpass(nz, 900)
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 28)
    return (0.75 * body * np.exp(-t * 18) + 0.35 * tone)


def hat(rng):
    n = int(0.06 * SR)
    nz = rng.standard_normal(n)
    return (nz - lowpass(nz, 7000)) * env(n, 0.001, 70)


def bass(note, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f = hz(note - 12)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    return np.tanh(1.4 * s) * env(n, 0.006, 2.6)


def keys(root, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n)
    terca = 3 if root % 12 in (9, 2, 4) else 4  # menor em Lá, Ré e Mi; maior nos outros
    for k in (0, terca, 7, 12):
        f = hz(root + 12 + k)
        out += np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
    return lowpass(out, 2600) * env(n, 0.012, 1.9) / 4


def add(buf, sig, at, gain, pan=0.0):
    i = int(at * SR)
    if i >= buf.shape[0]:
        return
    j = min(buf.shape[0], i + len(sig))
    s = sig[: j - i] * gain
    buf[i:j, 0] += s * (1 - pan) ** 0.5
    buf[i:j, 1] += s * (1 + pan) ** 0.5


def pop(dur, seed=0):
    rng = np.random.default_rng(seed)
    acordes, bpm = PROGRESSOES[seed % len(PROGRESSOES)]
    passo = 60 / bpm / 4
    n = int((dur + 0.5) * SR)
    buf = np.zeros((n, 2))
    k, s, total = kick(), snare(rng), int(dur / passo) + 1
    for step in range(total):
        t0 = step * passo
        pos = step % 16
        compasso = (step // 16) % 4
        if pos in (0, 10) or (pos == 7 and compasso == 3):
            add(buf, k, t0, 0.95)
        if pos in (4, 12):
            add(buf, s, t0 + 0.004, 0.42)
        if pos % 2 == 0:
            add(buf, hat(rng), t0 + rng.uniform(0, 0.006), 0.10 if pos % 4 else 0.16, pan=0.25)
        if pos in (0, 10):
            add(buf, bass(acordes[compasso], passo * (6 if pos == 0 else 4)), t0, 0.40)
        if pos in (0, 6):
            add(buf, keys(acordes[compasso], passo * 8), t0, 0.22, pan=-0.2)
    return master(buf, dur)


def master(buf, dur):
    buf = buf[: int(dur * SR)]
    buf = np.tanh(buf * 1.1)
    fade_in, fade_out = int(0.4 * SR), int(1.2 * SR)
    buf[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    buf[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    rms = np.sqrt(np.mean(buf ** 2)) or 1
    buf *= min(0.89 / np.max(np.abs(buf)), 0.10 / rms)  # fundo: cerca de -20 dBFS de média
    return buf


# ---------- instrumentos extras ----------
def clap(rng):
    n = int(0.25 * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    band = lowpass(nz, 3200) - lowpass(nz, 900)
    e = np.zeros(n)
    for d in (0.0, 0.011, 0.022):
        k = int(d * SR); e[k:] += np.exp(-(t[: n - k]) * (70 if d < 0.02 else 16))
    return band * e * 0.9


def open_hat(rng):
    n = int(0.32 * SR)
    nz = rng.standard_normal(n)
    return (nz - lowpass(nz, 6500)) * env(n, 0.002, 9)


def crash(rng):
    n = int(1.6 * SR)
    nz = rng.standard_normal(n)
    return (nz - lowpass(nz, 4500)) * env(n, 0.002, 2.4) * 0.6


def sub808(note, dur, glide=0):
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = hz(note - 12)
    f = f0 * (2 ** ((glide * np.exp(-t * 18)) / 12))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return np.tanh(2.2 * s) * env(n, 0.004, 1.6)


def tom(freq):
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = freq * (1 + 0.5 * np.exp(-t * 30))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 9)


def caixa_marcha(rng):
    n = int(0.16 * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    body = (nz - lowpass(nz, 1800)) * np.exp(-t * 26)
    ring = np.sin(2 * np.pi * 330 * t) * np.exp(-t * 40)
    return 0.8 * body + 0.4 * ring


def orgao(note, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 6 * t)
    f = hz(note) * vib
    fase = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(k * fase) / k for k in (1, 2, 3, 4, 6, 8))
    trem = 1 + 0.12 * np.sin(2 * np.pi * 5.5 * t)
    return lowpass(s * trem, 3800) * env(n, 0.01, 1.2) / 3


def pluck(note, dur, brilho=3000):
    n = int(dur * SR); t = np.arange(n) / SR
    f = hz(note)
    saw = 2 * ((f * t) % 1) - 1
    return lowpass(saw, brilho) * env(n, 0.002, 7) * 0.5


def rhodes(notas, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n)
    for m in notas:
        f = hz(m)
        out += np.sin(2 * np.pi * f * t) * np.exp(-t * 1.4) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 6)
    trem = 1 + 0.18 * np.sin(2 * np.pi * 4.5 * t)
    return out * trem * env(n, 0.006, 0.8) / len(notas)


def chiado(dur, rng):
    n = int(dur * SR)
    x = np.zeros(n)
    idx = rng.integers(0, n, size=int(dur * 14))
    x[idx] = rng.uniform(-1, 1, size=len(idx))
    return lowpass(x, 3500) * 0.6 + lowpass(rng.standard_normal(n), 1200) * 0.012


# ---------- estilos ----------
def drumline(dur, seed=0):
    rng = np.random.default_rng(seed)
    bpm = int(rng.integers(108, 122)); passo = 60 / bpm / 4
    raiz = 45 + int(rng.integers(-2, 3))
    buf = np.zeros((int((dur + 0.5) * SR), 2))
    k, cs, total = kick(), caixa_marcha(rng), int(dur / passo) + 1
    acentos = [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]
    for step in range(total):
        t0 = step * passo; pos = step % 16; bar = (step // 16) % 4
        if pos in (0, 8) or (pos == 11 and bar % 2):
            add(buf, k, t0, 0.9)
        if bar == 3 and pos >= 8:
            add(buf, tom([196, 165, 147, 123][(pos - 8) // 2]), t0, 0.55, pan=0.3 - 0.08 * (pos - 8))
        else:
            add(buf, cs, t0 + rng.uniform(0, 0.004), 0.30 if acentos[pos] else 0.12, pan=0.15)
        if pos == 0 and bar == 0:
            add(buf, crash(rng), t0, 0.35, pan=-0.3)
        if pos in (0, 6, 12):
            add(buf, pluck(raiz + [0, 0, 7][(pos // 6)], passo * 3, 900), t0, 0.45)
    return master(buf, dur)


def trap(dur, seed=0):
    rng = np.random.default_rng(seed)
    bpm = int(rng.integers(136, 146)); passo = 60 / bpm / 4
    base = 52 + int(rng.integers(-3, 3))
    prog = [base, base - 4, base - 2, base - 5]
    escala = [0, 3, 5, 7, 10, 12]
    buf = np.zeros((int((dur + 0.5) * SR), 2))
    k, c, total = kick(), clap(rng), int(dur / passo) + 1
    for step in range(total):
        t0 = step * passo; pos = step % 16; bar = (step // 16) % 4
        if pos in (0, 11) or (pos == 3 and bar % 2):
            add(buf, k, t0, 0.8)
        if pos == 8:
            add(buf, c, t0, 0.5)
        if pos in (0, 11):
            add(buf, sub808(prog[bar], passo * (10 if pos == 0 else 5), glide=(5 if pos == 11 else 0)), t0, 0.5)
        if bar % 2 == 1 and pos >= 12:
            for r in range(3):
                add(buf, hat(rng), t0 + r * passo / 3, 0.09, pan=0.3)
        elif pos % 2 == 0:
            add(buf, hat(rng), t0, 0.12, pan=0.3)
        if pos in (0, 3, 6, 10, 13) and rng.random() < 0.8:
            nota = prog[bar] + 12 + escala[int(rng.integers(0, len(escala)))]
            add(buf, pluck(nota, passo * 3, 2400), t0, 0.16, pan=-0.35)
    return master(buf, dur)


def lofi(dur, seed=0):
    rng = np.random.default_rng(seed)
    bpm = int(rng.integers(76, 86)); passo = 60 / bpm / 4
    t_ = int(rng.integers(-2, 3))
    acordes = [[62 + t_, 65 + t_, 69 + t_, 72 + t_], [55 + t_, 59 + t_, 62 + t_, 65 + t_],
               [60 + t_, 64 + t_, 67 + t_, 71 + t_], [57 + t_, 60 + t_, 64 + t_, 67 + t_]]
    buf = np.zeros((int((dur + 0.5) * SR), 2))
    k, s, total = kick(), snare(rng), int(dur / passo) + 1
    for step in range(total):
        t0 = step * passo; pos = step % 16; bar = (step // 16) % 4
        swing = passo * 0.28 if pos % 2 else 0
        if pos in (0, 7, 10):
            add(buf, k, t0, 0.7)
        if pos in (4, 12):
            add(buf, s, t0 + 0.01, 0.26)
        if pos % 2 == 0 or rng.random() < 0.35:
            add(buf, hat(rng), t0 + swing, 0.07, pan=0.2)
        if pos == 0:
            add(buf, rhodes(acordes[bar], passo * 16), t0, 0.5, pan=-0.15)
            add(buf, bass(acordes[bar][0] - 12, passo * 12), t0, 0.32)
    buf[:, 0] += chiado(dur + 0.5, rng)[: buf.shape[0]]
    buf[:, 1] += chiado(dur + 0.5, rng)[: buf.shape[0]]
    buf[:, 0] = lowpass(buf[:, 0], 5000); buf[:, 1] = lowpass(buf[:, 1], 5000)
    return master(buf, dur)


def house(dur, seed=0):
    rng = np.random.default_rng(seed)
    bpm = int(rng.integers(120, 126)); passo = 60 / bpm / 4
    t_ = int(rng.integers(-2, 3))
    prog = [57 + t_, 53 + t_, 60 + t_, 55 + t_]
    buf = np.zeros((int((dur + 0.5) * SR), 2))
    k, c, total = kick(), clap(rng), int(dur / passo) + 1
    for step in range(total):
        t0 = step * passo; pos = step % 16; bar = (step // 16) % 4
        if pos % 4 == 0:
            add(buf, k, t0, 0.85)
        if pos in (4, 12):
            add(buf, c, t0, 0.38)
        if pos in (2, 6, 10, 14):
            add(buf, open_hat(rng), t0, 0.10, pan=0.25)
        elif pos % 2:
            add(buf, hat(rng), t0, 0.05, pan=-0.25)
        if pos in (2, 6, 10, 14):
            add(buf, bass(prog[bar], passo * 1.6), t0, 0.36)
        if pos in (3, 6, 11):
            r = prog[bar] + 12
            for m in (r, r + (3 if bar % 2 == 0 else 4), r + 7):
                add(buf, pluck(m, passo * 2, 3200), t0, 0.08, pan=0.1)
    return master(buf, dur)


def arena(dur, seed=0):
    rng = np.random.default_rng(seed)
    bpm = int(rng.integers(96, 106)); passo = 60 / bpm / 4
    raiz = 57 + int(rng.integers(-2, 3))
    riff = [0, 3, 5, 7, 10, 7, 5, 3]
    buf = np.zeros((int((dur + 0.5) * SR), 2))
    k, c, total = kick(), clap(rng), int(dur / passo) + 1
    for step in range(total):
        t0 = step * passo; pos = step % 16; bar = (step // 16) % 4
        if pos in (0, 6, 8):
            add(buf, k, t0, 0.9); add(buf, tom(90), t0, 0.4)
        if pos in (4, 12):
            for d in (0, 0.017, 0.031):
                add(buf, c, t0 + d, 0.22, pan=float(rng.uniform(-0.5, 0.5)))
        if pos % 2 == 0 and bar >= 2:
            add(buf, hat(rng), t0, 0.08, pan=0.3)
        if pos % 2 == 0 and bar % 2 == 0:
            add(buf, orgao(raiz + riff[pos // 2], passo * 2), t0, 0.22, pan=-0.2)
        if pos == 0 and bar % 2 == 1:
            for m in (raiz - 12, raiz - 5, raiz):
                add(buf, orgao(m, passo * 14), t0, 0.12)
    eco = np.zeros_like(buf); d = int(0.09 * SR)
    eco[d:] = buf[:-d] * 0.25
    return master(buf + eco, dur)


ESTILOS = {"pop": pop, "drumline": drumline, "trap": trap, "lofi": lofi, "house": house, "arena": arena}


def trilha(dur, seed=0, estilo=None):
    nome = estilo if estilo in ESTILOS else list(ESTILOS)[seed % len(ESTILOS)]
    return ESTILOS[nome](dur, seed)


def salvar(buf, path):
    pcm = (np.clip(buf, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    dur = float(sys.argv[1]); out = sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    estilo = sys.argv[4] if len(sys.argv) > 4 else None
    salvar(trilha(dur, seed, estilo), out)
    print(out)
