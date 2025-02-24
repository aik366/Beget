from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import MY_ID
from random import choice
from datetime import datetime
import app.func as fn
import os

import app.database as db
import app.keyboards as kb

router_notes = Router()


class Notes(StatesGroup):
    fsm_note_name = State()
    fsm_note_text = State()
    note_number = State()
    note_list = State()
    note_all = State()
    note_delete = State()
    note_edit = State()
    name_text = State()


@router_notes.message(F.text == '📝Добавить заметку')
async def note_text(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Notes.fsm_note_name)
    await message.answer("Пишите название заметки 👇", reply_markup=kb.note_list)


@router_notes.message(F.text == '📋Мои заметки')
async def my_note_text(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Notes.note_number)
    notes_dict = await db.select_note(message.from_user.id)
    if notes_dict:
        await state.update_data(note_list=notes_dict)
        for key in notes_dict:
            await message.answer(f"{key}. {notes_dict[key][0]}")
        await message.answer("Выберите номер заметки Для\nпросмотра, удаления и редактирования",
                             reply_markup=kb.note_list)
    else:
        await message.answer("У вас нет заметок",
                             reply_markup=kb.note_list)


@router_notes.message(Notes.note_number)
async def number_note(message: Message, state: FSMContext):
    try:
        await state.update_data(note_namber=message.text)
        await state.set_state(Notes.note_all)
        data_state = await state.get_data()
        num = int(data_state['note_namber'])
        await message.answer(f"{num}. {data_state['note_list'][num][0]}", reply_markup=kb.edit_note)
    except Exception as e:
        await message.answer("По этому номеру заметок нет!", reply_markup=kb.note_list)


@router_notes.callback_query(Notes.note_all, F.data == 'note_view')
async def view_note(call: CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = int(data_state['note_namber'])
    await call.message.answer(f"{data_state['note_list'][num][1]}", reply_markup=kb.note_list)
    await call.answer()


@router_notes.callback_query(Notes.note_all, F.data == 'note_edit')
async def edit_note(call: CallbackQuery, state: FSMContext):
    await state.update_data(note_all=call.data)
    await state.set_state(Notes.note_edit)
    await call.message.answer("Имя заметки или текст заметки?", reply_markup=kb.note_edit)
    await call.answer()


@router_notes.callback_query(Notes.note_edit, F.data == 'edit_name')
async def edit_note_name(call: CallbackQuery, state: FSMContext):
    await state.update_data(note_edit=call.data)
    await state.set_state(Notes.name_text)
    await call.message.answer("Пишите Имя заметки 👇", reply_markup=kb.note_list)
    await call.answer()


@router_notes.callback_query(Notes.note_edit, F.data == 'edit_text')
async def edit_note_text(call: CallbackQuery, state: FSMContext):
    await state.update_data(note_edit=call.data)
    await state.set_state(Notes.name_text)
    await call.message.answer("Пишите текст заметки 👇", reply_markup=kb.note_list)
    await call.answer()


@router_notes.message(Notes.name_text)
async def save_note(message: Message, state: FSMContext):
    await state.update_data(name_text=message.text)
    data_state = await state.get_data()
    num = int(data_state['note_namber'])
    note_name, note_text = data_state['note_list'][num]
    if data_state['note_edit'] == 'edit_name':
        await db.update_note_name(message.from_user.id, data_state['name_text'], note_name, note_text)
        await message.answer("Имя заметки сохранена", reply_markup=kb.note_list)
    else:
        await db.update_note_text(message.from_user.id, data_state['name_text'], note_name, note_text)
        await message.answer("Текст сохранена", reply_markup=kb.note_list)
    await state.clear()


@router_notes.callback_query(Notes.note_all, F.data == 'note_delete')
async def delete_note(call: CallbackQuery, state: FSMContext):
    await state.update_data(note_all=call.data)
    await state.set_state(Notes.note_delete)
    data_state = await state.get_data()
    num = int(data_state['note_namber'])
    await call.message.answer(f"{num}. {data_state['note_list'][num][0]}", reply_markup=kb.note_delete)
    await call.answer()


@router_notes.callback_query(Notes.note_delete, F.data == 'delete_note')
async def delete_note_es(call: CallbackQuery, state: FSMContext):
    await state.update_data(note_delete=call.data)
    data_state = await state.get_data()
    num = int(data_state['note_namber'])
    note_name, note_text = data_state['note_list'][num]
    await db.note_delete(call.from_user.id, note_name, note_text)
    await call.message.answer("Заметка удалена!!!", reply_markup=kb.note_list)
    await call.answer()
    await state.clear()


@router_notes.message(Notes.fsm_note_name)
async def text_note(message: Message, state: FSMContext):
    await state.update_data(fsm_note_name=message.text)
    await state.set_state(Notes.fsm_note_text)
    await message.answer("Пишите текст заметки 👇", reply_markup=kb.note_list)


@router_notes.message(Notes.fsm_note_text)
async def save_note(message: Message, state: FSMContext):
    await state.update_data(fsm_note_text=message.text)
    data_state = await state.get_data()
    await db.add_note(message.from_user.id, data_state['fsm_note_name'], data_state['fsm_note_text'])
    await message.answer("Заметка сохранена", reply_markup=kb.note_list)


@router_notes.callback_query(F.data == 'delete')
async def delete_user(call: CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    await db.delete_to_number(call.from_user.id, int(data_state['del_number']))
    await call.message.answer('Данные удалены', reply_markup=kb.note_list)
    await state.clear()
    await call.answer()


@router_notes.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено", reply_markup=kb.add_user_data)
    await state.clear()
    await call.answer()


@router_notes.callback_query(F.data == 'cancel_note')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено", reply_markup=kb.note_list)
    await state.clear()
    await call.answer()

