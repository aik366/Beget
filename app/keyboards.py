from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

add_user_data = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🆕Добавить данные'),
                                               KeyboardButton(text='👁️Просмотр данных'), ],
                                              [KeyboardButton(text='🗑️Удалить данные'),
                                               KeyboardButton(text='✏️Редактировать')],
                                              [KeyboardButton(text='✨Пожелания'),
                                               KeyboardButton(text='🥂Тост'),
                                               KeyboardButton(text='🎁Открытки'), ],
                                              [KeyboardButton(text='😂Анекдот дня'),
                                               KeyboardButton(text='💲Курсы валют'),
                                               KeyboardButton(text='🌦️Погода'), ],
                                              [KeyboardButton(text='📝Заметки'),
                                               KeyboardButton(text='📝Мои заметки'), ], ], resize_keyboard=True)

admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🗑️Удалить по ID'),
                                       KeyboardButton(text='Удалить данные'), ],
                                      [KeyboardButton(text='Данные по ID'),
                                       KeyboardButton(text='❌Отмена')],
                                      [KeyboardButton(text='Объявление'),
                                       KeyboardButton(text='Картинка')]], resize_keyboard=True)

edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фамилия', callback_data='surname'),
     InlineKeyboardButton(text='Имя', callback_data='name'),
     InlineKeyboardButton(text='Дата', callback_data='date')],
    [InlineKeyboardButton(text='❌Отмена', callback_data='cancel')], ], resize_keyboard=True)

edit_note = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Просмотр', callback_data='note_view'),
     InlineKeyboardButton(text='Удалить', callback_data='note_delete'), ],
    [InlineKeyboardButton(text='Редактировать', callback_data='note_edit'),
     InlineKeyboardButton(text='❌Отмена', callback_data='cancel')], ], resize_keyboard=True)

delete = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗑️Удалить', callback_data='delete'),
     InlineKeyboardButton(text='❌Отмена', callback_data='cancel')], ], resize_keyboard=True)

note_delete = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗑️Удалить', callback_data='delete_note'),
     InlineKeyboardButton(text='❌Отмена', callback_data='cancel')], ], resize_keyboard=True)

note_edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Имя заметки', callback_data='edit_name'),
     InlineKeyboardButton(text='Текст заметки', callback_data='edit_text'),
     InlineKeyboardButton(text='❌Отмена', callback_data='cancel')], ], resize_keyboard=True)

cancel_one = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌Отмена', callback_data='cancel')], ], resize_keyboard=True)

view_birthday = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Даты рождения', callback_data='birthday')], ], resize_keyboard=True)

# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
#                                                            request_contact=True)]],
#                                  resize_keyboard=True)
