from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.database as db

router_admin = Router()


class Reg(StatesGroup):
    del_id = State()


@router_admin.message(F.text == 'Данные по ID')
async def viev_id(message: Message, state: FSMContext):
    await message.answer(f"{await db.db_select_users()}")
    await state.clear()


@router_admin.message(F.text == '🗑️Удалить ID')
async def delete_id(message: Message, state: FSMContext):
    await state.set_state(Reg.del_id)
    await message.answer('Введите ID')


@router_admin.message(Reg.del_id)
async def delete_id_reg(message: Message, state: FSMContext):
    await state.update_data(del_id=message.text)
    data_state = await state.get_data()
    await db.db_delete_id(data_state['del_id'])
    await message.answer('Данные по ID удалены')
    await state.clear()
