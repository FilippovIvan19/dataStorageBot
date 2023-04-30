from telebot.types import ReplyKeyboardMarkup

from dataStorageBot.utils.constants import CREATE_SUBDIR_BTN_TEXT


def get_dir_reply_keyboard() -> ReplyKeyboardMarkup:
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_keyboard.row(CREATE_SUBDIR_BTN_TEXT)
    return reply_keyboard
