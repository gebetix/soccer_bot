import boto3

class S3(object):
    def __init__(self, service_name='s3', endpoint_url='https://storage.api.cloud.yandex.net'):
        self.client = boto3.session.Session().client(
            service_name=service_name,
            endpoint_url=endpoint_url
        )
