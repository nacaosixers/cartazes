# Pautas: o que postar e como nunca repetir

Leia na rodada da manhã e no radar, antes de criar qualquer mídia. Nasceu da crítica do Rodrigo em 15/11: no dia do Pacers, três posts seguidos diziam "Hoje tem 76ers contra o Pacers".

## A regra de ouro

Cada post traz algo novo para quem já viu os anteriores: um fato, um número, uma história, uma leitura da Filadélfia ou uma opinião que ainda não apareceu naquele canal. Post que só repete o anterior em outro formato não sai.

## Plano do dia (rodada da manhã, antes de gerar mídia)

Escreva em `estado/registro.json`, chave `plano`, uma linha por post: `{"canal", "hora", "formato", "gancho", "fato"}`. O gancho é a primeira linha do texto e a primeira cena ou o título do cartaz. Antes de gerar, confira:

1. **Gancho:** nenhum gancho igual ou parecido no mesmo canal em 48 horas (compare com `list_posts` dos últimos 2 dias). "Hoje tem 76ers" aparece uma vez por canal no dia do jogo, só no pré-jogo.
2. **Fato:** o fato principal não pode ter sido o fato principal de outro post no mesmo canal nos últimos 7 dias (registro `fatos`: `{"fato", "canal", "data"}`). Pode voltar como detalhe de apoio.
3. **Formato:** pelo menos 3 formatos diferentes no dia; no máximo 2 do mesmo formato por canal em 3 dias.
4. **Mistura:** todo dia, pelo menos um post de história ou curiosidade e um de "Na Filadélfia" ou de tática.
5. **Visual:** posts seguidos no mesmo canal com papel ou modelo diferentes.

## Cardápio

**Dia de jogo** (escolha 4 a 6, cada um com gancho próprio):
- **Pré-jogo** (`prejogo`): horário, onde assistir e desfalques. Um por canal. É o único que abre com "Hoje tem".
- **História do confronto** (reel ou carrossel): séries de playoff, jogos marcantes, a última vez que algo aconteceu, retrospecto histórico. Duas fontes.
- **O confronto em números** (`comparativo`): campanha, pontos marcados e sofridos, três pontos, rebotes, retrospecto recente. Barras com dados reais.
- **O duelo da noite** (`comparativo` ou reel): o destaque do 76ers contra o do adversário, com as médias.
- **Na Filadélfia** (`manchete` com selo Opinião ou Notícia): o que Inquirer, PhillyVoice, NBC Sports Philadelphia, Crossing Broad, Liberty Ballers e as rádios estão discutindo hoje, com o nome do jornalista.
- **Reencontro:** ex-jogador que volta à Filadélfia, ou jogador do 76ers contra o ex-time, com números.
- **Palpite da Nação** (X, texto, marcado como OPINIÃO): placar e o porquê em uma frase.
- **O que observar** (`lista`): 3 pontos táticos para o jogo.

**Depois do jogo:** placar (já automático), Raio-X e, no dia seguinte, a reação da Filadélfia (o que os jornais disseram, com nome).

**Dia sem jogo:** Raio-X (se teve jogo ontem), Número do dia, Neste dia na história, "2001: 25 anos" (quarta), From Brazil (sexta), Na Filadélfia (treino, frase do técnico, debate da semana), Prancheta (tática em 3 pontos), ranking na liga (`comparativo` contra a média da NBA ou contra o rival da semana), Opinião da Nação (X). No TikTok: Adivinha quem é, Você sabia?, Explicando o 76ers, Top 3 histórico, Quem ganha? (duas lendas com números).

## Fios da temporada (números que andam a cada jogo)

Nasceu em 16/11: o próprio 76ers postou "9-0 no clutch, único invicto da NBA, com 50% de quadra e de três nesses momentos". A Nação tinha dado o 8-0 em 14/11, mas deixou passar a atualização e no Raio-X do Pacers tratou o jogo como decidido no terceiro quarto.

- O registro guarda em `fios` os números da temporada que mudam a cada jogo: `{"fio", "valor", "ate", "fonte", "ultimo_post"}`. Exemplos: campanha no clutch (diferença de até 5 pontos nos 5 minutos finais), sequências, marcas de carreira que estão perto (LeBron e as assistências), recordes da temporada, campanha sem Joel Embiid.
- Depois de cada jogo (pós-jogo e Raio-X), atualize os fios no registro.
- **Fio que já teve post só volta quando cresce de verdade:** número redondo (10-0, 15-0, 20-0) ou recorde do time ou da liga. Um a mais (8-0 para 9-0) não vira post nem gancho (regra do Rodrigo, 16/11). Fio que chegou a um marco vira o gancho do pós-jogo ou do Raio-X, ou o Número do dia seguinte.
- Onde achar: nba.com/sixers/news (notas e números do próprio time), NBA.com/stats (página Clutch, quando abrir) e as notas da imprensa local, que repetem esses números. O perfil do 76ers no X (série "76 By The Numbers") é a melhor vitrine, mas não abre sem login: quando o Rodrigo mandar um print, ele entra em `fila_pautas`. Traduza, confira e dê o crédito ("segundo o 76ers", "dados da NBA"). A arte deles nunca: foto, logo e patrocinador ficam de fora; o número vira cartaz do kit.

## Fila de pautas

`fila_pautas` no registro guarda pautas para os próximos dias, inclusive as que o Rodrigo sugerir: `{"pauta", "quando", "fonte", "sugerida_por"}`. A rodada da manhã lê a fila ao fazer o plano: pauta dentro do prazo entra antes das outras e, depois de usada, sai da fila (registre em `fatos`).

## Onde achar história e números do confronto

- Land of Basketball: `landofbasketball.com/head_to_head/76ers_vs_[time]_all_time.htm` (retrospecto e séries de playoff).
- Basketball-Reference: séries de playoff e box scores antigos.
- NBA.com, prévia oficial do jogo (`nba.com/[time]/news/preview-...`): desfalques, sequências, reencontros e curiosidades do dia.
- Imprensa local (fontes.md) para Na Filadélfia.

## Trilha dos vídeos

Estilos do kit: pop, drumline, trap, lofi, house, arena. Use um diferente dos 2 últimos do registro `trilhas` (`{"estilo", "video", "data"}`) e registre. Combina: história e rivalidade com drumline ou arena; números e tática com trap ou house; curiosidade e Explicando com lofi ou pop.

## Imagens

Sem foto de jogador ou de qualquer pessoa, sem imagem de transmissão e sem logo de time: são direitos de imagem e de autor, e as redes derrubam e penalizam contas por isso. O visual real que usamos: os cartazes do kit e gráficos com dados reais (`comparativo`).

## Revisão visual (obrigatória)

Depois de gerar a mídia e antes de agendar, rode `python kit/grade.py grade.png [mídias de hoje] [mídias de ontem do mesmo canal]` e olhe a grade com a ferramenta de leitura. Duas capas que parecem o mesmo post no mesmo canal: troque uma. Texto cortado, faixa ou letra borrada: refaça.
