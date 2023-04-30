from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot.types import ReplyKeyboardRemove

from dataStorage import settings
from dataStorageBot.utils.constants import ROOT_DIR_NAME, CREATE_SUBDIR_BTN_TEXT
from dataStorageBot.utils.data_helper import check_root_exists, get_user, \
    create_sub_directory
from dataStorageBot.utils.message_helper import get_dir_reply_keyboard


def hello(request):
    return render(request, 'hello.html')


bot = telebot.TeleBot(settings.TG_TOKEN, threaded=False)
bot.set_webhook(url=settings.TG_WEBHOOK)


@csrf_exempt
def webhook(request):
    if request.method == 'POST' and request.META['CONTENT_TYPE'] == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied


@bot.message_handler(commands=['start'])
def greet(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        "Hello, I'm a bot for storing files in simulated file system with tags feature")
    if check_root_exists(message.from_user.id):
        bot.send_message(message.chat.id,
                         f"You already have \"{ROOT_DIR_NAME}\" directory")
    else:
        bot.send_message(message.chat.id,
                         f"Directory \"{ROOT_DIR_NAME}\" for you was created")
    bot.send_message(message.chat.id, "Use /help to see bot usage prompts")


@bot.message_handler(commands=['root'])
def open_root(message: telebot.types.Message):
    user = get_user(message.from_user.id)
    user.current_dir = None
    user.save()
    bot.send_message(message.chat.id, f"Opening directory \"{ROOT_DIR_NAME}\"",
                     reply_markup=get_dir_reply_keyboard())
    bot.send_message(message.chat.id, "dir visualization placeholder")


@bot.message_handler(regexp=CREATE_SUBDIR_BTN_TEXT)
def create_subdir(message: telebot.types.Message):
    msg = bot.send_message(message.chat.id, "Please, choose name for new directory",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_subdir_name)


def process_subdir_name(message: telebot.types.Message):
    user = get_user(message.from_user.id)
    create_sub_directory(user=user, name=message.text)
    bot.send_message(message.chat.id, f"Directory \"{message.text}\" was created",
                     reply_markup=get_dir_reply_keyboard())
    bot.send_message(message.chat.id, "dir visualization placeholder")

