from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import MY_ID

import app.database as db
import app.keyboards as kb

router = Router()


class Reg(StatesGroup):
    add_user = State()
    del_user = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await db.start_db(message.from_user.id, message.from_user.full_name)
    await message.answer('Привет!', reply_markup=kb.add_user_data)
    await state.clear()


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    if message.from_user.id != MY_ID:
        await message.answer('Вы не администратор')
        return
    await message.answer('Вы нажали на кнопку администратора', reply_markup=kb.admin)


@router.message(F.text == '✖ Отмена')
async def add_user_data(message: Message, state: FSMContext):
    await message.answer("Действие отменено")
    await state.clear()


@router.message(F.text == 'Просмотр данных')
async def add_user_data(message: Message, state: FSMContext):
    await message.answer(f"{await db.db_select()}")
    await state.clear()


@router.message(F.text == 'Добавить данные')
async def add_user_data(message: Message, state: FSMContext):
    await state.set_state(Reg.add_user)
    await message.answer('Введите Ф.И. и дату рождения\nПример:\nИванов Иван 30.01.2000')


@router.message(Reg.add_user)
async def add_user_data(message: Message, state: FSMContext):
    await state.update_data(add_user=message.text)
    data_state = await state.get_data()
    await db.add_db(data_state['add_user'])
    await message.answer('Данные добавлены')
    await state.clear()


@router.message(F.text == 'Удалить данные')
async def add_user_data(message: Message, state: FSMContext):
    await state.set_state(Reg.del_user)
    await message.answer('Введите Ф.И.\nПример: Иванов Иван')


@router.message(Reg.del_user)
async def add_user_data(message: Message, state: FSMContext):
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

