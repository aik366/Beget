from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

# Главное меню бота
add_user_data = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🆕Добавить данные'), KeyboardButton(text='👁️Просмотр данных')],
    [KeyboardButton(text='🗑️Удалить данные'), KeyboardButton(text='✏️Редактировать')],
    [KeyboardButton(text='✨Пожелания'), KeyboardButton(text='🥂Тост'), KeyboardButton(text='🎁Открытки')],
    [KeyboardButton(text='😂Анекдот дня'), KeyboardButton(text='💲Курсы валют'), KeyboardButton(text='🌦️Погода')],
    [KeyboardButton(text='📝Заметки'), KeyboardButton(text='⚖️Идеальный вес')],
], resize_keyboard=True)

# Админ панель
admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🗑️Удалить по ID'), KeyboardButton(text='Удалить данные')],
    [KeyboardButton(text='Данные по ID'), KeyboardButton(text='❌Отмена')],
    [KeyboardButton(text='Объявление'), KeyboardButton(text='Картинка')]
], resize_keyboard=True)

# Редактирование данных (Фамилия, Имя, Дата)
edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фамилия', callback_data='surname'),
     InlineKeyboardButton(text='Имя', callback_data='name'),
     InlineKeyboardButton(text='Дата', callback_data='date')],
    [InlineKeyboardButton(text='❌Отмена', callback_data='cancel')],
], resize_keyboard=True)

# --- ИСПРАВЛЕНО: Добавлена кнопка "🔙 К списку" ---
edit_note = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✏️Редактировать', callback_data='note_edit'),
     InlineKeyboardButton(text='🗑️Удалить', callback_data='note_delete')],
], resize_keyboard=True)

# Подтверждение удаления
delete = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗑️Удалить', callback_data='delete'),
     InlineKeyboardButton(text='❌Отмена', callback_data='cancel')],
], resize_keyboard=True)

# Подтверждение удаления заметки
note_delete = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗑️Удалить', callback_data='delete_note'),
     InlineKeyboardButton(text='❌Отмена', callback_data='cancel_note')],
], resize_keyboard=True)

# Выбор что редактировать в заметке (Имя или Текст)
note_edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Имя заметки', callback_data='edit_name'),
     InlineKeyboardButton(text='Текст заметки', callback_data='edit_text')],
], resize_keyboard=True)

# Выбор режима редактирования текста (Добавить или Новый)
note_edit_content = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_text'),
     InlineKeyboardButton(text='Новый', callback_data='new_text')],
], resize_keyboard=True)

# Кнопка отмены
cancel_one = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌Отмена', callback_data='cancel')],
], resize_keyboard=True)

# Просмотр дней рождений
view_birthday = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Даты рождения', callback_data='birthday')],
], resize_keyboard=True)

# Меню внутри раздела Заметки
note_list = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📝Добавить заметку"), KeyboardButton(text="📋Мои заметки")],
    [KeyboardButton(text="🏠Главное меню"), KeyboardButton(text="❌Отмена")]
], resize_keyboard=True)