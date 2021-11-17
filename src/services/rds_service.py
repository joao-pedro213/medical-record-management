import pymysql

def set_rds_connection():
  try:
    print('Trying to connect do MYSQL server.')
    connection = pymysql.connect(
      host='mysqlserver.cacesswihlex.us-east-1.rds.amazonaws.com',
      user='admin',
      passwd='admin1980',
      db='stage',
      connect_timeout=5,
      cursorclass=pymysql.cursors.DictCursor
    )
    print('Connection established with success.')
    return connection
  except Exception as e:
    raise RuntimeError(f'Error while tring to connect MYSQL: {e}')
