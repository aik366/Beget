from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import MY_ID
from random import choice
from datetime import datetime
import os

import app.database as db
import app.keyboards as kb

router = Router()


class Reg(StatesGroup):
    add_user = State()
    del_user = State()


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        s = message.text.replace(",", ".").split()
        s2 = s[2].split(".")
        d_day = s2[0].isdigit() and 1 <= int(s2[0]) <= 31
        d_month = s2[0].isdigit() and 1 <= int(s2[0]) <= 12
        d_year = s2[0].isdigit() and 1900 <= int(s2[0]) <= datetime.now().year
        all_dmy = any([d_day, d_month, d_year])
        if len(s) == 3 and s[0].isalpha() and s[1].isalpha() and s[2].count('.') == 2 and all_dmy:
            return True
        return False


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await db.start_db(message.from_user.id, message.from_user.full_name)
    await message.answer('Привет!', reply_markup=kb.add_user_data)
    await state.clear()


@router.message(Command('help'))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Вы нажали на кнопку помощи')
    await state.clear()


@router.message(Command('admin'))
async def cmd_admin(message: Message, state: FSMContext):
    if message.from_user.id != MY_ID:
        await message.answer('Вы не администратор')
        return
    await message.answer('Вы нажали на кнопку администратора', reply_markup=kb.admin)
    await state.clear()


@router.message(F.text == '❌Отмена')
async def add_cencel(message: Message, state: FSMContext):
    await message.answer("Действие отменено")
    await state.clear()


@router.message(F.text == '👁️Просмотр данных')
async def add_user_viev(message: Message, state: FSMContext):
    await message.answer(f"{await db.db_select()}")
    await state.clear()


@router.message(F.text == '🎁Открытки')
async def file_open_images(message: Message, state: FSMContext):
    img = FSInputFile(f'images/{choice(os.listdir("images"))}')
    await message.answer_photo(img)
    await state.clear()


@router.message(F.text == '🆕Добавить данные')
async def add_user_data(message: Message, state: FSMContext):
    await state.set_state(Reg.add_user)
    await message.answer('Введите Ф.И. и дату рождения\nФормате: дд.мм.гггг\nПример: 👇\nИванов Иван 30.01.2000')


@router.message(Reg.add_user, MyFilter(F.text))
async def add_user_reg(message: Message, state: FSMContext):
    await state.update_data(add_user=message.text)
    data_state = await state.get_data()
    if not await db.db_check(data_state['add_user']):
        await db.add_db(data_state['add_user'])
        await message.answer('Данные добавлены')
    else:
        await message.answer('Такой запись уже есть')
    await state.clear()


@router.message(F.text == '🗑️Удалить данные')
async def delete_user(message: Message, state: FSMContext):
    await state.set_state(Reg.del_user)
    await message.answer('Введите Ф.И.\nПример: Иванов Иван')


@router.message(Reg.del_user)
async def delete_user_reg(message: Message, state: FSMContext):
    await state.update_data(del_user=message.text)
    data_state = await state.get_data()
    data_list = data_state['del_user'].split()
    await db.db_data_delete(data_list[0], data_list[1])
    await message.answer('Данные удалены')
    await state.clear()


@router.message(F.text == '33')
async def file_open(message: Message):
    with open("DATA/33.txt", "r") as file:
        f = file.read()
        await message.answer(f"{f}")


@router.message(F.text == 'log')
async def file_open_logo(message: Message):
    with open("DATA/logs.log", "r") as file:
        f = file.read()[-3000:]
        await message.answer(f"{f}")


@router.message(F.photo, F.from_user.id == MY_ID)
async def cmd_admin_photo(message: Message, bot: Bot):
    try:
        file_name = f"images/{len(os.listdir('images'))+1}.jpg"
        await bot.download(message.photo[-1], destination=file_name)
        await message.answer('Фото сохранено')
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")


@router.message()
async def echo(message: Message):
    await message.reply('ошибка!')
