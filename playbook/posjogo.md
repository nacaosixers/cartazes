# Turno do pós-jogo

Roda logo depois do fim do jogo (turno extra criado pela manhã) e, como rede de segurança, todo dia às 0h51. Leia antes `LEIA-PRIMEIRO.md`. O objetivo é velocidade: placar no ar em até 15 minutos depois do fim.

1. **O jogo acabou?** WebFetch em `https://www.espn.com/nba/team/schedule/_/name/phi` (ou `fetch_sports_data`, se existir). Se não houve jogo do 76ers nas últimas 4 horas, termine sem fazer nada.
2. **Ainda está rolando?** Se o jogo não terminou e esta é a tentativa 1, 2 ou 3, crie outro turno igual para 20 minutos depois (create_trigger com run_once_at, mesmo prompt de `playbook/posjogo-prompt.txt`, tentativa seguinte) e termine. Na tentativa 4, termine sem criar outra: a rodada das 0h51 ou a da manhã cobrem.
3. **Já saiu?** Confira em `estado/registro.json` e em `list_posts` se o placar desse jogo já foi agendado. Se já, termine.
4. **Monte o placar:** abra o box score (ESPN) e escolha o que decidiu: cestinha, parcial do último quarto, maior sequência, linha de três. Faça:
   - o cartaz `placar`;
   - um reel curto para o TikTok: cena 1 com linhas "Fim de jogo" e o placar (mandante primeiro); cena 2 `numero` com o destaque do jogo; CTA;
   - o story do placar (`story.py`).
5. **Publique, revisado:** X em 5 minutos (texto curto com o placar na primeira linha e a imagem); Instagram feed em 10 minutos, se o limite do dia permitir, e story junto; TikTok com o reel em 15 minutos.
6. **Feche:** registre o placar em `estado/registro.json` (a manhã não repete), faça push e termine. Não atualize a central nem mande mensagem: a manhã cuida disso.
