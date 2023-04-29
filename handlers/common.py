from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Привет, я бот-переводчик.\n"
             "По запросу /translate я могу перевести заданный вами текст.\n"
             "Если хотите поменять направление перевода, то пишите /translate.",
    )
