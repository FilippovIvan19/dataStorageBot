from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot

from dataStorage import settings
from dataStorageBot.models import Directories
from dataStorageBot.utils.data_helper import get_or_create_user


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
    user = get_or_create_user(message.from_user.id)

    try:
        root = Directories.objects.get(title='root', user_id=user, parent=None)
        bot.send_message(message.chat.id, "You already have root directory")
    except Directories.DoesNotExist:
        root = Directories(title='root', user_id=user, parent=None)
        root.save()
        bot.send_message(message.chat.id, "Root directory for you was created")

    bot.send_message(message.chat.id, "Use /help to see bot usage prompts")


@bot.message_handler(commands=['root'])
def open_root(message: telebot.types.Message):
    bot.send_message(message.chat.id, "root")
