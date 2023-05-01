from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from dataStorageBot.utils.constants import *


def get_dir_reply_keyboard() -> ReplyKeyboardMarkup:
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_keyboard.row(CREATE_SUBDIR_BTN_TEXT)
    reply_keyboard.row(UPLOAD_FILE_BTN_TEXT)
    return reply_keyboard


def get_dir_inline_keyboard(cur_dir) -> InlineKeyboardMarkup:
    parent_dir = cur_dir.parent or cur_dir
    subdirs = cur_dir.subdirs.all()
    files = cur_dir.files_set.all()

    inline_keyboard = InlineKeyboardMarkup()

    for file in sorted(files, reverse=True, key=lambda f: f.title):
        data = '_'.join((DIRECTORY_VIEW_SCOPE, FILE_OPEN_OPTION, str(file.id)))
        inline_keyboard.row(
            InlineKeyboardButton(file.get_title_with_emoji(), callback_data=data))

    for directory in sorted(subdirs, reverse=True, key=lambda d: d.title):
        data = '_'.join((DIRECTORY_VIEW_SCOPE, NAVIGATION_OPTION, str(directory.id)))
        inline_keyboard.row(
            InlineKeyboardButton(directory.get_title_with_emoji(), callback_data=data))

    parent_data = '_'.join((DIRECTORY_VIEW_SCOPE, NAVIGATION_OPTION, str(parent_dir.id)))
    inline_keyboard.row(
        InlineKeyboardButton(DIRECTORY_EMOJI + '..', callback_data=parent_data))

    return inline_keyboard
