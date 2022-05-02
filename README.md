# ⚡ MagicEdenBot

It is a telegram bot that parser NFTs from [Magic Eden](https://magiceden.io/)

### Tools:

- 💪 Aiogram
- 😄 Peewee
- 🤹🏽 Loguru

## 🔥 Getting started

### Installing

##### For linux

```bash
git clone https://github.com/lleballex/magiceden-bot.git
cd magiceden-bot
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt

# First write the data to .env (more details below)

cd src
python migrate.py
```

##### For windows

```bash
git clone https://github.com/lleballex/magiceden-bot.git
cd magiceden-bot
python -m venv env
env\scripts\activate
pip install -r requirements.txt

# First write the data to .env (more details below)

cd src
python migrate.py
```

#### magiceden-bot/.env

```
API_TOKEN=api token of the bot
ADMIN=admin id
DEBUG=True or False
```

### Starting

```bash
python bot.py
```

## 🙋🏽‍♂️ Contact me

[<img width="30px" title="lleballex | Telegram" src="https://raw.githubusercontent.com/github/explore/main/topics/telegram/telegram.png">](https://t.me/lleballex)
[<img width="30px" title="lleballex | VK" src="https://raw.githubusercontent.com/github/explore/main/topics/vk/vk.png">](https://vk.com/lleballex)
