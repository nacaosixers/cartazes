#!/usr/bin/env python3
"""Relógio do ao vivo: diz se o momento do comentário chegou e quando conferir de novo.

Uso (com o que o fetch_sports_data devolveu):
  python3 kit/relogio.py --momento q1 --status inprogress --quarto 1 --relogio 5:12

Momentos, na ordem: bola, q1, intervalo, q3, reta, fim.
Saída, uma linha:
  agora       poste o comentário desse momento
  esperar N   marque send_later para daqui a N minutos e termine
  passou      o momento já passou: não poste, siga para o próximo

Fatores (minutos reais por minuto de jogo) medidos em Magic x 76ers, 18/11:
1º quarto 2,2; 2º 2,8; 3º 2,3; 4º 2,6, e os 2 últimos minutos levam uns 9 minutos.
Intervalo de 15 minutos; troca de quarto, 2. Ajuste FATOR se os jogos mostrarem outro ritmo.
"""
import argparse

FATOR = {1: 2.2, 2: 2.8, 3: 2.3, 4: 2.6}
FATOR_PRORROGACAO = 3.0
TROCA = 2          # minutos reais entre o 1º e o 2º quarto, e entre o 3º e o 4º
INTERVALO = 15     # minutos reais de intervalo
FIM_LENTO = 9      # minutos reais dos 2 últimos minutos do jogo
FOLGA = 1.5        # chegar um pouco antes do momento
MIN_ESPERA = 2


def minutos(relogio):
    m, _, s = relogio.partition(":")
    return int(m) + (int(s) if s else 0) / 60


def ate_fim_do_quarto(q, c):
    """Minutos reais até o fim do quarto q, com c minutos no relógio."""
    return c * FATOR.get(q, FATOR_PRORROGACAO)


def quarto_inteiro(q):
    return 12 * FATOR[q]


def esperar(n):
    return f"esperar {max(MIN_ESPERA, round(n - FOLGA))}"


def decide(momento, status, q, c):
    if status in ("scheduled", "created"):
        return "esperar 3" if momento == "bola" else "esperar 10"
    if status in ("postponed", "cancelled"):
        return "passou"
    if status in ("complete", "closed"):
        return "agora" if momento == "fim" else "passou"
    if status == "halftime":
        if momento == "intervalo":
            return "agora"
        if momento in ("bola", "q1"):
            return "passou"
        if momento == "q3":
            return "esperar 25"  # não se sabe quanto do intervalo já passou: reconfira com o relógio do 3º quarto
        return "esperar 40"

    # jogo rolando
    if momento == "bola":
        return "agora" if q == 1 else "passou"

    if momento == "q1":
        if q == 1:
            return "agora" if c == 0 else esperar(ate_fim_do_quarto(1, c))
        if q == 2 and c >= 10:
            return "agora"  # placar do fim do 1º pelo placar por quarto
        return "passou"

    if momento == "intervalo":
        if q == 1:
            return esperar(ate_fim_do_quarto(1, c) + TROCA + quarto_inteiro(2))
        if q == 2:
            return "agora" if c == 0 else esperar(ate_fim_do_quarto(2, c))
        return "passou"

    if momento == "q3":
        if q == 2:
            return esperar(ate_fim_do_quarto(2, c) + INTERVALO + quarto_inteiro(3))
        if q == 3:
            return "agora" if c == 0 else esperar(ate_fim_do_quarto(3, c))
        if q == 4 and c >= 10:
            return "agora"  # placar do fim do 3º pelo placar por quarto
        return "passou"

    if momento == "reta":  # 4º quarto entre 6min30 e 2min30 para o fim
        if q == 3:
            return esperar(ate_fim_do_quarto(3, c) + TROCA + (12 - 6) * FATOR[4])
        if q == 4:
            if c > 6.5:
                return esperar((c - 6) * FATOR[4])
            return "agora" if c >= 2.5 else "passou"
        return "passou"

    if momento == "fim":
        if q <= 3:
            return esperar(ate_fim_do_quarto(q, c) + 20)
        if q == 4:
            if c > 2:
                return esperar((c - 2) * FATOR[4] + FIM_LENTO)
            return "esperar 3"
        return esperar(max(3, c * FATOR_PRORROGACAO))  # prorrogação

    raise SystemExit(f"momento desconhecido: {momento}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--momento", required=True, choices=["bola", "q1", "intervalo", "q3", "reta", "fim"])
    ap.add_argument("--status", required=True)
    ap.add_argument("--quarto", type=int, default=0)
    ap.add_argument("--relogio", default="12:00")
    a = ap.parse_args()
    print(decide(a.momento, a.status, a.quarto, minutos(a.relogio)))


if __name__ == "__main__":
    main()
