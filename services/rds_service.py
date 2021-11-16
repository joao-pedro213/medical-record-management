import pymysql
from dotenv import dotenv_values

secrets = dotenv_values('.env')
rds_host = secrets.get('RDS_HOST')
username = secrets.get('RDS_USERNAME')
password = secrets.get('RDS_PASSWORD')
database = secrets.get('DATABASE_NAME')
port =  secrets.get('PORT')

def set_rds_connection():
  try:
    print('Trying to connect do MYSQL server.')
    connection = pymysql.connect(
      host=rds_host,
      user=username,
      passwd=password,
      db=database,
      connect_timeout=5,
      cursorclass=pymysql.cursors.DictCursor
    )
    print('Connection established with success.')
    return connection
  except Exception as e:
    raise RuntimeError(f'Error while tring to connect MYSQL: {e}')