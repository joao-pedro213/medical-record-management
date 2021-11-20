import pymysql
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class RDSService:
    def __init__(self):
        pass

    @staticmethod
    def get_connection() -> pymysql.Connection:
        try:
            print('Connecting to MYSQL server.')
            connection = pymysql.connect(
                host=os.environ.get('HOST'),
                user=os.environ.get('USER'),
                passwd=os.environ.get('PASSWORD'),
                db=os.environ.get('DATABASE_NAME'),
                connect_timeout=5,
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            raise RuntimeError(f'Error while tring to connect MYSQL: {e}')
