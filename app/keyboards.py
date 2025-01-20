from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

add_user_data = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🆕Добавить данные'),
                                               KeyboardButton(text='👁️Просмотр данных'), ],
                                              [KeyboardButton(text='🎁Открытки'),
                                              KeyboardButton(text='❌Отмена'), ],], resize_keyboard=True)


admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Данные по ID'),
                                       KeyboardButton(text='🗑️Удалить данные'), ],
                                      [KeyboardButton(text='❌Отмена')], ], resize_keyboard=True)


# catalog = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Футболки', callback_data='t-shirt')],
#     [InlineKeyboardButton(text='Кроссовки', callback_data='sneakers')],
#     [InlineKeyboardButton(text='Кепки', callback_data='cap')]])


# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
#                                                            request_contact=True)]],
#                                  resize_keyboard=True)
