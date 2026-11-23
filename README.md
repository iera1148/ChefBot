# ChefBot

ChefBot is a Malaysian cooking assistant for teens. It suggests recipes from leftover ingredients, explains simple kitchen science, and answers questions about local food such as nasi goreng and sambal. The page also includes short games that award XP.

## Features

- Chat with ChefBot, powered by OpenAI (`gpt-4o-mini`)
- Peti Sejuk Surprise: recipe ideas from ingredients you already have
- XP for each chat message, saved for a guest user in SQLite
- Kitchen games: Chef Catch, Rasa Memory, and Bahan Misteri

## Setup

Python 3 is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp app.env.example app.env
```

Open `app.env` and set your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

`app.env` and the SQLite database in `instance/` stay on your computer. They are listed in `.gitignore`.

## Run

```bash
python3 ChefBot.py
```

Open http://127.0.0.1:5000 in a browser.
