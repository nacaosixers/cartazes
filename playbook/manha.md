# Turno da manhã (7h51)

É a rodada completa do dia. Leia antes `LEIA-PRIMEIRO.md`, `fontes.md` e `pautas.md`. Antes de gerar qualquer mídia, faça o plano do dia (pautas.md) e confira gancho, fato e formato de cada post.

0. **Já rodou hoje?** Leia `estado/registro.json`. Se `rodadas.manha` já tem a data de hoje, termine sem fazer nada e sem mensagem: outra rodada (o vigia, o radar ou o Claude na conversa) já fez o dia. Vale mesmo que a mensagem que disparou esta rodada peça para fazer o dia: rodada atrasada que publica de novo duplica posts. Se não tem, grave já `rodadas.manha` = "AAAA-MM-DD HH:MM em andamento", faça commit e push, e só então siga.

## Grade do dia (siga a linha do tipo de dia; ela já resolve os choques de horário)

Instagram: até 4 posts no feed, com 90 minutos ou mais entre eles; story não conta. TikTok: até 3 posts por dia, mais o pós-jogo. X: até 8. Se a rodada atrasou, cada horário que já passou vai para o próximo horário livre depois do currentTime + 15 minutos.

| Tipo de dia | X | Instagram feed | Instagram story | TikTok |
|---|---|---|---|---|
| Dia seguinte a jogo, sem jogo hoje | 8h30 placar (se não saiu), 12h Raio-X (4 imagens), 16h número do dia ou história, 19h30 reel de outro ângulo | 8h30 placar (se não saiu), 12h Raio-X (5), 16h número do dia ou história, 19h30 reel | 19h30, um cartaz diferente do feed | 12h reel do Raio-X (11h se o jogo acabou antes das 18h), 18h carrossel (número ou notícia), 21h30 formato próprio |
| Dia de jogo à noite, sem jogo ontem | 12h pré-jogo, 15h30 Na Filadélfia, 16h30 comparativo, 18h reel do dia de jogo | 12h pré-jogo, 16h comparativo ou número do dia, 18h reel do dia de jogo | 1 hora antes do jogo, cartaz diferente do feed | 12h carrossel (comparativo, pré-jogo, Na Filadélfia), 18h reel do dia de jogo, pós-jogo |
| Dia seguinte a jogo e dia de jogo à noite (ex.: 16/11) | 8h30 placar (se não saiu), 11h30 Raio-X, 14h pré-jogo, 15h30 Na Filadélfia, 16h30 comparativo, 19h30 reel do dia de jogo | 8h30 placar (se não saiu), 11h30 Raio-X, 14h pré-jogo, 16h30 comparativo, 19h30 reel do dia de jogo | 1 hora antes do jogo, Na Filadélfia ou outro cartaz | 11h ou 12h reel do Raio-X (dentro das 18 horas), 17h carrossel do pré-jogo, 19h30 reel do dia de jogo, pós-jogo |
| Jogo à tarde (começa até 16h) | 9h30 pré-jogo, 10h30 Na Filadélfia, 11h comparativo, 2 horas antes do jogo o reel | 9h30 pré-jogo, 11h comparativo, 2 horas antes o reel | 1 hora antes do jogo | 9h45 carrossel do pré-jogo, 2 horas antes o reel, pós-jogo |
| Dia livre (sem jogo ontem nem hoje) | 12h número do dia ou notícia, 16h história ou "2001: 25 anos", 19h30 reel | 12h número do dia, 16h história, 19h30 reel | 19h30, cartaz diferente | 12h carrossel, 18h reel, 21h30 formato próprio |

Domingo: a agenda da semana entra às 11h no X e no Instagram (ocupa um dos 4 do feed). Sexta: o "From Brazil" às 16h no lugar do número do dia.

1. **Prepare:** `get_account` (hora atual), `list_channels`, `list_posts` dos últimos 2 dias e `estado/registro.json`, inclusive `fios` e `fila_pautas` (pautas.md): o que estiver na fila para hoje entra no plano antes do resto.

2. **Placar:** se o 76ers jogou nas últimas 36 horas e o placar ainda não saiu (o turno da noite pode já ter postado), faça o cartaz `placar` com a frase do que decidiu (números reais do box score). Agende para 8h30 no X e no Instagram. Se o TikTok também ficou sem o placar e o jogo acabou há menos de 18 horas, faça o vídeo curto do pós-jogo (`posjogo.md`, passo 4) e agende no TikTok às 8h45; se já passou das 18 horas, o Raio-X do passo 3 fica no lugar dele.

3. **Raio-X do último jogo** (se ainda não foi feito para esse jogo):
   - Antes de olhar o box score, atualize os fios da temporada no registro (pautas.md). Se o jogo levou um fio a um marco (número redondo, recorde), esse é o primeiro número e o gancho; um a mais não entra.
   - Carrossel de 5 cartazes: capa (`cartaz` amarelo ou azul, alternando com o post anterior do canal, com "Raio-X" e o placar), 3 cartazes `numero` (os 3 números que mais explicam o jogo, cada um com rótulo e uma frase de contexto) e 1 `lista` "O que fica" com 3 leituras factuais (aproveitamento de quem decidiu, tendência que se repetiu, o que observar no próximo jogo).
   - Procure no box score: diferença na linha de três, maior sequência (`most_unanswered`), parcial do último quarto, garrafão, banco, contra-ataque, segunda chance, lances livres tentados, erros que viraram pontos, aproveitamento real (TS%) dos titulares.
   - Reel "3 números" com as mesmas informações (gancho, 3 cenas `numero`, CTA), **só para o TikTok**. No X e no Instagram o Raio-X é o carrossel: o mesmo conteúdo em outro formato no mesmo canal é repetição (pautas.md). O reel da noite no X e no Instagram é outro ângulo.
   - Horários: carrossel às 12h no X (até 4 imagens) e no Instagram (5).
   - **TikTok: o reel do Raio-X sai às 12h**, ou às 11h se o jogo acabou antes das 18h, nunca à noite. Lá o que conta é ser recente: nada sobre um jogo sai no TikTok mais de 18 horas depois do fim.

4. **Dia de jogo:**
   - Pré-jogo: confirme horário e onde assistir no Brasil. Cartaz `prejogo` no horário da grade, no X e no Instagram, com um fato de contexto real.
   - Reel do dia de jogo no horário da grade: **nunca abre com "Hoje tem"**, que é do pré-jogo. Escolha um ângulo do cardápio de pautas.md (história do confronto, o duelo da noite, o confronto em números, reencontro) e só cite o horário na legenda.
   - Na Filadélfia: um cartaz `manchete` com a leitura da imprensa local sobre o jogo (prévia, palpite, debate), com o nome do jornalista, no X (e no Instagram se houver espaço no feed).
   - O confronto em números: cartaz `comparativo` (campanha, ataque, defesa, três pontos, ou retrospecto), no X e no Instagram, quando houver espaço.
   - **Pós-jogo rápido:** se ainda não existe um turno de pós-jogo para esse jogo (veja `posjogo` no registro), crie **dois** turnos extras com `create_trigger`, para não depender de um só (em 15/11 o primeiro travou e o placar saiu 40 minutos depois do fim): name "Pós-jogo [adversário] [dd/mm] (1)" com run_once_at igual ao início mais 2h30, e "... (2)" com o início mais 3h05, no formato `AAAA-MM-DDTHH:MM:00[America/Sao_Paulo]`, initiation "human_schedule", notifications `{}`, prompt = o texto de `playbook/posjogo-prompt.txt` com os campos preenchidos (tentativa 1 e tentativa 2). Confira no resultado que `mcp_connections` inclui Buffer; se não incluir, apague com `delete_trigger` e anote na central (o turno das 0h51 cobre). Registre os dois ids em `posjogo` no registro.
   - Story do Instagram: o reel do dia (vídeo) ou um cartaz diferente do pré-jogo do feed.
   - Cola do jogo na central: 4 ou 5 pontos com números (campanha, sequência, médias dos destaques, desfalques do relatório de lesões, retrospecto recente contra o adversário), fontes e o roteiro de 4 momentos para o Rodrigo comentar no X ao vivo.

5. **Número do dia ou Neste dia na história** (todo dia, menos quando o Raio-X e o pré-jogo já encheram o feed do Instagram):
   - Número do dia: um dado da temporada do 76ers que surpreende (ranking na liga, sequência, marca individual, comparação com temporadas passadas). Primeiro a `fila_pautas`, depois os fios que chegaram a um marco sem post; só então procure um número novo. Cartaz `numero` em papel azul (o padrão do kit), com texto de apoio de até 14 palavras.
   - Neste dia na história: um jogo ou fato marcante do 76ers nesta data (títulos de 1967 e 1983, Wilt Chamberlain, Julius Erving, Moses Malone, Charles Barkley, Allen Iverson, o Processo, recordes). Só com duas fontes. Cartaz `numero` com o ano gigante, papel azul.
   - Publique às 16h no X e no Instagram. Uma vez por semana, transforme o melhor desses num reel.

6. **Domingo:** agenda da semana seguinte (`agenda`, até 8 jogos), às 11h no X e no Instagram.

   **Quarta-feira:** a curiosidade da série "2001: 25 anos" entra no lugar do número do dia.
   **Sexta-feira:** o post "From Brazil" em inglês, às 16h no X e no Instagram, marcando @sixers.

   **TikTok, todo dia (3 posts, 3 ganchos diferentes, nos horários da grade):** no dia de jogo, o carrossel é o pré-jogo e o reel é outro ângulo do cardápio; sem jogo, às 21h30, um formato só do TikTok (veja "TikTok" no LEIA-PRIMEIRO). A primeira foto do carrossel alterna amarelo e azul com o post anterior do TikTok. Registre em `tiktok` no registro para não repetir tema.

7. **Notícias:** varredura das fontes locais das últimas 18 horas (veja `radar.md`, passos 2 a 4).

8. **Segunda-feira, números da semana:** `get_aggregated_post_metrics` dos últimos 7 dias por canal e `list_posts` com `includeMetrics` para achar os 3 posts com mais alcance ou interação. Escreva na central o bloco `semana`: `{"titulo": "Semana de [dd/mm] a [dd/mm]", "itens": [{"rotulo": "Posts", "valor": "..."}, {"rotulo": "Impressões", "valor": "..."}, ...], "destaques": ["formato e tema do post, com o número", ...], "ajuste": "uma frase sobre o que fazer mais nesta semana"}`. Use o que funcionou para escolher os formatos da semana.

9. **Para promover:** escolha o vídeo do TikTok do dia para o Rodrigo promover (veja "Promoção paga" no LEIA-PRIMEIRO) e ponha o item na central.

10. **Revise:** rode `kit/grade.py` com as mídias de hoje e as de ontem e olhe a grade antes de agendar (pautas.md). Registre `plano`, `fatos` e `trilhas`.

11. **Feche:** registro (com `rodadas.manha` = "AAAA-MM-DD HH:MM feito") e central (os dois lugares). Mensagem ao Rodrigo só em caso de erro.
