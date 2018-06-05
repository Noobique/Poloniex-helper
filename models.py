from app import db


class Ticker(db.Model):
    __tablename__ = 'tickers'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(10), primary_key = True)
    tradethiscoin = db.Column(db.Integer, default = 0, primary_key = True)
    support = db.Column(db.Float, default = 0)
    resistance = db.Column(db.Float, default = 0)

    def __init__(self, name, tradethiscoin, support, resistance):
        self.name = name
        self.tradethiscoin = tradethiscoin
        self.support = support
        self.resistance = resistance


class RawData(db.Model):
    __tablename__ = 'raw_data'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tme = db.Column(db.DateTime, primary_key = True)
    ticker_id = db.Column(db.Integer, db.ForeignKey('tickers.id'), primary_key = True)
    ticker = db.relationship("Ticker", backref=db.backref("tickers", uselist=False))
    baseVolume = db.Column(db.Float, default = 0)
    quoteVolume = db.Column(db.Float, default = 0)
    lowestAsk = db.Column(db.Float, default = 0)
    highestBid = db.Column(db.Float, default = 0)
    percentChange = db.Column(db.Float, default = 0)

    def __init__(self, tme, ticker, baseVolume, quoteVolume, lowestAsk, highestBid, percentChange):
        self.tme = tme
        self.ticker_id = ticker
        self.baseVolume = baseVolume
        self.quoteVolume = quoteVolume
        self.lowestAsk = lowestAsk
        self.highestBid = highestBid
        self.percentChange = percentChange


class RawDataMarket(db.Model):
    __tablename__ = 'raw_data_market'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    rawdata_id = db.Column(db.Integer, db.ForeignKey('raw_data.id'))
    rawdata = db.relationship("RawData", backref=db.backref("raw_data", uselist=False))
    market_ask_price = db.Column(db.Float, default = 0)
    market_ask_volume = db.Column(db.Float, default = 0)
    market_bid_price = db.Column(db.Float, default = 0)
    market_bid_volume = db.Column(db.Float, default = 0)

    def __init__(self, rawdata, market_ask_price, market_ask_volume, market_bid_price, market_bid_volume):
        self.rawdata_id = rawdata
        self.market_ask_price = market_ask_price
        self.market_ask_volume = market_ask_volume
        self.market_bid_price = market_bid_price
        self.market_bid_volume = market_bid_volume
