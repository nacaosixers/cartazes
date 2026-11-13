# Turno da manhã (7h51)

É a rodada completa do dia. Leia antes `LEIA-PRIMEIRO.md` e `fontes.md`.

1. **Prepare:** `get_account` (hora atual), `list_channels`, `list_posts` dos últimos 2 dias e `estado/registro.json`.

2. **Placar:** se o 76ers jogou nas últimas 36 horas e o placar ainda não saiu (o turno da noite pode já ter postado), faça o cartaz `placar` com a frase do que decidiu (números reais do box score). Agende para 8h30 no X e no Instagram.

3. **Raio-X do último jogo** (se ainda não foi feito para esse jogo):
   - Carrossel de 5 cartazes: capa (`cartaz` amarelo com "Raio-X" e o placar), 3 cartazes `numero` (os 3 números que mais explicam o jogo, cada um com rótulo e uma frase de contexto) e 1 `lista` "O que fica" com 3 leituras factuais (aproveitamento de quem decidiu, tendência que se repetiu, o que observar no próximo jogo).
   - Procure no box score: diferença na linha de três, maior sequência (`most_unanswered`), parcial do último quarto, garrafão, banco, contra-ataque, segunda chance, lances livres tentados, erros que viraram pontos, aproveitamento real (TS%) dos titulares.
   - Reel "3 números" com as mesmas informações (capa, 3 cenas `numero`, CTA).
   - Horários: carrossel às 12h no X (até 4 imagens) e no Instagram; reel às 19h30 no Instagram, no X (vídeo) e no TikTok se existir. Se houver jogo hoje antes das 19h30, publique o reel às 16h.

4. **Dia de jogo:**
   - Pré-jogo: confirme horário e onde assistir no Brasil. Cartaz `prejogo` às 12h (se o jogo for antes das 16h, às 9h30), no X e no Instagram, com um fato de contexto real.
   - Reel de contagem às 18h (ou 2 horas antes se o jogo for à tarde): cena 1 "Hoje tem / 76ers / contra o [adversário]"; cena 2 `numero` com o horário ("21h", rótulo "de Brasília, no [onde assistir]"); cena 3 `numero` com o dado mais forte do confronto (campanha, sequência, média de um destaque); CTA.
   - **Pós-jogo rápido:** crie um turno extra com `create_trigger` para o placar sair minutos depois do fim: name "Pós-jogo [adversário] [dd/mm]", run_once_at no formato `AAAA-MM-DDTHH:MM:00[America/Sao_Paulo]` igual ao horário de início mais 2h15, initiation "human_schedule", notifications `{}`, prompt = o texto de `playbook/posjogo-prompt.txt` com os campos preenchidos (tentativa 1). Confira no resultado que `mcp_connections` inclui Buffer; se não incluir, apague com `delete_trigger` e anote na central (o turno das 0h51 cobre). Registre o id em `posjogo` no registro.
   - Story do pré-jogo no Instagram às 12h (cartaz passado pelo `story.py`).
   - Cola do jogo na central: 4 ou 5 pontos com números (campanha, sequência, médias dos destaques, desfalques do relatório de lesões, retrospecto recente contra o adversário), fontes e o roteiro de 4 momentos para o Rodrigo comentar no X ao vivo.

5. **Número do dia ou Neste dia na história** (todo dia, menos quando o Raio-X e o pré-jogo já encheram o feed do Instagram):
   - Número do dia: um dado da temporada do 76ers que surpreende (ranking na liga, sequência, marca individual, comparação com temporadas passadas). Cartaz `numero`.
   - Neste dia na história: um jogo ou fato marcante do 76ers nesta data (títulos de 1967 e 1983, Wilt Chamberlain, Julius Erving, Moses Malone, Charles Barkley, Allen Iverson, o Processo, recordes). Só com duas fontes. Cartaz `numero` com o ano gigante, papel azul.
   - Publique às 16h no X e no Instagram. Uma vez por semana, transforme o melhor desses num reel.

6. **Domingo:** agenda da semana seguinte (`agenda`, até 8 jogos), às 11h no X e no Instagram.

   **Quarta-feira:** a curiosidade da série "2001: 25 anos" entra no lugar do número do dia.
   **Sexta-feira:** o post "From Brazil" em inglês, às 16h no X e no Instagram, marcando @sixers.

   **TikTok, todo dia:** carrossel de fotos às 12h, reel às 18h e, nos dias sem jogo, um formato só do TikTok às 21h30 (veja "TikTok" no LEIA-PRIMEIRO).

7. **Notícias:** varredura das fontes locais das últimas 18 horas (veja `radar.md`, passos 2 a 4).

8. **Segunda-feira, números da semana:** `get_aggregated_post_metrics` dos últimos 7 dias por canal e `list_posts` com `includeMetrics` para achar os 3 posts com mais alcance ou interação. Escreva na central o bloco `semana`: `{"titulo": "Semana de [dd/mm] a [dd/mm]", "itens": [{"rotulo": "Posts", "valor": "..."}, {"rotulo": "Impressões", "valor": "..."}, ...], "destaques": ["formato e tema do post, com o número", ...], "ajuste": "uma frase sobre o que fazer mais nesta semana"}`. Use o que funcionou para escolher os formatos da semana.

9. **Feche:** registro e central (os dois lugares). Mensagem ao Rodrigo só em caso de erro.
