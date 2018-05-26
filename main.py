# -*- coding: utf-8 -*-

from config import config
from s3 import S3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import TelegramError


class Game(object):
    def __init__(self, date, place):
        self.date = date
        self.place = place

    def add_player(self, username, chat_id):
        s3 = S3()
        key = 'games/' + self.date + '/' + username
        try:
             s3.client.get_object(Bucket='soccer-storage', Key=key)
             message = 'Рад твоему рвению, но записаться можно только один раз.'
        except:
             s3.client.put_object(Bucket='soccer-storage', Key=key, Body=chat_id)
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
        text="Здравствуй, товарищ! Меня зовут Лев Яшин. Приглашаю тебя сыграть в футбол " + config['next_game_date'] + " в 21:00. Играть будем " + config['place'] + ". Жду тебя!"
    )


def add_me(bot, update):
    game = Game(config['next_game_date'], config['place'])
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    bot.sendMessage(chat_id=chat_id, text=game.add_player(username, chat_id))


def del_me(bot, update):
    game = Game(config['next_game_date'], config['place'])
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    bot.sendMessage(chat_id=chat_id, text=game.del_player(username))


def location(bot, update):
    chat_id = update.message.chat_id
    place_location = config['place_location']
    bot.sendLocation(chat_id=chat_id, latitude=place_location['lat'], longitude=place_location['lon'])


updater = Updater(token=config['token'])

start_handler = CommandHandler('start', start)
add_me_handler = CommandHandler('add_me', add_me)
del_me_handler = CommandHandler('del_me', del_me)
location_handler = CommandHandler('location', location)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(add_me_handler)
updater.dispatcher.add_handler(del_me_handler)
updater.dispatcher.add_handler(location_handler)

updater.start_polling()
