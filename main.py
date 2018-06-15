# -*- coding: utf-8 -*-
import logging
import datetime

from config import config
from game import Game
from telegram.ext import Updater, RegexHandler, CommandHandler
from telegram import ReplyKeyboardMarkup

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("soccer_bot/logs/debug.log"),
    ])

reply_markup = ReplyKeyboardMarkup([
        ['Записаться', 'Отменить запись'],
        ['Где играем?', 'Кто играет?', 'Инфо']
    ])

money_info = "Сбер/Рокет/Райф +79090162390"

max_players_text = "Состав уже укомплектован, но не расстраивайся! Будет следующая игра, а возможно кто-то отпишется от этой."

def game_info():
    return config['next_game_date'] + " в " + config['next_game_time'] + ". Играть будем " + config['place'] + "."


def main():
    def start(bot, update):
        invite_msg = "Приглашаю тебя сыграть в футбол " + game_info() + "\nЖду тебя!"
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Здравствуй, товарищ!\nМеня зовут Лев Яшин. " + invite_msg,
            reply_markup=reply_markup
        )

    def info(bot, update):
        info_msg = "Следующая игра –– " + game_info() + "\nСдать 270 рублей безналом –– " + money_info + "\n" + "\nЕсли остались вопросы или есть фидбэк –– @gebetix"
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=info_msg,
            reply_markup=reply_markup
        )

    def add_me(bot, update):
        game = Game(config['next_game_date'], config['place'])
        players = game.get_players()
        if len(players) > 10:
            bot.sendMessage(chat_id=chat_id, text=max_players_text)
            return
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
        message = '' if players else "Никто пока не записался. Ты будешь первым!"
        for i, player in enumerate(players):
            message += str(i+1) + '. @' + player + '\n'
        bot.sendMessage(chat_id=chat_id, text=message)

    def push_everyweek(bot, job):
        chat_ids = job.context
        for chat_id in chat_ids:
            bot.sendMessage(
                chat_id=chat_id,.
                text="Пора записываться на следующую игру!",
                reply_markup=reply_markup
            )

    updater = Updater(token=config['token'])
    job_queue = updater.job_queue
    job_queue.run_daily(push_everyweek, days=(3,), time=datetime.time(13, 00), context=config['yandex_chat_ids'])
    job_queue.run_daily(push_everyweek, days=(4,), time=datetime.time(13, 00), context=config['outer_chat_ids'])

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
