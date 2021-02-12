import json, requests, pprint, csv
from config import api_key
import pandas as pd

base_url = 'https://api.tdameritrade.com/v1'
instruments_url = f'{base_url}/instruments'
market_data = f'{base_url}marketdata/'


def create_stock_list():
    """
    :return creates nasdaq_stocks_ticker.csv from data I got online no need to run every again.
    """
    df = pd.read_json('data/nasdaq-listed_json.json')
    arr = []
    for i in df.iterrows():
        arr.append(i[1]['Symbol'])

    with open('data/nasdaq_stocks_ticker.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(arr)


def get_stock_data(symbol, projection):
    """
    :param symbol: ticker of stock
    :param projection: type of stock/data you want
    :return: data on the stock
    """

    payload = {'apikey': api_key,
               'symbol': symbol,
               'projection': projection}

    results = requests.get(instruments_url, params=payload)
    return results.json()


def get_stock_price_history(symbol, periodType, period=None, frequencyType=None, frequency=None, endDate=None,
                            startDate=None,
                            needExtendedHoursData=None):
    """
    :param startDate: Start date as milliseconds since epoch. If startDate and endDate are provided, period should not be provided.
    :param endDate: End date as milliseconds since epoch. If startDate and endDate are provided, period should not be provided. Default is previous trading day.
    :param frequency: The number of the frequencyType to be included in each candle.
        Valid frequencies by frequencyType (defaults marked with an asterisk):
        minute: 1*, 5, 10, 15, 30
        daily: 1*
        weekly: 1*
        monthly: 1*
    :param frequencyType: The type of frequency with which a new candle is formed.
        Valid frequencyTypes by periodType (defaults marked with an asterisk):
        day: minute*
        month: daily, weekly*
        year: daily, weekly, monthly*
        ytd: daily, weekly*
    :param needExtendedHoursData: Boolean whether you want extended data or na
    :param periodType: day, month, year, ytd
    :param period: The number of periods to show. Example: For a 2 day / 1 min chart, the values would be:
        period: 2
        periodType: day
        frequency: 1
        frequencyType: min
    :param symbol: ticker of stock
    :return: data on the stock
    """
    payload = {
        'apikey': api_key,
        'periodType': periodType,
        'period': period,
        'frequencyType': frequencyType,
        'frequency': frequency,
        'endDate': endDate,
        'startDate': startDate,
        'needExtendedHoursData': needExtendedHoursData
    }
    url = f'{market_data}/{symbol}/pricehistory'
    results = requests.get(url, params=payload)


def get_stock_list():
    """
    :returns an array of all the stocks in the nasdaq
    """
    arr = []
    with open('data/nasdaq_stocks_ticker.csv', newline='') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for r in data_reader:
            arr = r

    return arr


if __name__ == "__main__":
    stocks = get_stock_list()

    # i = 0
    # while i < 10:
    #     data = get_stock_data(stocks[i], 'fundamental')
    #     print(data)
    #     i += 1
    data = get_stock_data('GME', 'fundamental')
    print(data['GME']['fundamental'])
