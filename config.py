DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'polo'
DB_USER = 'root'
DB_PASSWORD = 'root'

SERVER_NAME = '127.0.0.1:5555'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME

POLONIEX_TICKER = 'https://poloniex.com/public?command=returnTicker'
POLONIEX_MARKET = 'https://poloniex.com/public?command=returnOrderBook&currencyPair=all&depth=100'

POLONIEX_KEY = ''
POLONIEX_SECRET = ''

TIMEDIFF = 0

MINVOLUME = 30

USD_BTC_TICKER = "USDT_BTC",

MAIL_SERVER = 'smtp.mail.ru'

MAIL_PORT =  465

MAIL_USE_SSL = True

MAILS_ACCOUNTS = (
                  {
                   'login' : 'coinsbot1',
                   'password' : 'pass1'
                  },
                  {
                   'login' : 'coinsbot2',
                   'password' : 'pass2'
                  }
                 )