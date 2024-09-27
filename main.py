import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from Utils.keyboards import ButtonText, get_on_start_kb, FuncKb

load_dotenv()
TOKEN = getenv("TOKEN")

dp = Dispatcher()


class Form(StatesGroup):
    func = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text=f"Hello, {html.bold(message.from_user.full_name)}!",
                         reply_markup=get_on_start_kb())


@dp.message(F.text == ButtonText.HELP)
@dp.message(Command('help', prefix='!/'))
async def help_handler(message: Message):
    text = f"I`m a calculation bot"
    await message.answer(text=text)


@dp.message(Command('test', prefix='!/'))
async def calculator_method(message: Message, state: FSMContext):
    await state.set_state(Form.func)
    kb = FuncKb()
    await state.update_data(func=kb)
    await message.answer(text='Фаша функция: ',
                         reply_markup=kb.getMarkup())


@dp.callback_query(F.data.startswith('num'))
async def calculator_num_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    kb: FuncKb = data['func']
    kb + callback.data[-1]
    text = kb.getText()
    await state.update_data(func=kb)
    await callback.answer()
    await callback.message.edit_text(text=text, reply_markup=kb.getMarkup())


@dp.callback_query(F.data.startswith('do'))
async def calculator_do_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    kb: FuncKb = data['func']
    do = callback.data.split('_')[-1]

    match do:
        case ')':
            kb.pressedBracket()
        case '(':
            kb.pressedBracket()
        case 'backspace':
            kb.pressedBackspace()
        case 'clear':
            kb.clearFunc()
        case 'done':
            kb.pressedDone()
        case 'pow':
            kb.pressedPower()

    text = kb.getText()
    await state.update_data(func=kb)
    await callback.message.edit_text(text=text, reply_markup=kb.getMarkup())


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    await dp.start_polling(bot, storage=storage)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())