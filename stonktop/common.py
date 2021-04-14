import json
import pytz
import yfinance as yf
from pathlib import Path
from datetime import datetime
from random import randint


class Stock(object):
    def __init__(self, d: dict):
        super().__init__()

        self.company_name = d["COMPANY_NAME"]
        self.stock_ticker = d["STOCK_TICKER"]
        self.real_time_price = d["REAL_TIME_PRICE"]
        self.previous_close = d["PREVIOUS_CLOSE"]
        self.open = d["OPEN"]
        self.fifty_two_week_range = d["FIFTY_TWO_WEEK_RANGE"]
        self.volume = d["VOLUME"]
        self.average_volume = d["AVERAGE_VOLUME"]
        self.market_cap = d["MARKET_CAP"]
        self.pe_ratio = d["PE_RATIO"]
        self.state = d["STATE"]

    def __repr__(self):
        return f"{self.stock_ticker} - {self.company_name}"


class Portfolio(object):
    def __init__(self, config_path = Path.cwd().parent / 'tests/config.json'):
        super().__init__()
        self.config_path = config_path
        self.data = self._read_config()
        self.tickers = self.data.keys()
        self.stocks = self._get_stocks()


    def _read_config(self):
        with open(self.config_path, 'r') as fp:
            data = json.load(fp)
        
        return data

    def _get_stocks(self):
        stocks = []

        for ticker in self.tickers:
            # TODO: Replace random info with yfinance information
            if self.is_market_open():
                #TODO: Add error handling for tickers that don't exist
                yf_obj = yf.Ticker(ticker)
                temp = yf_obj.info
                stock = {
                    "COMPANY_NAME": temp['longName'],
                    "STOCK_TICKER": temp['symbol'],
                    "REAL_TIME_PRICE": str(yf_obj.history(period='1d')['Close'][0]),
                    "PREVIOUS_CLOSE": str(temp['previousClose']),
                    "OPEN": str(temp['open']),
                    "FIFTY_TWO_WEEK_RANGE": f"{temp['fiftyTwoWeekLow']}, {temp['fiftyTwoWeekHigh']}",
                    "VOLUME": str(temp['volume']), #TODO: fix to be live volume
                    "AVERAGE_VOLUME": str(temp['averageVolume']),
                    "MARKET_CAP": str(temp['marketCap']),
                    "PE_RATIO": str(self.data[ticker]['PE_RATIO']), #TODO: figure out how to get PE ratio
                    "STATE": "loss", #TODO: change state to update based on price change
                }
            else:
                stock = {
                    "COMPANY_NAME": self.data[ticker]['COMPANY_NAME'],
                    "STOCK_TICKER": self.data[ticker]['STOCK_TICKER'],
                    "REAL_TIME_PRICE": str(self.data[ticker]['REAL_TIME_PRICE']),
                    "PREVIOUS_CLOSE": str(self.data[ticker]['PREVIOUS_CLOSE']),
                    "OPEN": str(self.data[ticker]['OPEN']),
                    "FIFTY_TWO_WEEK_RANGE": str(self.data[ticker]['FIFTY_TWO_WEEK_RANGE']),
                    "VOLUME": str(self.data[ticker]['VOLUME']),
                    "AVERAGE_VOLUME": str(self.data[ticker]['AVERAGE_VOLUME']),
                    "MARKET_CAP": str(self.data[ticker]['MARKET_CAP']),
                    "PE_RATIO": str(self.data[ticker]['PE_RATIO']),
                    "STATE": "loss", #TODO: change state to update based on price change
                }

            stocks.append(Stock(stock))

        return stocks

    #TODO: Add multi-exchange support
    def is_market_open(
        self,
        close_time=datetime(1, 1, 1, hour=16, minute=0).time(),
        open_time=datetime(1, 1, 1, hour=9, minute=30).time(),
        timezone="US/Eastern",
    ):
        current_datetime = datetime.now(pytz.timezone("US/Eastern"))

        if (current_datetime.weekday() < 5) and (
            (current_datetime.time() > open_time) and (current_datetime.time() < close_time)
        ):
            return True

    def update_price_and_volume(self):
        for stock in self.stocks:
            yf_obj = yf.Ticker(stock.stock_ticker)
            stock.real_time_price = str(yf_obj.history(period='1d')['Close'][0])
            #stock.volume = str(randint(0, 100))

        return self.stocks