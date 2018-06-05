from app import app, db
import time
from datetime import datetime
from decimal import Decimal
from pytz import timezone
from urllib.request import Request, urlopen
import json
from models import *


fmt = "%Y-%m-%d %H:%M:"
fmtsec = "%S"


if __name__ == "__main__":
    for nowtme in range(6):
        now_utc = datetime.now(timezone('UTC'))
        tme = now_utc.strftime(fmt)
        tmesec = int(now_utc.strftime(fmtsec))//10
        tme = tme + str(tmesec) + "0"

#        market = json.loads(urlopen(Request(app.config['POLONIEX_MARKET'])).read().decode())
        currences = json.loads(urlopen(Request(app.config['POLONIEX_TICKER'])).read().decode())

        for cur, value in currences.items():
            tick = Ticker.query.filter(Ticker.name == cur).first()
            print (cur, tme)
            if not tick:
                tck = Ticker(cur, 0, 0, 0)
                db.session.add(tck)
                db.session.commit()

            if tick.tradethiscoin == 1:
                avg = (float(value['lowestAsk']) + float(value['highestBid']))/2
                raw = RawData(tme, tick.id, float(value['baseVolume']), float(value['quoteVolume']), float(value['lowestAsk']), float(value['highestBid']), avg, float(value['percentChange']))
                db.session.add(raw)
                db.session.commit()

#                coinmarket = market[cur]

#                coinmarket_asks = coinmarket['asks']
#                for current_ask in coinmarket_asks:
#                    raw_market = RawDataMarket(raw.id, round(Decimal(current_ask[0]), 7), round(Decimal(current_ask[1]), 3), 0, 0)
#                    db.session.add(raw_market)

#                coinmarket_bids = coinmarket['bids']
#                for current_bid in coinmarket_bids:
#                    raw_market = RawDataMarket(raw.id, 0, 0, round(Decimal(current_bid[0]), 7), round(Decimal(current_bid[1]), 3))
#                    db.session.add(raw_market)

#                db.session.commit()

        time.sleep(10)