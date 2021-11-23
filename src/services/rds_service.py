import pymysql
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class RDSService:
    _instance = None

    def __init__(self):
        self.mysql_connection = self._get_connection()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print('Using the existing instance for RDSService class.')
        return cls._instance

    def _get_connection(self) -> pymysql.Connection:
        try:
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
            raise RuntimeError(f'Error while trying to connect MYSQL: {e}')

    def insert_into_stage(self, table_name: str, insert_fields: str, values: str) -> None:
        try:
            print(f'Executing insert command in {table_name} table.')
            sql_query = (
                    f'insert into stage.{table_name} {insert_fields} ' +
                    f"values {values};"
            )
            with self.mysql_connection.cursor() as cursor:
                cursor.execute(query=sql_query)
            self.mysql_connection.commit()
        except Exception as e:
            raise RuntimeError(f'Error while executing command: {e}.')

    def delete_from_stage(self, table_name: str, where_condition: str) -> None:
        try:
            print(f'Executing delete command in {table_name} table.')
            sql_query = f"delete from stage.{table_name} where {where_condition};"
            print(sql_query)
            with self.mysql_connection.cursor() as cursor:
                cursor.execute(query=sql_query)
            self.mysql_connection.commit()
        except Exception as e:
            raise RuntimeError(f'Error while trying to execute delete command in {table_name}: {e}')
