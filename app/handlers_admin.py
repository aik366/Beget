from aiogram import Bot, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import MY_ID
import os

import app.database as db

router_admin = Router()


class Reg(StatesGroup):
    del_id = State()
    text_1 = State()
    text_2 = State()
    text_img = State()


@router_admin.message(F.text == "Объявление")
async def cmd_admin_ad(message: Message, state: FSMContext):
    await state.set_state(Reg.text_1)
    await message.answer("Пишите объявление")


@router_admin.message(Reg.text_1)
async def reg_admin_text_1(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(text_1=message.text)
    data_state = await state.get_data()
    for tg_id, name, data in await db.db_select_users():
        await bot.send_message(int(tg_id), f"Привет {name}!\n{data_state['text_1']}\nАдминистрация!!!")
    await state.clear()


@router_admin.message(F.text == "Картинка")
async def cmd_admin_img(message: Message, state: FSMContext):
    await state.set_state(Reg.text_2)
    await message.answer("Пишите объявление")


txt = ''


@router_admin.message(Reg.text_2)
async def reg_admin_text_2(message: Message, state: FSMContext):
    global txt
    txt = message.text

    await message.answer("Прикрепите картинку")
    await state.clear()


@router_admin.message(F.photo, F.from_user.id == MY_ID)
async def cmd_admin_photo(message: Message, bot: Bot):
    global txt
    if txt:
        for tg_id, name, data in await db.db_select_users():
            await bot.send_photo(int(tg_id), message.photo[-1].file_id,
                                 caption=f"Привет {name}!\n{txt}\nАдминистрация!!!")
        txt = ''
    else:
        file_name = f"images/{len(os.listdir('images')) + 1}.jpg"
        await bot.download(message.photo[-1], destination=file_name)
        await message.answer('Фото сохранено')


@router_admin.message(F.text == 'Данные по ID')
async def viev_id(message: Message, state: FSMContext):
    data_txt = ""
    for tg_id, name, data in await db.db_select_users():
        data_txt += f"{tg_id} {name} {data}\n"
    await message.answer(f"{data_txt}")
    await state.clear()


@router_admin.message(F.text == '🗑️Удалить по ID')
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


@router_admin.message()
async def echo(message: Message):
    await message.reply('ошибка!')
