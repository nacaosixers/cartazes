# Turno do pós-jogo (0h51)

A rodada mais curta. Leia antes `LEIA-PRIMEIRO.md`.

1. `fetch_sports_data` (scores, team "Philadelphia 76ers"). Se o 76ers não teve jogo encerrado nas últimas 4 horas, **termine imediatamente**, sem mexer em nada e sem mensagem.
2. Confira em `estado/registro.json` e em `list_posts` se o placar desse jogo já saiu. Se já saiu, termine.
3. `game_stats` do jogo. Faça o cartaz `placar` com a frase do que decidiu (números reais), texto do X (curto, com o placar na primeira linha) e legenda do Instagram.
4. Suba a imagem no repositório e agende para 10 minutos depois do currentTime, no X e no Instagram.
5. Registre o placar no `estado/registro.json` (assim a manhã não repete) e faça push. Não atualize a central nem mande mensagem: o turno da manhã cuida disso.
