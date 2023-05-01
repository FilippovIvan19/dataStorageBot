import traceback

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot.types import ReplyKeyboardRemove, CallbackQuery

from dataStorage import settings
from dataStorageBot.models import Directories
from dataStorageBot.utils.constants import *
from dataStorageBot.utils.data_helper import check_root_exists, get_user, \
    create_sub_directory, get_full_path
from dataStorageBot.utils.message_helper import get_dir_reply_keyboard, \
    get_dir_inline_keyboard


def hello(request):
    return render(request, 'hello.html')


bot = telebot.TeleBot(settings.TG_TOKEN, threaded=False)
bot.set_webhook(url=settings.TG_WEBHOOK)
bot.set_my_commands(MY_COMMANDS)


@csrf_exempt
def webhook(request):
    if request.method == 'POST' and request.META['CONTENT_TYPE'] == 'application/json':
        try:
            json_data = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_data)
            bot.process_new_updates([update])
        except Exception as e:
            traceback.print_exc()
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


@bot.message_handler(commands=[HELP_COMMAND])
def open_root(message: telebot.types.Message):
    bot.send_message(message.chat.id, HELP_TEXT)


@bot.message_handler(commands=[ROOT_COMMAND])
def open_root(message: telebot.types.Message):
    user = get_user(message.from_user.id)
    user.current_dir = None
    user.save()
    bot.send_message(message.chat.id, f"Opening directory \"{ROOT_DIR_NAME}\"",
                     reply_markup=get_dir_reply_keyboard())
    draw_directory(message.chat.id, user)


@bot.message_handler(commands=[LAST_ACTIVE_DIR_COMMAND])
def open_last_active_dir(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'coming soon')


@bot.message_handler(commands=[SEARCH_COMMAND])
def search(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'coming soon')


@bot.message_handler(commands=[TAGS_COMMAND])
def show_tags(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'coming soon')


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
    draw_directory(message.chat.id, user)


def draw_directory(chat_id, user):
    cur_dir = user.get_current_dir()
    full_path = get_full_path(cur_dir)
    bot.send_message(chat_id, full_path, reply_markup=get_dir_inline_keyboard(cur_dir))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    scope, option, obj_id = call.data.split('_')
    user = get_user(call.from_user.id)
    if scope == DIRECTORY_VIEW_SCOPE:
        if option == NAVIGATION_OPTION:
            next_dir = Directories.objects.get(id=obj_id, user=user)
            user.current_dir = next_dir
            user.save()
            bot.answer_callback_query(call.id)
            draw_directory(call.message.chat.id, user)
