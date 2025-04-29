from telebot import types
import emoji


def create_keybord(*keys, row_width=2, resize_keyboard=True):

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keys = map(emoji.emojize, keys)
    buttuns = map(types.KeyboardButton, keys)
    markup.add(*buttuns)
    return markup


def create_inline_keyboard(*keys, row_width=2):
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    keys = map(emoji.emojize, keys)
    buttons = [types.InlineKeyboardButton(text=key, callback_data=key) for key in keys]

    markup.add(*buttons)
    return markup