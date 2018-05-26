# -*- coding: utf-8 -*-
import logging

from config import config
from game import Game
from telegram.ext import Updater, RegexHandler, CommandHandler
from telegram import TelegramError, ReplyKeyboardMarkup

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


reply_markup = ReplyKeyboardMarkup([
        ['Записаться', 'Где играем?'],
        ['Отменить запись','Кто играет?']
    ])

def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Здравствуй, товарищ! Меня зовут Лев Яшин. Приглашаю тебя сыграть в футбол " + 
        config['next_game_date'] + " в 21:00. Играть будем " + 
        config['place'] + ". Жду тебя!",
        reply_markup=reply_markup
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
add_me_handler = RegexHandler('^Записаться$', add_me)
del_me_handler = RegexHandler('^Отменить запись$', del_me)
location_handler = RegexHandler('^Где играем\?$', location)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(add_me_handler)
updater.dispatcher.add_handler(del_me_handler)
updater.dispatcher.add_handler(location_handler)

updater.start_polling()
