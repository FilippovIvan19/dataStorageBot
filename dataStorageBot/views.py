import traceback

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot.types import ReplyKeyboardRemove, CallbackQuery

from dataStorage import settings
from dataStorageBot.models import Directories, Files, Tags
from dataStorageBot.utils.constants import *
from dataStorageBot.utils.data_helper import check_root_exists, get_user, \
    create_sub_directory, get_full_path, create_file, get_send_file_func, get_tags_info, \
    create_tag, get_file_tags_info
from dataStorageBot.utils.message_helper import get_dir_reply_keyboard, \
    get_dir_inline_keyboard, get_file_inline_keyboard, get_tag_inline_keyboard, \
    get_file_tag_inline_keyboard, get_file_add_tag_inline_keyboard, \
    get_file_delete_tag_inline_keyboard


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
    user._current_dir = None
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
    bot.send_message(message.chat.id, "Currently existing tags:",
                     reply_markup=ReplyKeyboardRemove())
    user = get_user(message.from_user.id)
    draw_tags(message.chat.id, user)


@bot.message_handler(regexp=CREATE_SUBDIR_BTN_TEXT)
def create_subdir(message: telebot.types.Message):
    msg = bot.send_message(message.chat.id, "Please, choose name for new directory",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_subdir_name)


def process_subdir_name(message: telebot.types.Message):
    user = get_user(message.from_user.id)
    create_sub_directory(user=user, title=message.text)
    bot.send_message(message.chat.id, f"Directory \"{message.text}\" was created",
                     reply_markup=get_dir_reply_keyboard())
    draw_directory(message.chat.id, user)


@bot.message_handler(regexp=UPLOAD_FILE_BTN_TEXT)
def upload_file(message: telebot.types.Message):
    msg = bot.send_message(message.chat.id,
                           "Please, send your file with desired name in message text",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_uploaded_file)


def process_uploaded_file(message: telebot.types.Message):
    created = create_file(message)
    if created:
        text = f"File \"{message.caption}\" was uploaded"
    else:
        text = f"File \"{message.caption}\" was NOT uploaded, " \
               f"probably because of unsupported type"

    bot.send_message(message.chat.id, text, reply_markup=get_dir_reply_keyboard())
    user = get_user(message.from_user.id)
    draw_directory(message.chat.id, user)


def draw_directory(chat_id, user):
    cur_dir = user.get_current_dir()
    full_path = get_full_path(cur_dir)
    bot.send_message(chat_id, full_path, parse_mode='Markdown',
                     reply_markup=get_dir_inline_keyboard(cur_dir))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    scope, option, obj_id = call.data.split('_', maxsplit=2)
    user = get_user(call.from_user.id)

    if option == NAVIGATION_OPTION and scope in (DIRECTORY_VIEW_SCOPE, FILE_VIEW_SCOPE):
        next_dir = Directories.objects.get(id=obj_id, user=user)
        user._current_dir = next_dir
        user.save()
        draw_directory(call.message.chat.id, user)
        return

    if scope == DIRECTORY_VIEW_SCOPE and option == FILE_OPEN_OPTION:
        file = Files.objects.get(id=obj_id, user=user)
        draw_file(call.message.chat.id, file)
        return

    if scope == TAG_VIEW_SCOPE:
        if option == ADD_OPTION:
            msg = bot.send_message(call.message.chat.id,
                                   "Please, choose name for new tag")
            bot.register_next_step_handler(msg, process_new_tag_name)
        else:
            bot.send_message(call.message.chat.id, 'coming soon')
        return

    if scope == FILE_VIEW_SCOPE:
        if option == ADD_OPTION:
            file = Files.objects.get(id=obj_id, user=user)
            file_tags = file.tags.all()
            user_tags = Tags.objects.filter(user=file.user)
            tags = user_tags.difference(file_tags)
            bot.send_message(call.message.chat.id, "Please, choose tag to attach",
                             reply_markup=get_file_add_tag_inline_keyboard(file, tags))
        elif option == DELETE_OPTION:
            file = Files.objects.get(id=obj_id, user=user)
            tags = file.tags.all()
            bot.send_message(call.message.chat.id, "Please, choose tag to detach",
                             reply_markup=get_file_delete_tag_inline_keyboard(file, tags))
        elif option == ATTACH_OPTION:
            obj_id = obj_id.split('_')
            file = Files.objects.get(id=obj_id[0], user=user)
            tag = Tags.objects.get(id=obj_id[1], user=user)
            file.tags.add(tag)
            file.save()
            draw_file(call.message.chat.id, file)
        elif option == DETACH_OPTION:
            obj_id = obj_id.split('_')
            file = Files.objects.get(id=obj_id[0], user=user)
            tag = Tags.objects.get(id=obj_id[1], user=user)
            file.tags.remove(tag)
            file.save()
            draw_file(call.message.chat.id, file)


def draw_file(chat_id, file):
    draw_file_tags(chat_id, file)
    send_file_func = getattr(bot, get_send_file_func(file.content_type))
    send_file_func(chat_id, file.tg_file_id, caption=file.title,
                   reply_markup=get_file_inline_keyboard(file))


def draw_tags(chat_id, user):
    tags_info = get_tags_info(user)
    bot.send_message(chat_id, tags_info, reply_markup=get_tag_inline_keyboard())


def draw_file_tags(chat_id, file):
    tags_info = get_file_tags_info(file)
    bot.send_message(chat_id, tags_info, reply_markup=get_file_tag_inline_keyboard(file))


def process_new_tag_name(message: telebot.types.Message):
    user = get_user(message.from_user.id)
    create_tag(user=user, title=message.text)
    bot.send_message(message.chat.id, f"Tag \"{message.text}\" was created")
    draw_tags(message.chat.id, user)
