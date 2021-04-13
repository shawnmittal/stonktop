# StonkTop
Python based terminal user interface (TUI) for tracking stocks. Inspired by [cointop](https://github.com/miguelmota/cointop).

The project is built using [urwid](https://github.com/urwid/urwid) a CUI library for Python. 

Data structures heavily lifted from [stui](https://github.com/mil-ad/stui), a Slurm dashboard for the terminal.

## To Do:
- Add yfinance integration to pull down real stock data
- Add portfolio config file to maintain persistance
- Add pop-up that allows adding tickers
- Add ability to delete stocks
- Add ability to sort by columns
- Update state based on gain/loss

## Fixes:
- Change focus to be at the top most stock widget, not bottom