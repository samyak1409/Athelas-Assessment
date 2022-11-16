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
