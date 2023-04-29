from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from langdetect import detect
from translate.main import translate
from keyboards.simple_row import make_row_keyboard

router = Router()

languages = ['Английский/Русский', 'Русский/Английский']
lang_dict = dict(zip(languages, ['en', 'ru']))
current_language = ""


class TranslateText(StatesGroup):
    selecting_language = State()
    translating_text = State()


@router.message(Command("translate"))
async def cmd_translate(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите направление перевода:\n",
        reply_markup=make_row_keyboard(languages)
    )
    # Устанавливаем пользователю состояние "выбирает направление перевода"
    await state.set_state(TranslateText.selecting_language)


@router.message(
    TranslateText.selecting_language, F.text.in_(languages)
)
async def translating_text(message: Message, state: FSMContext):
    await state.update_data(selected_language=message.text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите текст:",
        reply_markup=ReplyKeyboardRemove(),
        input_field_placeholder="Введите текст:"
    )
    await state.set_state(TranslateText.translating_text)


@router.message(TranslateText.selecting_language)
async def translate_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого типа перевода.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(languages)
    )


@router.message(TranslateText.translating_text)
async def text_written(message: Message, state: FSMContext):
    await state.update_data(written_text=message.text)
    user_data = await state.get_data()
    selected_language = lang_dict[user_data['selected_language']]
    target_language = list(filter(lambda s: s != selected_language, lang_dict.values()))[0]
    translated_text = translate(user_data['written_text'], src=selected_language, target=target_language)
    if selected_language == translated_text['src']:
        await message.answer(
            text=f"Перевод:\n"
                 f"{translated_text['text']}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text="Кажется, вы ввели некорректный текст.\n\n"
                 "Пожалуйста, попробуйте ввести текст на корректном языке:",
            reply_markup=ReplyKeyboardRemove()
        )
