from aiogram.dispatcher.filters.state import StatesGroup, State


class MainStates(StatesGroup):
    action_wait = State()
    parser_view = State()


class CreateParser(StatesGroup):
    collection = State()
    field = State()
    value = State()
    min_price = State()
    max_price = State()