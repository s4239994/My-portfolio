# AI-Powered Customer Support Chatbot

A customer support assistant with a real persona, sentiment detection, and
automatic hand-off to a human agent when needed -- available both as a web
chat widget and a terminal channel. Runs on a free, local AI model -- no
account, no API key, no cost.

## What it does

- **Natural conversation**, driven by a local AI model, not a rigid decision tree
- **Personalized responses** -- optionally looks up a customer's account and
  order details, but only if the customer explicitly consents
- **Sentiment detection** on every message (positive / neutral / frustrated / angry)
- **Human hand-off** -- automatically flags a conversation for a human agent
  when the customer is angry, explicitly asks for a person, or uses phrases
  like "talk to a human"
- **Multi-channel** -- the same conversation engine (`chatbot.py`) powers both
  a Streamlit web chat (`app.py`) and a plain terminal chat (`cli_channel.py`),
  so adding a new channel (Slack, SMS, etc.) later means writing a thin
  adapter, not rebuilding the bot

## Setup

1. Install [Ollama](https://ollama.com/) -- a free tool that runs AI models
   locally on your own computer.
2. Pull the model this project uses:
   ```
   ollama pull llama3.2:3b
   ```
   (about 2 GB, one-time download)
3. Install the Python dependencies:
   ```
   pip install -r requirements.txt
   ```

That's it -- no accounts, no API keys. Ollama runs a local server in the
background automatically once installed.

## Running it

**Web chat:**
```
streamlit run app.py
```

**Terminal chat:**
```
python cli_channel.py
```

Both use the exact same conversation engine and persona -- try the same
question in each to see it behave identically.

## How it's organized

- **[persona.py](persona.py)** + **[config/persona.json](config/persona.json)** --
  the brand's name, tone, greeting, and escalation policy. Edit the JSON file
  to change how the bot sounds without touching any code.
- **[profiles.py](profiles.py)** + **[data/customers.csv](data/customers.csv)** --
  mock customer records (name, plan, recent order). In a real deployment this
  would be a real CRM/database lookup instead of a CSV.
- **[llm.py](llm.py)** -- the actual call to the local AI model via Ollama.
  Uses structured outputs (a JSON schema) so every response comes back as a
  reply, a sentiment label, and a handoff recommendation, all in one call.
- **[handoff.py](handoff.py)** -- decides whether to escalate (either the
  model recommends it, or the message contains a phrase like "talk to a
  human"), and logs a ticket to `data/handoff_tickets.json`.
- **[chatbot.py](chatbot.py)** -- the channel-agnostic conversation engine
  that ties the above together. Both channels just call `.send()` on it.
- **[app.py](app.py)** -- the Streamlit web chat channel.
- **[cli_channel.py](cli_channel.py)** -- the terminal chat channel.

## Editing the persona

Change `config/persona.json` -- `brand_name`, `tone`, `greeting`, and
`escalation_policy` are all plain text fed into the system prompt. No code
changes needed.

## Reviewing hand-offs

Every escalated conversation is appended to `data/handoff_tickets.json` with
the full transcript, the reason, and a timestamp -- a human agent (or you,
while testing) can review these to see exactly what happened and why.

## Using a bigger model

`llama3.2:3b` (in `llm.py`) is small and fast, tuned to run on an ordinary
laptop. For noticeably better conversation quality at the cost of a larger
download and slower replies, pull a bigger model and change `MODEL` in
`llm.py` to match, e.g.:
```
ollama pull qwen2.5:7b
```

## Honest scope notes

- **"Multi-channel"** here means the core bot logic is fully decoupled from
  any one interface (proven by having two working channels already) -- it
  does not include real integrations with Slack, SMS, or WhatsApp, which
  would each need their own API credentials and adapter.
- **"Continuously tune and retrain"** is implemented as: an editable persona
  file, plus a full transcript log of every conversation that got escalated --
  a human can review those logs and adjust the persona or escalation rules
  over time. This project does not fine-tune or retrain the underlying model.
