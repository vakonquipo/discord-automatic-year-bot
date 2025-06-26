# Discord Automatic Year Bot
  Ένα Discord bot που διαχειρίζεται την ακαδημαϊκή χρονιά των χρηστών.

# Τι κάνει
- Επιτρέπει στους χρήστες να επιλέξουν την ακαδημαϊκή τους χρονιά με slash command
- Αναβαθμίζει αυτόματα τη χρονιά κάθε 1 Οκτωβρίου
- Οι χρήστες μπορούν να ορίσουν τη χρονιά μόνο μία φορά, εκτός αν είναι διαχειριστές

# Εγκατάσταση
1. Κλωνοποίηση repository:
  ```bash
  git clone https://github.com/vakonquipo/discord-automatic-year-bot.git
  cd discord-automatic-year-bot
2. Δημιουργία και ενεργοποίηση virtual environment (Windows PowerShell):
  python -m venv venv
  .\venv\Scripts\Activate.ps1
3. Εγκατάσταση απαιτήσεων:
  pip install -r requirements.txt
4. Δημιουργία αρχείου .env με το Discord token:
  DISCORD_TOKEN=your_discord_bot_token_here
5. Εκτέλεση:
  python bot.py
