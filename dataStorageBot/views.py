from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot

from dataStorage import settings


def hello(request):
    return render(request, 'hello.html')


bot = telebot.TeleBot(settings.TG_TOKEN, threaded=False)
bot.set_webhook(url=settings.TG_WEBHOOK)


@csrf_exempt
def webhook(request):
    print('qwerty')
    if request.method == 'POST' and request.META['CONTENT_TYPE'] == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied


@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, "Hello")
