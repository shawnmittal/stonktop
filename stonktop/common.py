import json
import pytz
import yfinance as yf
from pathlib import Path
from datetime import datetime


class Stock:
    def __init__(self, d: dict):
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


class Portfolio:
    def __init__(self, data_path=Path("./data.json")):
        self.data_path = data_path
        self.data = self._read_data()
        self.tickers = self.data.keys()
        self.stocks = self._get_stocks()

    def _read_data(self):
        with open(self.data_path, "r") as fp:
            data = json.load(fp)

        return data

    def _get_stocks(self):
        stocks = []

        for ticker in self.tickers:
            # TODO: Replace random info with yfinance information
            if self.is_market_open():
                # TODO: Add error handling for tickers that don't exist
                yf_obj = yf.Ticker(ticker)
                temp = yf_obj.info
                stock = {
                    "COMPANY_NAME": temp["longName"],
                    "STOCK_TICKER": temp["symbol"],
                    "REAL_TIME_PRICE": f'${yf_obj.history(period="1d")["Close"][0]:>.2f}',
                    "PREVIOUS_CLOSE": f'${temp["previousClose"]:>.2f}',
                    "OPEN": f'${temp["open"]:>.2f}',
                    "FIFTY_TWO_WEEK_RANGE": f"(${temp['fiftyTwoWeekLow']:>.2f}, ${temp['fiftyTwoWeekHigh']:>.2f})",
                    "VOLUME": f'{temp["volume"]}',  # TODO: fix to be live volume
                    "AVERAGE_VOLUME": f'{temp["averageVolume"]}',
                    "MARKET_CAP": f'${temp["marketCap"]}',
                    "PE_RATIO": f'{self.data[ticker]["PE_RATIO"]:>.2f}',
                    # TODO: figure out how to get PE ratio
                    "STATE": "loss",  # TODO: change state to update based on price change
                }
            else:
                stock = {
                    "COMPANY_NAME": self.data[ticker]["COMPANY_NAME"],
                    "STOCK_TICKER": self.data[ticker]["STOCK_TICKER"],
                    "REAL_TIME_PRICE": f'${self.data[ticker]["REAL_TIME_PRICE"]:>.2f}',
                    "PREVIOUS_CLOSE": f'${self.data[ticker]["PREVIOUS_CLOSE"]:>.2f}',
                    "OPEN": f'${self.data[ticker]["OPEN"]:>.2f}',
                    "FIFTY_TWO_WEEK_RANGE": f'{self.data[ticker]["FIFTY_TWO_WEEK_RANGE"]}',
                    "VOLUME": f'{self.data[ticker]["VOLUME"]}',
                    "AVERAGE_VOLUME": f'{self.data[ticker]["AVERAGE_VOLUME"]}',
                    "MARKET_CAP": f'${self.data[ticker]["MARKET_CAP"]}',
                    "PE_RATIO": f'{self.data[ticker]["PE_RATIO"]:>.2f}',
                    "STATE": "loss",  # TODO: change state to update based on price change
                }

            stocks.append(Stock(stock))

        return stocks

    # TODO: Add multi-exchange support
    def is_market_open(
        self,
        close_time=datetime(1, 1, 1, hour=16, minute=0).time(),
        open_time=datetime(1, 1, 1, hour=9, minute=30).time(),
        timezone="US/Eastern",
    ):
        current_datetime = datetime.now(pytz.timezone("US/Eastern"))

        if (current_datetime.weekday() < 5) and (
            (current_datetime.time() > open_time)
            and (current_datetime.time() < close_time)
        ):
            return True

    def update_price_and_volume(self):
        for stock in self.stocks:
            yf_obj = yf.Ticker(stock.stock_ticker)
            stock.real_time_price = f'${yf_obj.history(period="1d")["Close"][0]:>.2f}'
            # stock.volume = str(randint(0, 100))

        return self.stocks