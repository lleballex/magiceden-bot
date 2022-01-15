import handlers
from misc import dp, bot
from core.parser import Parser
from misc import PARSERS, DEBUG
from models import User, Parser as ParserModel

import asyncio
import traceback
from pathlib import Path
from loguru import logger
from aiogram import executor
from aiogram.utils.exceptions import InvalidHTTPUrlContent, WrongFileIdentifier


async def parsing():
    while True:
        try:
            await asyncio.sleep(5)

            for parser in PARSERS:
                result = parser.parse()

                if result[0] and not result[1]:
                    continue

                for user in User.select():
                    if not result[0]:
                        await bot.send_message(user.user_id, f'Ой-ой... Что-то пошло не так - код {result[1]}')
                    else:
                        for item in result[1]:
                            caption = f'{item["title"]} - {item["price"]}\n{item["url"]}'
                            try:
                                await bot.send_photo(user.user_id, item['image'], caption)
                            except (InvalidHTTPUrlContent, WrongFileIdentifier):
                                await bot.send_message(user.user_id, caption)
        except:
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    logger.add(Path().resolve().parent / 'logs.log', level=('DEBUG' if DEBUG else 'INFO'))

    for model in ParserModel.select():
        parser = Parser.from_model(model)
        parser.parse(initial=True)
        PARSERS.append(parser)

    loop = asyncio.get_event_loop()
    loop.create_task(parsing())

    executor.start_polling(dp, skip_updates=True)