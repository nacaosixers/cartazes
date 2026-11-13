"""Nação Sixers · trilha original para os reels (batida leve, gerada do zero, sem direito autoral).

Uso: python trilha.py duracao_em_segundos saida.wav [semente]
A semente escolhe andamento e harmonia, para os reels não soarem todos iguais.
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


def trilha(dur, seed=0):
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
    buf = buf[: int(dur * SR)]
    buf = np.tanh(buf * 1.1)
    fade_in, fade_out = int(0.4 * SR), int(1.2 * SR)
    buf[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    buf[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    rms = np.sqrt(np.mean(buf ** 2)) or 1
    buf *= min(0.89 / np.max(np.abs(buf)), 0.10 / rms)  # fundo: cerca de -20 dBFS de média
    return buf


def salvar(buf, path):
    pcm = (np.clip(buf, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    dur = float(sys.argv[1]); out = sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    salvar(trilha(dur, seed), out)
    print(out)
