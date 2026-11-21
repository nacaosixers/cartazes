# Comentários ao vivo no X

Nasceu em 18/11: o Rodrigo ia estar num voo na hora de Magic x 76ers e pediu um motor de comentários durante o jogo, só no X. Em 19/11 ele aprovou o resultado e pediu conferência automática do início do jogo e do tempo de cada quarto. Combinado de 20/11 (vale sobre o de 19/11), depois do Raio-X das redes mostrar que o comentário ao vivo é o post que mais aparece no X:

- **Placar logo depois do fim: em todo jogo**, automático.
- **Comentários durante o jogo: em todo jogo**, automático. Nas palavras dele: "melhor garantir seus comentários que atraiam mais pessoas".
- **Os posts do Rodrigo durante o jogo são extras.** Quando ele consegue assistir, posta os dele direto no app. A corrente não para, não responde e não apaga nada por causa deles. Se um post dele (no `list_posts`, os que não saíram pelo Buffer) deu o placar do mesmo momento há menos de 5 minutos, mude o destaque do seu para não repetir a mesma informação.
- **Se ele pedir um jogo sem comentários:** desligue o início e a rede 1 desse jogo (`update_trigger` com `enabled` false, ids na agenda), marque `comentarios` false e responda numa linha. A rede 2 cuida do placar.

## Como roda

Quem roda é o Claude na conversa, acordado por mensagens agendadas (`send_later`). Rodada automática nova (`create_trigger`) não serve aqui: pode travar em PENDING e pedir aprovação que ninguém responde.

Por jogo, só 4 despertadores fixos, contando do horário marcado:

| Despertador | Quando | O que faz |
|---|---|---|
| Início | início + 8 min | confere se a bola subiu, posta a bola ao alto e começa a corrente |
| Rede 1 | início + 1h25 | se a corrente parou, retoma |
| Rede 2 | início + 2h10 | se a corrente parou, retoma; num jogo sem comentários (só a pedido do Rodrigo), começa a corrente do placar, em que o único momento é o fim |
| Rede 3 | início + 2h55 | garante o placar nos três canais |

Num jogo sem comentários, a corrente só tem o momento `fim`: o relógio diz quando o jogo acaba e o placar sai na hora.

O resto é a **corrente**: cada despertador, depois de conferir o jogo, marca o próximo pelo relógio do jogo, com `kit/relogio.py`. Ele diz se o momento chegou ("agora"), quanto esperar ("esperar N") ou se o momento já passou ("passou"). Os fatores de ritmo vêm de 18/11 (bola ao alto às 21h11, fim do 1º às 21h37, intervalo às 22h12, fim do 3º às 22h56, fim às 23h36); refeito sobre aquele jogo, ele acerta cada momento com 1 ou 2 minutos de folga. Se os jogos mostrarem outro ritmo, ajuste `FATOR` no script.

Em cada despertador da corrente:

1. Se `/home/claude/cartazes` não existe (o computador da sessão foi trocado), chame `add_repo` (nacaosixers/cartazes, push) e clone de novo.
2. Leia o log do jogo (`aovivo-AAAA-MM-DD.txt` no scratchpad da conversa): o que já saiu e qual é o próximo momento. Sem log, o X (`list_posts`, últimas 3 horas) diz o que já saiu.
3. **Conferência do relógio:** `fetch_sports_data` `scores` (nba, time 76ers), que é leve e traz status, quarto e relógio do jogo. Se o `scores` ainda disser `created` ou `scheduled` depois do horário de início, confira no `game_stats`: em 21/11 o `scores` ficou em `created` com o jogo no 1º quarto, e o relógio do jogo todo saiu do `game_stats`. Rode `python3 kit/relogio.py --momento [próximo] --status [status] --quarto [q] --relogio [MM:SS]`.
   - "esperar N": `send_later` em N minutos, anote no log e termine.
   - "passou": anote e repita o passo 3 com o momento seguinte.
   - "agora": siga.
   - Relógio parado igual ao da conferência anterior (pausa, revisão, dado atrasado): `send_later` em 3 minutos.
4. **Já saiu?** O log ou o X (`list_posts`) mostram esse momento: pule para o seguinte.
5. **Escreva e publique:** só agora busque o `game_stats` (pesado) e escreva. Buffer `create_post` no X (canal 6af3664262b70b94b0e6d5e9), `mode` shareNow, `schedulingType` automatic, só texto. Deu erro: tente uma vez de novo; falhou de novo, pule esse momento.
6. **Marque o próximo:** rode o relógio para o momento seguinte, `send_later` no tempo que ele der e anote no log a hora, o momento e o post.

Redes: se o log mostra uma conferência nos últimos 20 minutos, a corrente está viva: termine. Se não, retome pelo passo 3 com o primeiro momento que ainda não saiu; sem comentários nesse jogo (`comentarios` false na agenda), esse momento é sempre o `fim`.

## Agenda

- `aovivo_agenda` no registro lista os jogos com despertadores marcados: `{"jogo", "data", "inicio", "game_id", "comentarios", "ids"}`, com os ids do início e das 3 redes. A rodada da manhã confere: dia de jogo sem o jogo na agenda, avise o Rodrigo (os despertadores só podem ser marcados pela conversa).
- A cada 2 semanas, um despertador de renovação marca os jogos seguintes (início e 3 redes de cada um, todos ligados, com `comentarios` true na agenda), atualiza a agenda e marca a próxima renovação. Não desligue nada: desde 20/11 os comentários saem em todo jogo. A plataforma aceita uns 10 despertadores por minuto: marque em lotes.
- O texto de um despertador não pode ser trocado sem aprovação no computador do Rodrigo; para ligar ou desligar, mexa só no `enabled`.

## O texto

- Até 240 caracteres (conte com python; emoji conta 2).
- Primeira linha: o momento e o placar, mandante primeiro ("Fim do 1º quarto em Orlando: Magic 24 x 30 76ers."). Diga sempre o momento real do placar que está dando.
- Depois, um destaque tirado do box score: cestinha do 76ers com os números, a parcial do quarto, aproveitamento de três, rebotes, erros, o duelo com o destaque do adversário.
- Tom de torcedor: vibra quando vai bem, admite quando vai mal. Sem xingar ninguém, nem juiz, nem adversário.
- Cada comentário com abertura e destaque diferentes do anterior. Se o mesmo jogador está dominando, diga isso de outro jeito.
- No máximo 1 emoji. Sem hashtag, sem link, sem travessão.
- Pergunta curta para a torcida responder em alguns comentários, não em todos.
- A lista de jogadores do `game_stats` pode vir cortada (em 18/11 vinham só 5 por time, sem Maxey). Só chame alguém de cestinha se a soma dos pontos dos listados bater com o total do time, ou se os pontos dele forem maiores que os que faltam na lista (total do time menos a soma dos listados): aí ninguém de fora passa dele. Senão, cite o número do jogador sem dizer que é o maior.
- Nunca invente: só número que veio da ferramenta. Lesão durante o jogo não entra (ninguém confirmou). Dado que parece velho ou não bate (placar parado, quarto errado): não poste.

## Os momentos

- **Bola ao alto:** o quinteto do 76ers, se o `game_stats` trouxer os titulares; senão, uma linha com o que está em jogo (campanha, desfalque já noticiado no dia). Se o jogo começou há mais de 6 minutos, já dê o primeiro placar ("Começou em Orlando: ..."). Não começou 25 minutos depois do horário: anote "atrasado" e confira a cada 5 minutos; adiado: anote e termine (as redes leem o log e não fazem nada).
- **Fim do 1º quarto:** placar e o destaque do quarto.
- **Intervalo:** placar, cestinha de cada time e o que decidiu o 1º tempo.
- **Fim do 3º quarto:** placar e o que o 3º quarto mudou (parcial do quarto, se o placar por quarto vier).
- **Reta final** (4º quarto entre 6 e 2min30 para o fim): diferença de até 5 pontos é jogo de clutch; a campanha no clutch (registro `fios`) entra como apoio. Jogo resolvido: um comentário curto e honesto. Faltando menos de 2min30, pule e espere o fim.
- **Prorrogação:** um comentário no fim do tempo normal e o fim de jogo depois.
- **Segundos finais** (4º quarto com menos de 1 minuto): já faça o cartaz, o story e o vídeo com o placar do momento, sem push, e confira de novo em 1 ou 2 minutos. Se o placar final for o mesmo, é só publicar; se mudar, refaça. Em 21/11 isso pôs o placar no ar 3 minutos depois do fim.
- **Fim de jogo** (status complete ou closed): é o pós-jogo, feito na hora por esta rodada. Antes de começar, grave `rodadas.posjogo` = "AAAA-MM-DD HH:MM em andamento (Claude na conversa)" e faça push, para a rodada da 0h51 não repetir. No X, o placar sai com o cartaz, num post só. Instagram, story e TikTok seguem `posjogo.md` e o limite de feed do dia (feed cheio: o post do feed vai para 0h01, e o story sai na hora). No fim, registre em `rodadas.aovivo` o que saiu.

## Limite

No máximo 7 comentários por jogo, fora o placar final. Eles não contam no limite de posts do X do dia.
