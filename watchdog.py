from app import app, db
from flask_mail import Mail, Message
from models import Ticker, RawData
from datetime import datetime, timedelta
import time
from pytz import timezone
from decimal import Decimal

#return average price chenge for a last periods
def returncoinpricedelta(tickid, basetme):
    minutesperiod = 5
    depthofpricedeltasearch = 100
    summeddelta = 0
                    
    for nowtme in range(0, depthofpricedeltasearch):
        tmeend = datetime.strptime(str(basetme), '%Y-%m-%d %H:%M:%S') - timedelta(minutes=minutesperiod*(nowtme+1)) 
        tmestart = datetime.strptime(str(basetme), '%Y-%m-%d %H:%M:%S') - timedelta(minutes=minutesperiod*nowtme) 
        maxpricerow = RawData.query.filter(RawData.ticker_id == tickid).filter(RawData.tme < tmestart).filter(RawData.tme > tmeend).order_by(RawData.highestBid.desc()).first()
        minpricerow = RawData.query.filter(RawData.ticker_id == tickid).filter(RawData.tme < tmestart).filter(RawData.tme > tmeend).order_by(RawData.lowestAsk.asc()).first()
        #remove intervals with zero grow
        if maxpricerow and minpricerow:
            if maxpricerow.average != minpricerow.average:
                 summeddelta = summeddelta + maxpricerow.average - minpricerow.average
            else:
                depthofpricedeltasearch -= 1
        else:
                depthofpricedeltasearch -= 1

    return summeddelta / depthofpricedeltasearch

def main():
    print('Started')
    fmt = "%Y-%m-%d %H:%M:%SS"
    oldtme = "0000-00-00 00:00:00"

    mail_account_counter = 0

    while True:
        db.session.commit()
        with app.app_context():
            for tick in Ticker.query.filter(Ticker.tradethiscoin == 1).order_by(Ticker.name):

                raw = RawData.query.filter(RawData.ticker_id == tick.id).order_by(RawData.id.desc()).first()
                if raw:
                    average = (Decimal(raw.lowestAsk) + Decimal(raw.highestBid)) / 2
                    messageUp = messageDown = grow = None

                    if raw.baseVolume >= app.config['MINVOLUME']:
                        if tick.resistance > 0:
                            if Decimal(average) > Decimal(tick.resistance):
                                delta = returncoinpricedelta(tick.id, raw.tme)
                                grow = Decimal(average) - Decimal(tick.resistance)
                                procgrow = Decimal(grow / Decimal(tick.resistance) * 100)
                                messageUp = tick.name + ": " + str('{:.9f}'.format(average)) + ". UP. % " + str('{:.3f}'.format(procgrow)) + " Time: " + str(raw.tme)
                                newresistance = average + Decimal(delta)
                                newsupport = average - Decimal(delta * 2)
                                print(messageUp)

                        if tick.support > 0:
                           if Decimal(average) < Decimal(tick.support):
                                delta = returncoinpricedelta(tick.id, raw.tme)
                                messageDown = tick.name + ": " + str('{:.9f}'.format(average)) + ". DOWN. Sup was " + str('{:.9f}'.format(tick.support)) + " Time: " + str(raw.tme)
                                newresistance = average + Decimal(delta * 2)
                                newsupport = average - Decimal(delta)
                                print(messageDown)

                    if messageUp and (grow*5 > delta):
                            mail_account = app.config['MAILS_ACCOUNTS'][mail_account_counter]
                            mail_account_counter += 1
                            if (mail_account_counter == len(app.config['MAILS_ACCOUNTS'])):
                                mail_account_counter = 0
                            app.config['MAIL_USERNAME'] = mail_account['login']
                            app.config['MAIL_PASSWORD'] = mail_account['password']
                            mail = Mail(app)
                            msg = Message(messageUp, sender=mail_account['login'], recipients=["e.sergeev@inbox.ru"])
                            msg.body = "Automated results from tracker:"
                            msg.body += "\nOld price: " + str('{:.9f}'.format(tick.resistance))
                            msg.body += "\nNew price: " + str('{:.9f}'.format(average))
                            msg.body += "\nPrice grow: " + str('{:.9f}'.format(grow))
                            msg.body += "\n% price grow: " + str('{:.9f}'.format(procgrow))
                            msg.body += "\nAverage 5 min delta: " + str('{:.9f}'.format(delta))
                            mail.send(msg)

                    if messageUp or messageDown:
                        db.session.query(Ticker).filter_by(id = tick.id).update({'support': newsupport, 'resistance': newresistance}) 
                        db.session.commit()
 
            print(raw.tme)
            time.sleep(60)

if __name__ == '__main__':
    main()