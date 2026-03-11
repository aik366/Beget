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

router = Router()


class Form(StatesGroup):
    first_name = State()
    last_name = State()
    birthday = State()
    del_user = State()
    del_number = State()
    del_len_list = State()
    edit_number = State()
    edit_len_list = State()
    edit_surname = State()
    edit_name = State()
    edit_data = State()
    surname_edit = State()
    name_edit = State()
    data_edit = State()
    body_Index = State()


def validate_name(name):
    return len(name) >= 2 and name.isalpha()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, state: FSMContext):
    await db.start_db(message.from_user.id, message.from_user.full_name)
    if message.from_user.id != MY_ID:
        await bot.send_message(MY_ID, f'Пользователь {message.from_user.full_name} начал работу с ботом')
    await message.answer(f'Привет! {message.from_user.full_name}', reply_markup=kb.add_user_data)
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


@router.message(F.text == '🏠Главное меню')
async def start_menu(message: Message, state: FSMContext):
    await message.answer('Главное меню', reply_markup=kb.add_user_data)
    await state.clear()


@router.message(F.text == '❌Отмена')
async def add_cencel(message: Message, state: FSMContext):
    await message.answer("Действие отменено")
    await state.clear()


@router.message(F.text == '👁️Просмотр данных')
async def add_user_viev(message: Message, state: FSMContext):
    await message.answer(f"{await db.db_select()}", reply_markup=kb.view_birthday)
    await state.clear()


@router.callback_query(F.data == 'birthday')
async def add_user_viev_data(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"{await db.select_data()}", reply_markup=kb.add_user_data)
    await state.clear()
    await call.answer()


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


@router.message(F.text == '🗑️Удалить данные')
async def delete_user(message: Message, state: FSMContext):
    await state.set_state(Form.del_number)
    list_id = await db.delete_select(message.from_user.id)
    await state.update_data(del_len_list=len(list_id.split('\n')) - 1)
    if list_id:
        await message.answer(f"{list_id}\nВведите порядковый номер\nДля удаления данных")
    else:
        await message.answer('У вас нет данных для удаления', reply_markup=kb.add_user_data)
        await state.clear()


@router.message(F.text == '✏️Редактировать')
async def view_user(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Form.edit_number)
    list_id = await db.delete_select(message.from_user.id)
    await state.update_data(edit_len_list=len(list_id.split('\n')) - 1)
    if list_id:
        await message.answer(f"{list_id}\nВведите порядковый номер\nДля редактирования данных")
    else:
        await message.answer('У вас нет данных для редактирования', reply_markup=kb.add_user_data)
        await state.clear()


@router.message(F.text == '🆕Добавить данные')
async def add_data(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Form.first_name)
    await message.answer("Введите имя (только буквы):", reply_markup=kb.cancel_one)


@router.message(F.text == '😂Анекдот дня')
async def open_wishes(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"{await fn.anekdot_random()}")


@router.message(F.text == '💲Курсы валют')
async def open_wishes(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"{await fn.currency()}")


@router.message(F.text == '🌦️Погода')
async def open_wishes(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"{await fn.get_weather_forecast()}")


@router.message(Form.del_number)
async def delete_user_reg(message: Message, state: FSMContext):
    await state.update_data(del_number=message.text)
    data_state = await state.get_data()
    if not message.text.isdigit() or int(message.text) > data_state['del_len_list'] or int(message.text) < 1:
        return await message.answer("Вы ввели неверное число\nПопробуйте ещё раз", reply_markup=kb.add_user_data)
    data_state = await state.get_data()
    surname, name, data = await db.edit_to_number(message.from_user.id, int(data_state['del_number']))
    await state.update_data(edit_surname=surname, edit_name=name, edit_data=data)
    await message.answer(f'{surname} {name} {data}', reply_markup=kb.delete)


@router.callback_query(F.data == 'delete')
async def delete_user(call: CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    await db.delete_to_number(call.from_user.id, int(data_state['del_number']))
    await call.message.answer('Данные удалены', reply_markup=kb.note_list)
    await state.clear()
    await call.answer()


@router.message(Form.edit_number)
async def view_user_reg(message: Message, state: FSMContext):
    await state.update_data(edit_number=message.text)
    data_state = await state.get_data()
    if not message.text.isdigit() or int(message.text) > data_state['edit_len_list'] or int(message.text) < 1:
        return await message.answer("Вы ввели неверное число\nПопробуйте ещё раз", reply_markup=kb.note_list)
    data_state = await state.get_data()
    surname, name, data = await db.edit_to_number(message.from_user.id, int(data_state['edit_number']))
    await state.update_data(edit_surname=surname, edit_name=name, edit_data=data)
    await message.answer(f'{surname} {name} {data}', reply_markup=kb.edit)


@router.callback_query(F.data == 'surname')
async def edit_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.surname_edit)
    await call.message.answer("Введите новую фамилию (только буквы):")
    await call.answer()


@router.message(Form.surname_edit)
async def edit_user_reg(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer("Неверная фамилия! Используйте только буквы (мин. 2 символа).",
                                    reply_markup=kb.add_user_data)
    await state.update_data(surname_edit=message.text.capitalize())
    data_state = await state.get_data()
    await db.update_surname(data_state['surname_edit'], data_state['edit_surname'], data_state['edit_name'])
    await message.answer('Данные изменены', reply_markup=kb.add_user_data)
    await state.clear()


@router.callback_query(F.data == 'name')
async def edit_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.name_edit)
    await call.message.answer("Введите новое имя (только буквы):")
    await call.answer()


@router.message(Form.name_edit)
async def edit_user_reg(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer("Неверная имя! Используйте только буквы (мин. 2 символа).",
                                    reply_markup=kb.add_user_data)
    await state.update_data(name_edit=message.text.capitalize())
    data_state = await state.get_data()
    await db.update_name(data_state['name_edit'], data_state['edit_surname'], data_state['edit_name'])
    await message.answer('Данные изменены', reply_markup=kb.add_user_data)
    await state.clear()


@router.callback_query(F.data == 'date')
async def edit_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.data_edit)
    await call.message.answer("Введите новую дату\nВ формате ДД.ММ.ГГГГ:")
    await call.answer()


@router.message(Form.data_edit)
async def edit_user_reg(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text.replace(",", "."), "%d.%m.%Y").date()
    except ValueError:
        return await message.answer("Неверный формат даты! Используйте ДД.ММ.ГГГГ", reply_markup=kb.add_user_data)
    await state.update_data(data_edit=message.text)
    data_state = await state.get_data()
    await db.update_data(data_state['data_edit'], data_state['edit_surname'], data_state['edit_name'])
    await message.answer('Данные изменены', reply_markup=kb.add_user_data)
    await state.clear()


@router.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено", reply_markup=kb.add_user_data)
    await state.clear()
    await call.answer()


@router.callback_query(F.data == 'cancel_note')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено", reply_markup=kb.note_list)
    await state.clear()
    await call.answer()


@router.message(Form.first_name)
async def process_first_name(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer("Неверное имя! Используйте только буквы (мин. 2 символа).",
                                    reply_markup=kb.add_user_data)

    await state.update_data(first_name=message.text.title())
    await state.set_state(Form.last_name)
    await message.answer("Введите фамилию (только буквы):", reply_markup=kb.cancel_one)


@router.message(Form.last_name)
async def process_last_name(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer("Неверная фамилия! Используйте только буквы (мин. 2 символа).",
                                    reply_markup=kb.add_user_data)

    await state.update_data(last_name=message.text.title())
    await state.set_state(Form.birthday)
    await message.answer("Введите дату рождения (ДД.ММ.ГГГГ):", reply_markup=kb.cancel_one)


@router.message(Form.birthday)
async def add_user_reg(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text.replace(",", "."), "%d.%m.%Y").date()
    except ValueError:
        return await message.answer("Неверный формат даты! Используйте ДД.ММ.ГГГГ", reply_markup=kb.add_user_data)

    await state.update_data(birthday=message.text.replace(",", "."))
    data_state = await state.get_data()
    if not await db.db_check(data_state['last_name'], data_state['first_name']):
        await db.add_db(message.from_user.id, data_state['last_name'], data_state['first_name'], data_state['birthday'])
        await message.answer('Данные добавлены', reply_markup=kb.add_user_data)
    else:
        await message.answer('Такой запись уже есть', reply_markup=kb.add_user_data)
    await state.clear()


# Состояния FSM
class UserData(StatesGroup):
    waiting_height = State()
    waiting_age = State()
    waiting_gender = State()


# Словарь для временного хранения данных
user_data = {}


# Функция расчета веса (из предыдущего примера)
def calculate_ideal_weight(height_cm: float, age: int, gender: str, formula: str) -> str:
    height_inch = height_cm / 2.54

    if formula == 'brock':
        weight = (height_cm - (100 if gender == 'male' else 110)) * 1.15 + (age - 20) * 0.1
    elif formula == 'brock_simple':
        weight = height_cm - (100 if gender == 'male' else 110)
    elif formula == 'lorentz':
        weight = (height_cm - 100) - (height_cm - 150) / (4 if gender == 'male' else 2)
    elif formula == 'cooper':
        weight = (height_cm * (4.0 if gender == 'male' else 3.5) / 2.54 - (128 if gender == 'male' else 108)) * 0.453
    elif formula == 'devine':
        weight = (50 if gender == 'male' else 45.5) + 2.3 * (height_inch - 60)
    elif formula == 'bmi':
        bmi_ranges = {
            (19, 24): (19, 24), (25, 34): (20, 25),
            (35, 44): (21, 26), (45, 54): (22, 27),
            (55, 64): (23, 28)
        }
        age_range = next((k for k in bmi_ranges if k[0] <= age <= k[1]), (20, 25))
        bmi_min, bmi_max = bmi_ranges.get(age_range, (20, 25))
        min_weight = bmi_min * (height_cm / 100) ** 2
        max_weight = bmi_max * (height_cm / 100) ** 2
        return f"Диапазон: {round(min_weight, 1)}–{round(max_weight, 1)} кг (ИМТ {bmi_min}–{bmi_max})"
    else:
        return "Ошибка: неизвестная формула."

    return f"Идеальный вес: {round(weight, 1)} кг"


# Клавиатура с формулами
def get_formulas_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Брока (с возрастом)", callback_data="brock")],
        [InlineKeyboardButton(text="Брока (упрощенная)", callback_data="brock_simple")],
        [InlineKeyboardButton(text="Лоренца", callback_data="lorentz")],
        [InlineKeyboardButton(text="Купера", callback_data="cooper")],
        [InlineKeyboardButton(text="Девина", callback_data="devine")],
        [InlineKeyboardButton(text="ИМТ (диапазон)", callback_data="bmi")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == '⚖️Идеальный вес')
async def body_start(message: Message, state: FSMContext):
    await message.answer("👋 Привет! Давай рассчитаем твой идеальный вес.\nВведи свой рост в см:")
    await state.set_state(UserData.waiting_height)


# Обработка роста
@router.message(UserData.waiting_height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
        if not 100 <= height <= 250:
            await message.answer("Рост должен быть от 100 до 250 см. Попробуй еще раз!")
            return
        await state.update_data(height=height)
        await message.answer("Теперь введи свой возраст:")
        await state.set_state(UserData.waiting_age)
    except ValueError:
        await message.answer("Нужно ввести число (например, 175).")


# Обработка возраста
@router.message(UserData.waiting_age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if not 10 <= age <= 120:
            await message.answer("Возраст должен быть от 10 до 120 лет. Попробуй еще раз!")
            return
        await state.update_data(age=age)

        # Клавиатура для выбора пола
        gender_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Мужской", callback_data="male")],
            [InlineKeyboardButton(text="Женский", callback_data="female")]
        ])
        await message.answer("Выбери пол:", reply_markup=gender_kb)
        await state.set_state(UserData.waiting_gender)
    except ValueError:
        await message.answer("Нужно ввести целое число (например, 30).")


# Обработка пола
@router.callback_query(UserData.waiting_gender, F.data.in_(["male", "female"]))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    gender = callback.data
    await state.update_data(gender=gender)
    data = await state.get_data()

    # Сохраняем данные пользователя
    user_data[callback.from_user.id] = data

    await callback.message.answer(
        "✅ Данные сохранены!\n"
        f"Рост: {data['height']} см\n"
        f"Возраст: {data['age']} лет\n"
        f"Пол: {'мужской' if gender == 'male' else 'женский'}\n\n"
        "Выбери формулу для расчета:",
        reply_markup=get_formulas_keyboard()
    )
    await state.clear()
    await callback.answer()


# Обработка выбора формулы
@router.callback_query(F.data.in_(["brock", "brock_simple", "lorentz", "cooper", "devine", "bmi"]))
async def process_formula(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        await callback.message.answer("❌ Данные устарели. Начни заново с /start")
        return

    data = user_data[user_id]
    result = calculate_ideal_weight(
        height_cm=data['height'],
        age=data['age'],
        gender=data['gender'],
        formula=callback.data
    )

    await callback.message.answer(
        f"📊 Результат по формуле {callback.data}:\n{result}",
        reply_markup=get_formulas_keyboard()  # Можно пересчитать
    )
    await callback.answer()


@router.message(F.text == '33')
async def file_open(message: Message):
    with open("DATA/33.txt", "r") as file:
        f = file.read()
        await message.answer(f"{f}")


@router.message(F.text.lower() == 'log')
async def file_open_logo(message: Message):
    with open("DATA/logs.log", "r") as file:
        f = file.read()[-3000:]
        await message.answer(f"{f}")
