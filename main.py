# -*- coding: utf-8 -*-
import logging

from config import config
from game import Game
from telegram.ext import Updater, RegexHandler, CommandHandler
from telegram import ReplyKeyboardMarkup

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/debug.log"),
    ])

reply_markup = ReplyKeyboardMarkup([
        ['Записаться', 'Отменить запись'],
        ['Где играем?', 'Кто играет?', 'Инфо']
    ])

game_info = config['next_game_date'] + " в " + config['next_game_time'] + ". Играть будем " + config['place'] + "."

invite_msg = "Приглашаю тебя сыграть в футбол " + game_info + "\nЖду тебя!"

money_info = "Сбер/Рокет/Райф +79090162390"

info_msg = "Следующая игра –– " + game_info + "\nСдать деньги безналом –– " + money_info + "\n" + "\nЕсли остались вопросы или есть фидбэк –– @gebetix"

def main():
    def start(bot, update):
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Здравствуй, товарищ!\nМеня зовут Лев Яшин. " + invite_msg,
            reply_markup=reply_markup
        )

    def info(bot, update):
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=info_msg,
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

    def show_players(bot, update):
        game = Game(config['next_game_date'], config['place'])
        chat_id = update.message.chat_id
        players = game.get_players()
        message = ''
        for i, player in enumerate(players):
            message += str(i+1) + '. @' + player + '\n'
        bot.sendMessage(chat_id=chat_id, text=message)

    updater = Updater(token=config['token'])

    start_handler = CommandHandler('start', start)
    add_me_handler = RegexHandler('^Записаться$', add_me)
    del_me_handler = RegexHandler('^Отменить запись$', del_me)
    location_handler = RegexHandler('^Где играем\?$', location)
    show_players_handler = RegexHandler('^Кто играет\?$', show_players)
    info_handler = RegexHandler('^Инфо$', info)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(add_me_handler)
    updater.dispatcher.add_handler(del_me_handler)
    updater.dispatcher.add_handler(location_handler)
    updater.dispatcher.add_handler(show_players_handler)
    updater.dispatcher.add_handler(info_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
