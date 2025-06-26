# Discord Automatic Year Bot
  Ένα Discord bot που διαχειρίζεται την ακαδημαϊκή χρονιά των χρηστών.

# Τι κάνει
- Επιτρέπει στους χρήστες να επιλέξουν την ακαδημαϊκή τους χρονιά με slash command
- Αναβαθμίζει αυτόματα τη χρονιά κάθε 1 Οκτωβρίου
- Οι χρήστες μπορούν να ορίσουν τη χρονιά μόνο μία φορά, εκτός αν είναι διαχειριστές

# Εγκατάσταση
```bash
git clone https://github.com/vakonquipo/discord-automatic-year-bot.git
cd discord-automatic-year-bot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
DISCORD_TOKEN=your_discord_bot_token_here
python bot.py
