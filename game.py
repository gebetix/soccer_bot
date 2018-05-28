from s3 import S3

class Game(object):
    def __init__(self, date, place):
        self.date = date
        self.place = place

    def get_players(self):
        s3 = S3()
        key = 'games/' + self.date + '/'
        players = []
        player_objects = s3.client.list_objects(Bucket='soccer-storage', Prefix=key).get('Contents')
        if player_objects:
            for obj in player_objects:
                players.append(obj['Key'].split('/')[-1])
        return players

    def add_player(self, username, chat_id):
        s3 = S3()
        key = 'games/' + self.date + '/' + username
        try:
            s3.client.get_object(Bucket='soccer-storage', Key=key)
            message = 'Рад твоему рвению, но записаться можно только один раз.'
        except:
            s3.client.put_object(Bucket='soccer-storage', Key=key, Body=str(chat_id))
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
