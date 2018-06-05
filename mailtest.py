from flask_mail import Mail, Message
from app import app, db
from datetime import datetime, timedelta
import time
from pytz import timezone
from decimal import Decimal
from models import Ticker, RawData


def main():
    with app.app_context():
        mails_accounts_count = len(app.config['MAILS_ACCOUNTS'])
        print (mails_accounts_count)
        counter = 0
        while counter < mails_accounts_count:
            print (app.config['MAILS_ACCOUNTS'][counter])
            counter += 1

        mail = Mail(app)
        msg = Message("Testing ", sender="coinsbot1@mail.ru", recipients=["e.sergeev@inbox.ru"])
        msg.body = "Sending automated results from tracker"
        print (msg)
#        mail.send(msg)

if __name__ == '__main__':
    main()