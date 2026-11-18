# Comentários ao vivo no X

Nasceu em 18/11: o Rodrigo ia estar num voo na hora de Magic x 76ers e pediu um motor de comentários durante o jogo, só no X. Roda quando ele pedir.

## Como roda

Quem roda é o Claude na conversa, acordado por mensagens agendadas (`send_later`) nos momentos do jogo. Rodada automática nova (`create_trigger`) não serve aqui: pode travar em PENDING e pedir aprovação que ninguém responde.

Despertadores, contando do horário marcado do jogo (21h00 vira 21h12, 21h45...):

| Momento | Quando |
|---|---|
| Bola ao alto | início + 12 min |
| Fim do 1º quarto | início + 45 min |
| Intervalo | início + 1h17 |
| Fim do 3º quarto | início + 1h58 |
| Reta final | início + 2h17 |
| Fim de jogo | início + 2h32 |
| Rede de segurança do fim | início + 3h05 |

Em cada despertador:

1. Se `/home/claude/cartazes` não existe (o computador da sessão foi trocado), chame `add_repo` (nacaosixers/cartazes, push) e clone de novo.
2. `fetch_sports_data`: `scores` (nba, time 76ers) e `game_stats` com o id do jogo.
3. **O momento chegou?** Se ainda não: marque outro despertador para daqui a 4 a 6 minutos (no máximo 4 vezes para o mesmo momento) e termine. Se já passou faz tempo (ex.: o 2º quarto já está na metade), não poste o comentário atrasado: espere o próximo momento.
4. **Já saiu?** Confira no X (`list_posts`, últimas 3 horas). Esse momento já tem post: termine.
5. **Escreva e publique:** Buffer `create_post` no X (canal 6af3664262b70b94b0e6d5e9), `mode` shareNow, `schedulingType` automatic, só texto. Deu erro: tente uma vez de novo; falhou de novo, pule esse momento.

## O texto

- Até 240 caracteres (conte com python; emoji conta 2).
- Primeira linha: o momento e o placar, mandante primeiro ("Fim do 1º quarto em Orlando: Magic 24 x 30 76ers."). Diga sempre o momento real do placar que está dando.
- Depois, um destaque tirado do box score: cestinha do 76ers com os números, a parcial do quarto, aproveitamento de três, rebotes, erros, o duelo com o destaque do adversário.
- Tom de torcedor: vibra quando vai bem, admite quando vai mal. Sem xingar ninguém, nem juiz, nem adversário.
- Cada comentário com abertura e destaque diferentes do anterior. Se o mesmo jogador está dominando, diga isso de outro jeito.
- No máximo 1 emoji. Sem hashtag, sem link, sem travessão.
- Pergunta curta para a torcida responder em alguns comentários, não em todos.
- Nunca invente: só número que veio da ferramenta. Lesão durante o jogo não entra (ninguém confirmou). Dado que parece velho ou não bate (placar parado, quarto errado): não poste.

## Os momentos

- **Bola ao alto:** o quinteto do 76ers, se o `game_stats` trouxer os titulares; senão, uma linha com o que está em jogo (campanha, desfalque já noticiado no dia). Se o jogo começou há mais de 6 minutos, já dê o primeiro placar ("Começou em Orlando: ...").
- **Fim do 1º quarto:** placar e o destaque do quarto.
- **Intervalo:** placar, cestinha de cada time e o que decidiu o 1º tempo.
- **Fim do 3º quarto:** placar e o que o 3º quarto mudou (parcial do quarto, se o placar por quarto vier).
- **Reta final** (4º quarto entre 6 e 2min30 para o fim): diferença de até 5 pontos é jogo de clutch; a campanha no clutch (registro `fios`) entra como apoio. Jogo resolvido: um comentário curto e honesto. Faltando menos de 2min30, pule e espere o fim.
- **Prorrogação:** um comentário no fim do tempo normal e o fim de jogo depois.
- **Fim de jogo** (status complete ou closed): é o pós-jogo, feito na hora por esta rodada. Antes de começar, grave `rodadas.posjogo` = "AAAA-MM-DD HH:MM em andamento (Claude na conversa)" e faça push, para a rodada da 0h51 não repetir. No X, o placar sai com o cartaz, num post só. Instagram, story e TikTok seguem `posjogo.md` e o limite de feed do dia (feed cheio: o post do feed vai para 0h01, e o story sai na hora). No fim, registre em `rodadas.aovivo` o que saiu.

## Limite

No máximo 7 comentários por jogo, fora o placar final. Eles não contam no limite de posts do X do dia.
