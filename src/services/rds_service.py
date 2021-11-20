import pymysql


class RDSService:
    def __init__(self):
        pass

    @staticmethod
    def get_connection() -> pymysql.Connection:
        try:
            print('Connecting to MYSQL server.')
            connection = pymysql.connect(
                host='mrmgmt.cacesswihlex.us-east-1.rds.amazonaws.com',
                user='admin',
                passwd='admin1980',
                db='stage',
                connect_timeout=5,
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            raise RuntimeError(f'Error while tring to connect MYSQL: {e}')
