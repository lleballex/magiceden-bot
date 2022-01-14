from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from peewee import SqliteDatabase
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv(Path().resolve().parent / '.env')


API_TOKEN = getenv('API_TOKEN')

ADMIN = int(getenv('ADMIN'))

DEBUG = getenv('DEBUG') == 'True'

PARSERS = []

COMMANDS = {
    'new_parser': '🆕 Добавить',
    'back': '⬅️ Назад',
    'save': '☑️ Сохранить',
    'delete': '🗑 Удалить',
    'min_price': 'MIN PRICE',
    'max_price': 'MAX PRICE',
}


bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
database = SqliteDatabase('db.sqlite3')