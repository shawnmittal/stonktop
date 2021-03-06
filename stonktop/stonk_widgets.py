import urwid
from stonktop import common
from stonktop import util_widgets
from typing import OrderedDict
from datetime import datetime

#TODO: Move into cli.py as configurable on launch
UPDATE_TIME_INTERVAL = 1
UPDATE_STOCK_INTERVAL = 10


class StockWidget(urwid.WidgetWrap):

    STATE_ATTR_MAPPING = {"gain": {None: "gain"}, "loss": {None: "loss"}}

    def __init__(self, stock):
        self.columns = OrderedDict()
        self.columns["selected"] = urwid.Text("", wrap="ellipsis", align='left')
        self.columns["name"] = urwid.Text("", wrap="ellipsis", align='left')
        self.columns["ticker"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["current"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["prev_close"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["open"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["52_week_range"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["volume"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["avg_volume"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["market_cap"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["pe_ratio"] = urwid.Text("", wrap="ellipsis", align='center')
        self.columns["state"] = urwid.AttrMap(urwid.Text("", wrap="ellipsis"), None)

        self.update_values(stock)

        w = util_widgets.SelectableColumns(
            [
                (*weight, urwid.Padding(c))
                for weight, c in zip(
                    PortfolioListWidget.column_widths, self.columns.values()
                )
            ]
        )

        w = urwid.AttrMap(w, None)  # Details handled by PortfolioListWidget

        self.selected = False

        super().__init__(w)

    def update_values(self, stock):
        self.columns["name"].set_text(stock.company_name)
        self.columns["ticker"].set_text(stock.stock_ticker)
        self.columns["current"].set_text(stock.real_time_price)
        self.columns["prev_close"].set_text(stock.previous_close)
        self.columns["open"].set_text(stock.open)
        self.columns["52_week_range"].set_text(stock.fifty_two_week_range)
        self.columns["volume"].set_text(stock.volume)
        self.columns["avg_volume"].set_text(stock.average_volume)
        self.columns["market_cap"].set_text(stock.market_cap)
        self.columns["pe_ratio"].set_text(stock.pe_ratio)
        self.columns["state"]._original_widget.set_text(stock.state.title())

        self.columns["state"].set_attr_map(self.STATE_ATTR_MAPPING[stock.state])

    def set_selected_attr(self, in_focus):
        if in_focus:
            attr = "highlight"
        else:
            attr = "highlight_out_of_focus"

        self._w.set_focus_map(
            {
                None: attr,
                "gain": attr,
                "loss": attr,
            }
        )

    def keypress(self, size, key):
        if key == " ":
            self.toggle_select()
        else:
            return super().keypress(size, key)

    def toggle_select(self):
        if not self.selected:
            self.columns["selected"].set_text("???")
        else:
            self.columns["selected"].set_text("")
        self.selected = not self.selected

    def is_selected(self):
        return self.selected


class PortfolioListWidget(urwid.WidgetWrap):

    signals = ["focus_changed"]

    column_widths = [
        (2,),
        (18,),
        (8,),
        (10,),
        (10,),
        (10,),
        (22,),
        (11,),
        (13,),
        (16,),
        (10,),
        (5,),
    ]

    def __init__(self):

        column_labels = [
            "",
            "Name",
            "Ticker",
            "Current",
            "Close",
            "Open",
            "52 wk",
            "Volume",
            "Avg. Volume",
            "Market Cap",
            "PE Ratio",
            "State",
        ]

        header_w = [
            (
                *weight,
                urwid.Padding(urwid.Text(c, wrap="ellipsis", align='center')),
            )
            for c, weight in zip(column_labels, self.column_widths)
        ]
        header_w = urwid.Columns(header_w)

        self.walker = urwid.SimpleFocusListWalker([])
        w = util_widgets.FancyListBox(self.walker)
        w = urwid.Frame(w, header_w)
        w = util_widgets.FancyLineBox(w, "Portfolio")

        self.walker.set_focus_changed_callback(self._focus_changed)

        super().__init__(w)

    def update_stock_widgets(self, stock_widgets):
        self.walker[:] = stock_widgets

    def get_focused_stock_idx(self):
        _, stock_idx = self.walker.get_focus()
        return stock_idx

    def get_selected_stock_indices(self):
        indices = [idx for idx, w in enumerate(self.walker) if w.is_selected()]
        return indices

    def _focus_changed(self, idx):
        urwid.emit_signal(self, "focus_changed")

    def render(self, size, focus=False):
        stock_widget, _ = self.walker.get_focus()
        if stock_widget is not None:
            stock_widget.set_selected_attr(focus)

        return self._wrapped_widget.render(size, focus=True)


class PortfolioViewWidget(urwid.WidgetWrap):
    def __init__(self):
        self.panel = PortfolioListWidget()

        w = urwid.Columns([("weight", 80, self.panel)])

        super().__init__(w)

    def keypress(self, size, key):
        return super().keypress(size, key)


class PortfolioView:
    def __init__(self, portfolio):
        self.portfolio = portfolio

        self.view = PortfolioViewWidget()
        self.panel = self.view.panel

        self.view_placeholder = urwid.WidgetPlaceholder(self.view)

        self.stock_widgets_dict = {}

        urwid.connect_signal(self.panel, "focus_changed", self.on_stocks_focus_changed)

    def on_stocks_focus_changed(self):
        stock = self.get_focus_stock()

        if stock is None:
            return
        else:
            return

    def create_stock_widgets(self, stocks):
        if len(stocks) == 0:
            return []
        stocks_widgets = [StockWidget(s) for s in stocks]
        return stocks_widgets

    def get_focus_stock(self):
        stock_idx = self.panel.get_focused_stock_idx()

        if stock_idx is None:
            return None
        else:
            return self.stocks[stock_idx]

    def refresh(self):
        self.stocks = self.portfolio.update_price_and_volume()

        stock_widgets_ordered = []
        stock_widgets_dict = {}  # TODO: Currently not using stock dict.
        for stock in self.stocks:
            try:
                w = self.stock_widgets_dict[stock.stock_ticker]
                w.update_values(stock)
                stock_widgets_ordered.append(w)
                stock_widgets_dict[stock.stock_ticker] = w
            except KeyError:
                w = StockWidget(stock)
                stock_widgets_ordered.append(w)
                stock_widgets_dict[stock.stock_ticker] = w

        self.stock_widgets_dict = stock_widgets_dict
        self.panel.update_stock_widgets(stock_widgets_ordered)

    def get_view(self):
        return self.view_placeholder


# TODO: should probably rename this to avoid confusion with StockWidget
class StonkWidget(urwid.WidgetWrap):
    def __init__(self, portfolio):

        self.portfolio = portfolio

        self.header_time = urwid.Text(datetime.now().strftime("%X"), align="right")
        self.header_portfolio_name = urwid.Text("Stonks", align="center")

        header = urwid.Columns(
            [
                urwid.Text("To the Moon", align="left"),
                self.header_portfolio_name,
                self.header_time,
            ]
        )
        header = urwid.AttrMap(header, "bold")
        footer = urwid.Text("[q]: quit  [space]: select  [k]: up  [j]: down")

        self.portfolio_view = PortfolioView(self.portfolio)

        self.view = urwid.Frame(self.portfolio_view.get_view(), header, footer)

        self.view_placeholder = urwid.WidgetPlaceholder(self.view)

        super().__init__(self.view_placeholder)

    def set_name(self, portfolio_name):
        self.header_portfolio_name.set_text(
            [(None, "Portfolio:"), ("portfolio_name", portfolio_name)]
        )

    def update_time(self):
        time = datetime.now().strftime("%X")
        self.header_time.set_text(time)

    def refresh_stocks(self):
        self.portfolio_view.refresh()


class StonkApp:

    palette = [
        ("portfolio_name", "dark magenta", ""),
        ("gain", "light green", ""),
        ("loss", "light red", ""),
        ("bold", "bold", ""),
        ("underline", "underline", ""),
        ("highlight", "black", "yellow", ""),
        ("highlight_out_of_focus", "black", "brown", ""),
    ]

    def __init__(self, args):
        # TODO: add additional arguments that StonkTop can be called with
        self.portfolio = common.Portfolio()

        self.w = StonkWidget(self.portfolio)

        self.loop = urwid.MainLoop(
            self.w,
            self.palette,
            unhandled_input=self.exit_on_q,
        )

    def run(self):
        self.w.refresh_stocks()
        self.register_time_refresh()
        self.register_stock_refresh()
        # FIXME: Super hacky way to set focus on startup to first stock. I don't like this.
        self.w.portfolio_view.view.panel.walker.set_focus(0)
        self.loop.run()

    def exit_on_q(self, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()

    def refresh_time(self, loop, user_data):
        self.w.update_time()
        self.register_time_refresh()

    def register_time_refresh(self):
        self.loop.set_alarm_in(UPDATE_TIME_INTERVAL, self.refresh_time)

    def refresh_stock(self, loop, user_data):
        self.w.refresh_stocks()
        self.register_stock_refresh()

    def register_stock_refresh(self):
        self.loop.set_alarm_in(UPDATE_STOCK_INTERVAL, self.refresh_stock)