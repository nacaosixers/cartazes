# Turno da manhã (7h51)

É a rodada completa do dia. Leia antes `LEIA-PRIMEIRO.md`, `fontes.md` e `pautas.md`. Antes de gerar qualquer mídia, faça o plano do dia (pautas.md) e confira gancho, fato e formato de cada post.

0. **Já rodou hoje?** Leia `estado/registro.json`. Se `rodadas.manha` já tem a data de hoje, termine sem fazer nada e sem mensagem: outra rodada (o vigia, o radar ou o Claude na conversa) já fez o dia. Vale mesmo que a mensagem que disparou esta rodada peça para fazer o dia: rodada atrasada que publica de novo duplica posts. Se não tem, grave já `rodadas.manha` = "AAAA-MM-DD HH:MM em andamento", faça commit e push, e só então siga.

## Grade do dia (siga a linha do tipo de dia; ela já resolve os choques de horário)

Instagram: até 4 posts no feed, mais o placar logo depois do jogo, com 90 minutos ou mais entre eles; a vaga que sobrar na grade fica para o radar (notícia). Story não conta: 2 por dia, todo dia. Na rota de 20/11 o Instagram mantém a quantidade e muda o formato e a conversa (veja "Instagram" no LEIA-PRIMEIRO). TikTok: até 3 posts por dia, mais o pós-jogo. X: até 8. Se a rodada atrasou, cada horário que já passou vai para o próximo horário livre depois do currentTime + 15 minutos.

| Tipo de dia | X | Instagram feed | Instagram story | TikTok |
|---|---|---|---|---|
| Dia seguinte a jogo, sem jogo hoje | 8h30 placar (se não saiu), 12h Raio-X (4 imagens), 16h número do dia ou história, 19h30 reel de outro ângulo | 8h30 placar (se não saiu), 12h Raio-X (carrossel), 16h reel extra, 19h30 reel | 11h e 20h30, cartazes diferentes do feed | 12h carrossel do Raio-X (11h se o jogo acabou antes das 18h), 18h carrossel (número ou notícia), 21h30 formato próprio |
| Dia de jogo à noite, sem jogo ontem | 12h pré-jogo, 15h30 Na Filadélfia, 16h30 comparativo, 18h reel do dia de jogo, 1 hora antes do jogo o aquecimento | 12h pré-jogo (carrossel com Na Filadélfia, comparativo e o palpite na última foto), 15h reel extra, 18h reel do dia de jogo | 13h30 número do dia ou comparativo; 1 hora antes do jogo, cartaz diferente do feed | 12h carrossel (comparativo, pré-jogo, Na Filadélfia), 18h reel do dia de jogo, pós-jogo |
| Dia seguinte a jogo e dia de jogo à noite (ex.: 16/11) | 8h30 placar (se não saiu), 11h30 Raio-X, 14h pré-jogo, 15h30 Na Filadélfia, 16h30 comparativo, 19h30 reel do dia de jogo, 1 hora antes do jogo o aquecimento | 8h30 placar (se não saiu), 11h30 Raio-X (carrossel), 14h pré-jogo (carrossel com Na Filadélfia, comparativo e o palpite), 19h30 reel do dia de jogo | 16h30 número do dia ou comparativo; 1 hora antes do jogo, Na Filadélfia ou outro cartaz | 11h ou 12h carrossel do Raio-X (dentro das 18 horas), 17h carrossel do pré-jogo, 19h30 reel do dia de jogo, pós-jogo |
| Jogo à tarde (começa até 16h) | 9h30 pré-jogo, 10h30 Na Filadélfia, 11h comparativo, 2 horas antes do jogo o reel, 1 hora antes o aquecimento | 9h30 pré-jogo (carrossel com o palpite), 11h reel extra, 2 horas antes o reel | 10h30 número do dia ou comparativo; 1 hora antes do jogo | 9h45 carrossel do pré-jogo, 2 horas antes o reel, pós-jogo |
| Dia livre (sem jogo ontem nem hoje) | 12h número do dia ou notícia, 16h história ou "2001: 25 anos", 19h30 reel | 12h carrossel (número do dia ou história), 16h reel extra, 19h30 reel | 11h e 20h30, cartazes diferentes do feed | 12h carrossel, 18h reel, 21h30 formato próprio |

Domingo: a agenda da semana entra às 11h no X e no Instagram (ocupa um dos 4 do feed). **Reel extra** (Instagram): o vídeo do TikTok da véspera que ainda não saiu no Instagram, nem com o mesmo tema em outro formato, de preferência um formato próprio (Adivinha quem é, Você sabia?, Explicando o 76ers), com legenda nova para o Instagram; se não houver, número do dia ou história em carrossel. Todo story leva uma pergunta escrita na arte. Sexta: o "From Brazil" às 16h no lugar do número do dia.

1. **Prepare:** `get_account` (hora atual), `list_channels`, `list_posts` dos últimos 2 dias e `estado/registro.json`, inclusive `fios` e `fila_pautas` (pautas.md): o que estiver na fila para hoje entra no plano antes do resto.

2. **Placar:** se o 76ers jogou nas últimas 36 horas e o placar ainda não saiu (o turno da noite pode já ter postado), faça o cartaz `placar` com a frase do que decidiu (números reais do box score). Agende para 8h30 no X e no Instagram. Se o TikTok também ficou sem o placar e o jogo acabou há menos de 18 horas, faça o vídeo curto do pós-jogo (`posjogo.md`, passo 4) e agende no TikTok às 8h45; se já passou das 18 horas, o Raio-X do passo 3 fica no lugar dele.

3. **Raio-X do último jogo** (se ainda não foi feito para esse jogo):
   - Antes de olhar o box score, atualize os fios da temporada no registro (pautas.md). Se o jogo levou um fio a um marco (número redondo, recorde), esse é o primeiro número e o gancho; um a mais não entra.
   - Carrossel de 5 cartazes: capa (`cartaz` amarelo ou azul, alternando com o post anterior do canal, com "Raio-X" e o placar), 3 cartazes `numero` (os 3 números que mais explicam o jogo, cada um com rótulo e uma frase de contexto) e 1 `lista` "O que fica" com 3 leituras factuais (aproveitamento de quem decidiu, tendência que se repetiu, o que observar no próximo jogo).
   - Procure no box score: diferença na linha de três, maior sequência (`most_unanswered`), parcial do último quarto, garrafão, banco, contra-ataque, segunda chance, lances livres tentados, erros que viraram pontos, aproveitamento real (TS%) dos titulares.
   - No TikTok, o Raio-X é um carrossel "3 números" com as mesmas informações: capa e os 3 cartazes `numero` passados pelo `story.py` (teste de 23 a 29/11, registro `testes`; se a manhã de 30/11 decidir voltar ao vídeo, é o reel de 3 cenas `numero` com CTA). No X e no Instagram o Raio-X é o carrossel: o mesmo conteúdo em outro formato no mesmo canal é repetição (pautas.md). O reel da noite no X e no Instagram é outro ângulo.
   - Horários: carrossel às 12h no X (até 4 imagens) e no Instagram (5).
   - **TikTok: o carrossel do Raio-X sai às 12h**, ou às 11h se o jogo acabou antes das 18h, nunca à noite. Lá o que conta é ser recente: nada sobre um jogo sai no TikTok mais de 18 horas depois do fim.

4. **Dia de jogo:**
   - Pré-jogo: confirme horário e onde assistir no Brasil. Cartaz `prejogo` no horário da grade, no X e no Instagram, com um fato de contexto real.
   - Reel do dia de jogo no horário da grade: **nunca abre com "Hoje tem"**, que é do pré-jogo. Escolha um ângulo do cardápio de pautas.md (história do confronto, o duelo da noite, o confronto em números, reencontro) e só cite o horário na legenda.
   - Na Filadélfia: um cartaz `manchete` com a leitura da imprensa local sobre o jogo (prévia, palpite, debate), com o nome do jornalista, no X (no Instagram, só como foto dentro do carrossel do pré-jogo).
   - O confronto em números: cartaz `comparativo` (campanha, ataque, defesa, três pontos, ou retrospecto), no X (no Instagram, dentro do carrossel do pré-jogo).
   - **Ao vivo e pós-jogo rápido:** desde 19/11 quem faz o placar logo depois do fim (e os comentários ao vivo no X, em todo jogo desde 20/11) é a corrente do ao vivo (`aovivo.md`), na conversa do Claude. Confira se o jogo de hoje está em `aovivo_agenda` no registro; se não estiver, anote na central e mande uma mensagem curta ao Rodrigo ("o ao vivo de hoje não está marcado; peça na conversa"). Não crie turnos de pós-jogo com `create_trigger`: numa rodada automática eles pedem aprovação. As redes de segurança seguem: a rodada da 0h51 para jogo à noite, o radar das 17h51 para jogo à tarde, a manhã seguinte às 8h30.
   - **Aquecimento** (só no X, 1 hora antes do jogo): texto curto, sem imagem. Primeira linha "Falta 1 hora: 76ers x [adversário], [hora] de Brasília."; depois a sequência ou a campanha e o desfalque do relatório de lesões, com a fonte; feche com o palpite e o aviso de que os comentários ao vivo saem ali. O pré-jogo é o post que mais aparece no X (212 impressões em média até 22/11), e o aquecimento leva esse público até o ao vivo. Se o relatório de lesões mudar à tarde, o radar corrige o texto agendado com `edit_post`.
   - Stories do Instagram: os 2 da grade, cartazes diferentes do feed, cada um com uma pergunta escrita na arte (LEIA-PRIMEIRO, Instagram).
   - Cola do jogo na central: 4 ou 5 pontos com números (campanha, sequência, médias dos destaques, desfalques do relatório de lesões, retrospecto recente contra o adversário), fontes e o roteiro de 4 momentos, que o ao vivo usa como apoio.

5. **Número do dia ou Neste dia na história** (todo dia, menos quando o Raio-X e o pré-jogo já encheram o feed do Instagram):
   - Número do dia: um dado da temporada do 76ers que surpreende (ranking na liga, sequência, marca individual, comparação com temporadas passadas). Primeiro a `fila_pautas`, depois os fios que chegaram a um marco sem post; só então procure um número novo. Cartaz `numero` em papel azul (o padrão do kit), com texto de apoio de até 14 palavras.
   - Neste dia na história: um jogo ou fato marcante do 76ers nesta data (títulos de 1967 e 1983, Wilt Chamberlain, Julius Erving, Moses Malone, Charles Barkley, Allen Iverson, o Processo, recordes). Só com duas fontes. Cartaz `numero` com o ano gigante, papel azul.
   - Publique às 16h no X. No Instagram, ele entra no carrossel do dia (12h) quando não há Raio-X nem pré-jogo; senão vira um dos stories do dia, com a pergunta na arte. Uma vez por semana, transforme o melhor desses num reel.

6. **Domingo:** agenda da semana seguinte (`agenda`, até 8 jogos), às 11h no X e no Instagram.

   **Terça-feira:** o vídeo vitrine da semana (LEIA-PRIMEIRO, Promoção paga), um vídeo que não envelhece, para quem não conhece a Nação. Sai no reel das 19h30 no X e no Instagram e no formato próprio do TikTok, e é o primeiro da lista de promoção.
   **Quarta-feira:** a curiosidade da série "2001: 25 anos" entra no lugar do número do dia.
   **Sexta-feira:** o post "From Brazil" em inglês, às 16h no X marcando @sixers; no Instagram, às 16h, no lugar do reel extra, também marcando @sixers.

   **TikTok, todo dia (3 posts, 3 ganchos diferentes, nos horários da grade):** no dia de jogo, o carrossel é o pré-jogo e o reel é outro ângulo do cardápio; sem jogo, às 21h30, um formato só do TikTok (veja "TikTok" no LEIA-PRIMEIRO). A primeira foto do carrossel alterna amarelo e azul com o post anterior do TikTok. Registre em `tiktok` no registro para não repetir tema.

7. **Notícias:** varredura das fontes locais das últimas 18 horas (veja `radar.md`, passos 2 a 4).

8. **Segunda-feira, números da semana:** `get_aggregated_post_metrics` dos últimos 7 dias por canal e `list_posts` com `includeMetrics` para achar os 3 posts com mais alcance ou interação. Escreva na central o bloco `semana`: `{"titulo": "Semana de [dd/mm] a [dd/mm]", "itens": [{"rotulo": "Posts", "valor": "..."}, {"rotulo": "Impressões", "valor": "..."}, ...], "destaques": ["formato e tema do post, com o número", ...], "ajuste": "uma frase sobre o que fazer mais nesta semana"}`. Use o que funcionou para escolher os formatos da semana. Leia `testes` no registro: para cada teste que terminou, escreva na central se ele fica, muda ou sai, com o número que decidiu, e atualize o playbook e o registro. Seguidores: compare com `seguidores` no registro (o Claude grava quando o Rodrigo manda os prints dos perfis na conversa) e ponha a diferença no bloco; se o último registro tiver mais de 7 dias, deixe na central o pedido "manda os prints dos 3 perfis para eu medir a semana" (só na central, sem mensagem).

9. **Para promover:** escolha o vídeo do TikTok do dia para o Rodrigo promover (veja "Promoção paga" no LEIA-PRIMEIRO) e ponha o item na central.

10. **Revise:** rode `kit/grade.py` com as mídias de hoje e as de ontem e olhe a grade antes de agendar (pautas.md). Registre `plano`, `fatos` e `trilhas`.

11. **Feche:** registro (com `rodadas.manha` = "AAAA-MM-DD HH:MM feito") e central (os dois lugares). Mensagem ao Rodrigo só em caso de erro.
