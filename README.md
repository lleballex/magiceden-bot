# Telegram NFT parser from [Magic Eden](https://magiceden.io/)

## Setup

**For linux**

```bash
git clone https://github.com/lleballex/magiceden-bot.git

cd magiceden-bot

python3 -m venv env

. env/bin/activate

pip install -r requirements.txt

cd src

python migrate.py
```

**For windows**

```bash
git clone https://github.com/lleballex/magiceden-bot.git

cd magiceden-bot

python -m venv env

env\scripts\activate

pip install -r requirements.txt

cd src

python migrate.py
```

**magiceden-bot/.env**

```
API_TOKEN=api token of the bot

ADMIN=admin id

DEBUG=True or False
```

## Start bot

```bash
python bot.py
```