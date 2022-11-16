"""
Write a Python script to accomplish the following tasks. The program should run
correctly.

Use https://finnhub.io/ free stock price API to query stock prices for specific tech
stocks. Please do not use their python package, use the requests package in
Python.

Get the latest price for Apple, Amazon, Netflix, Facebook, Google.

Between Apple, Amazon, Netflix, Facebook, Google : find the stock that moved the
most percentage points from yesterday. Call this stock most_volatile_stock

Save the following information for the most_volatile_stock to a CSV file with the
following rows. Please also include the header in the CSV file:

Example:
stock_symbol, percentage_change, current_price, last_close_price
AAPL, 13.2, 120.5, 150
"""


# IMPORTS:

from requests import Session, RequestException, Response
from csv import writer
from time import perf_counter, sleep
from os import startfile


# CONSTANTS:

# https://github.com/samyak1409/internship-tasks#7-always-send-custom-user-agent-to-tell-the-website-that-its-not-a-bot:
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/107.0.0.0 Safari/537.36'}

BASE_URL = 'https://finnhub.io/api/v1'  # API Documentation: https://finnhub.io/docs/api

API_KEY_FILE = 'API Key.txt'

# Stock Name to Stock Symbol Mapping:
STOCK_SYMBOLS = {'Apple': 'AAPL', 'Amazon': 'AMZN', 'Netflix': 'NFLX', 'Facebook': 'META', 'Google': 'GOOGL'}

CSV_FILE = 'most_volatile_stock.csv'

COLUMN_NAMES = ('stock_symbol', 'percentage_change', 'current_price', 'last_close_price')


# FUNCTIONS:

def get_response(url: str) -> Response:
    """Gets Request's Response handling any possible Exception (Error)."""
    while True:
        try:
            response_ = session.get(url=url)
        except RequestException as e:  # failed to get any response
            print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
            sleep(1)  # take a breath
        else:  # received response
            if response_.status_code == 200:  # OK
                return response_
            else:  # bad response
                print(f'{response_.status_code}: {response_.reason} TRYING AGAIN...')
                sleep(1)  # take a breath


# MAIN:

# Get API Key:
try:  # EAFP (https://docs.python.org/3/glossary.html#term-EAFP)
    api_key = open(file=API_KEY_FILE).read().strip()  # try to read key from file
except FileNotFoundError:
    # Ask the user for it:
    api_key = input('\nHey There! Copy your API Key from https://finnhub.io/dashboard and paste here '
                    '(you only need to do this once, it\'ll be cached for future): ').strip()
    open(file=API_KEY_FILE, mode='w', newline='').write(api_key)  # cache the key

# Time the Process:
start_time = perf_counter()

# Writing column names in CSV:
with open(file=CSV_FILE, mode='w', newline='') as f:  # (overwrites everytime)
    writer(f).writerow(COLUMN_NAMES)
# startfile(CSV_FILE); exit()  # debugging

# Session Init (https://github.com/samyak1409/internship-tasks#3-sending-multiple-requests-to-same-host):
with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    print('\nGetting Stock Data from https://finnhub.io...\n')

    most_volatile_stock = [None, 0, None, None]  # init
    # [stock_symbol, percentage_change, current_price, last_close_price]

    # Loop through the stocks:
    for stock_name, stock_symbol in STOCK_SYMBOLS.items():

        # Using https://finnhub.io/docs/api/quote (real-time quote data for US stocks):
        response_json = get_response(url=f'{BASE_URL}/quote?token={api_key}&symbol={stock_symbol}').json()
        print(stock_name, response_json)  # debugging
        # Response Attributes:
        # c: Current price
        # d: Change
        # dp: Percent change -> DECIDER FOR `most_volatile_stock`
        # h: High price of the day
        # l: Low price of the day
        # o: Open price of the day
        # pc: Previous close price

        # Check & Update Most Volatile Stock:
        if (percent_change := abs(response_json['dp'])) > most_volatile_stock[1]:
            # IMP: Using `abs` because we want absolute max percent_change.
            # `most_volatile_stock[1]`: previous max percent_change

            most_volatile_stock = [stock_symbol, percent_change, response_json['c'], response_json['pc']]

    print('\nMost Volatile Stock:', most_volatile_stock)

    # Writing it to the CSV:
    with open(file=CSV_FILE, mode='a', newline='') as f:
        writer(f).writerow(most_volatile_stock)


startfile(CSV_FILE)  # automatically open CSV when process completes

print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')
