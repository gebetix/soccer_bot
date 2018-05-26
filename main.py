# -*- coding: utf-8 -*-
import boto3

from config import telegram_token, next_game_date, place, place_location
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import TelegramError


class S3(object):
    def __init__(self, service_name='s3', endpoint_url='https://storage.api.cloud.yandex.net'):
        self.client = boto3.session.Session().client(
            service_name=service_name,
            endpoint_url=endpoint_url
        )


class Game(object):
    def __init__(self, date, place):
        self.date = date
        self.place = place

    def add_player(self, username):
        s3 = S3()
        key = 'games/' + self.date + '/' + username
        try:
             s3.client.get_object(Bucket='soccer-storage', Key=key)
             message = 'Рад твоему рвению, но записаться можно только один раз.'
        except:
             s3.client.put_object(Bucket='soccer-storage', Key=key)
             message = 'Отлично! Я внёс тебя в состав на игру.'
        return message

    def del_player(self, username):
        s3 = S3()
        key = 'games/' + self.date + '/' + username
        try:
             s3.client.get_object(Bucket='soccer-storage', Key=key)
             s3.client.delete_object(Bucket='soccer-storage', Key=key)
             message = 'С глубоким сожалением вычёркиваю тебя из состава на игру.'
        except:
             message = 'Убрать из состава не могу – тебя в нём и так не было.'
        return message

def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Здравствуй, товарищ! Меня зовут Лев Яшин. Приглашаю тебя сыграть в футбол " + next_game_date + " в 21:00. Играть будем " + place + ". Жду тебя!"
    )


def add_me(bot, update):
    game = Game(next_game_date, place)
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    bot.sendMessage(chat_id=chat_id, text=game.add_player(username))


def del_me(bot, update):
    game = Game(next_game_date, place)
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    bot.sendMessage(chat_id=chat_id, text=game.del_player(username))


def location(bot, update):
    chat_id = update.message.chat_id
    bot.sendLocation(chat_id=chat_id, latitude=place_location['lat'], longitude=place_location['lon'])


updater = Updater(token=telegram_token)

start_handler = CommandHandler('start', start)
add_me_handler = CommandHandler('add_me', add_me)
del_me_handler = CommandHandler('del_me', del_me)
location_handler = CommandHandler('location', location)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(add_me_handler)
updater.dispatcher.add_handler(del_me_handler)
updater.dispatcher.add_handler(location_handler)

updater.start_polling()
