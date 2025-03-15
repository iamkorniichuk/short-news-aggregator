# Short News Aggregator

Service to summarize news from Telegram.

## Workflow

1. **User adds a Telegram channel** in the admin panel

    ![add channel](/docs/channels.gif)

2. **Service fetches new posts** regularly

    ![fetch posts](/docs/posts.gif)

3. **Embeddings for posts generated** by [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

4. **Posts are clustered** based on semantic embeddings

    ![cluster plot](/docs/plot.png)

5. **Summaries are generated** using [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)

    Example of generated summary:
    ```
    Declan Rice has scored in his last three games for Arsenal. Barcelona will face either Dortmund or Lille in the quarter-final of the Champions League. Man United will play Lyon in the last 8 of the Europa League.
    ```

    Based on next 19 posts:
    ```
    Bruno Fernandes holds the record for the most goal contributions in UEFA Europa League history:
    24 goals
    17 assists

    Antony in his last 52 games for Man United:
    4 goals
    2 assists

    Antony in his first 10 games for Real Betis:
    4 goals
    4 assists.

    A player reborn in Spain.
    ```

    ```
    Bruno Fernandes' last six games:
    vs Everton
    vs Ipswich
    vs Fulham
    vs Real Sociedad
    vs Arsenal
    vs Real Sociedad
    ```

    ```
    Courtois reacts to Simeone's complaints:
    "I'm tired of this victimhood, always crying over things like that. Referees don't want to benefit a team, neither in Spain nor in Europe.
    They saw it clearly with technology and called it that way."
    ```

    ```
    Declan Rice has stepped up in front of goal for Arsenal in their last three games
    vs PSV
    vs Man Utd
    vs PSV
    ```

    ```
    Atletico — Oblak; Marcos Llorente, Giménez, Lenglet, Reinildo; Simeone, De Paul, Pablo Barrios, Gallagher; Griezmann, Julián Álvarez
    Real Madrid — Courtois; Fede Valverde, Rüdiger, Asencio, Mendy; Modric, Tchouaméni, Bellingham; Rodrygo, Mbappé, Vinicius
    ```

    ```
    INSANE UCL campaign from the Brazilian
    10 Games
    11 Goals
    5 Assists

    Barcelona will face EITHER Dortmund or Lille in the Quarter-final
    ```

    ```
    OFFICIAL: Manchester United will play Lyon in the last 8 of the Europa League.
    ```

    ```
    FULL-TIME
    Man United 4 - 1 Real Sociedad
    Tottenham 3 - 1 Az Alkmaar
    Chelsea 1 - 0 Kobenhavn
    ```

    ```
    Goal - FERNANDES (pk)
    Man United 1 - 1 Real Sociedad 16 mins
    ```

    ```
    Goal - OYAZARBAL (pk)
    Man United 0 - 1 Real Sociedad 10 mins
    ```

    ```
    Amorim: "If we look at our performances, we can do much better. We are in a big club. Everyone here has a comfortable life, so we have to improve our results and performances."
    ```

    ```
    Luka Modric on facing Arsenal in the quarter finals of the Champions League:
    "There's still a long way to go until that match. Now we have to focus on Villarreal and go calmly into the international break. Arsenal is a very good team, and it’s going to be another interesting knockout round. But as I said, we need to prepare for Villarreal first, we have to win there, and then we will take the time to think about Arsenal."
    ```

    ```
    Arteta: “Very happy, we are in the Champions League quarter-final for the second consecutive season. We will travel to Madrid, unfortunately we don’t know who yet!”
    ```

    ```
    𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟: The quarter-finals of the Champions League.
    ```

    ```
    𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟: The quarter-final of the Champions League:
    Aston Villa vs. PSG
    ```

    ```
    Price money distribution of the Champions Trophy 2025!
    ```

    ```
    BCCI named Rohit Sharma captain in 2021, and the rest is history!
    ```

    ```
    T20WC 2024: Captain Rohit Sharma
    CT 2025: Vice-Captain Shubman Gill

    The tradition continues....
    ```

    ```
    The GOAT Indian Captains
    ```
