from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.database as db

router_admin = Router()


@router_admin.message(F.text == 'Данные по ID')
async def add_user_data(message: Message, state: FSMContext):
    await message.answer(f"{await db.db_select_users()}")
    await state.clear()
