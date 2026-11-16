# Turno do vigia (9h17)

Rodada de conferência, curta. Existe porque em 16/11 as rodadas automáticas das 7h51 e das 10h37 ficaram presas na plataforma, sem começar, e nada saiu até as 11h.

1. **Leia só `estado/registro.json`** (o resto do manual só se precisar trabalhar).
2. **A manhã rodou?** Se `rodadas.manha` tem a data de hoje e diz "feito", termine sem fazer nada e sem mensagem. Se diz "em andamento" há menos de 90 minutos, termine também: a manhã está trabalhando. Se diz "em andamento" há mais de 90 minutos e `list_posts` não mostra nenhum post criado hoje, a manhã travou no meio: siga o passo 3.
3. **Faça o dia:** grave `rodadas.manha` = "AAAA-MM-DD HH:MM em andamento (vigia)", faça commit e push, leia `LEIA-PRIMEIRO.md`, `fontes.md`, `pautas.md` e `manha.md` e faça o turno da manhã inteiro, com estes ajustes:
   - o que já passou do horário vai para o próximo horário livre depois do currentTime + 15 minutos, seguindo a grade do `manha.md` e os 90 minutos entre posts do feed do Instagram;
   - primeiro o que envelhece: placar (se não saiu) e o Raio-X do TikTok (dentro das 18 horas depois do fim do jogo); depois o resto;
   - antes de cada create_post, confira em `list_posts` que o post ainda não existe (outra rodada pode ter acordado).
4. **Feche:** grave `rodadas.manha` = "AAAA-MM-DD HH:MM feito (vigia)" e `rodadas.vigia` = "AAAA-MM-DD HH:MM", escreva na central `motor.texto` = "A rodada das 7h51 não rodou; o vigia fez o dia às HH:MM." e mande ao Rodrigo uma linha com SendUserMessage dizendo isso.
