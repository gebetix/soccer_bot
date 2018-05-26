from s3 import S3
import json


class Config(object):
    def __getitem__(self, item):
        s3 = S3()
        data = json.loads(
            str(
                s3.client.get_object(
                    Bucket='soccer-storage', Key='config.json'
                )['Body'].read(),
                'utf-8'
            )
        )
        return data[item]

config = Config()
