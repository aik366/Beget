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


class Form(StatesGroup):
    first_name = State()
    last_name = State()
    birthday = State()


def validate_name(name):
    return len(name) >= 2 and name.isalpha()


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


@router.message(F.text == '✨Пожелания')
async def open_wishes(message: Message):
    with open(f"files/wishes.txt", "r", encoding="utf-8") as f:
        wishes_txt = choice(f.read().split('\n'))
        await message.answer(f"{wishes_txt}")


@router.message(F.text == '🥂Тост')
async def open_toasts(message: Message):
    with open(f"files/toasts.txt", "r", encoding="utf-8") as f:
        toasts_txt = choice(f.read().split('\n'))
        await message.answer(f"{toasts_txt}")


@router.message(F.text == '🎁Открытки')
async def file_open_images(message: Message, state: FSMContext):
    img = FSInputFile(f'images/{choice(os.listdir("images"))}')
    await message.answer_photo(img)
    await state.clear()


@router.message(F.text == '🆕Добавить данные')
async def add_data(message: Message, state: FSMContext):
    await state.set_state(Form.first_name)
    await message.answer("Введите имя (только буквы):")


@router.message(Form.first_name)
async def process_first_name(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer("Неверное имя! Используйте только буквы (мин. 2 символа).",
                                    reply_markup=kb.add_user_data)

    await state.update_data(first_name=message.text.title())
    await state.set_state(Form.last_name)
    await message.answer("Введите фамилию (только буквы):", reply_markup=kb.add_user_data)


@router.message(Form.last_name)
async def process_last_name(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer("Неверная фамилия! Используйте только буквы (мин. 2 символа).",
                                    reply_markup=kb.add_user_data)

    await state.update_data(last_name=message.text.title())
    await state.set_state(Form.birthday)
    await message.answer("Введите дату рождения (ДД.ММ.ГГГГ):", reply_markup=kb.add_user_data)


@router.message(Form.birthday)
async def add_user_reg(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text.replace(",", "."), "%d.%m.%Y").date()
    except ValueError:
        return await message.answer("Неверный формат даты! Используйте ДД.ММ.ГГГГ", reply_markup=kb.add_user_data)

    await state.update_data(birthday=message.text)
    data_state = await state.get_data()
    data = f"{data_state['last_name']} {data_state['first_name']} {data_state['birthday']}"
    if not await db.db_check(data):
        await db.add_db(data)
        await message.answer('Данные добавлены', reply_markup=kb.add_user_data)
    else:
        await message.answer('Такой запись уже есть', reply_markup=kb.add_user_data)
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
