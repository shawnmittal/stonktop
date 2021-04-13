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
    def __init__(self, tickers=["AAPL", "GOOG", "MSFT"]):
        super().__init__()
        self.tickers = tickers
        self.stocks = self._get_stocks()

    def _get_stocks(self):
        stocks = []

        for ticker in self.tickers:
            # TODO: Replace random info with yfinance information
            stock = {
                "COMPANY_NAME": "temp",
                "STOCK_TICKER": ticker,
                "REAL_TIME_PRICE": str(randint(0, 100)),
                "PREVIOUS_CLOSE": str(randint(0, 100)),
                "OPEN": str(randint(0, 100)),
                "FIFTY_TWO_WEEK_RANGE": str(randint(0, 100)),
                "VOLUME": str(randint(0, 100)),
                "AVERAGE_VOLUME": str(randint(0, 100)),
                "MARKET_CAP": str(randint(0, 100)),
                "PE_RATIO": str(randint(0, 100)),
                "STATE": "loss",
            }

            stocks.append(Stock(stock))

        return stocks

    def update_price_and_volume(self):
        for stock in self.stocks:
            stock.real_time_price = str(randint(0, 100))
            stock.volume = str(randint(0, 100))

        return self.stocks