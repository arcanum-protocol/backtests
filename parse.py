import datetime
import requests
import matplotlib.pyplot as plt
import csv

START_TIME=datetime.datetime(2020, 1, 1)

def get_candlesticks(symbol, interval, limit, start_time=None):
    """
    Fetch candlestick data for a given symbol and interval.
    """
    r = requests.get(f'https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}&timeZone=3&startTime={start_time}')
    raw_candles = r.json()

    candles = []
    for raw_candle in raw_candles:
        candle = []
        # Convert timestamp to datetime
        candle.append(datetime.datetime.fromtimestamp(raw_candle[0] / 1000))
        # Convert prices to float
        candle.append(float(raw_candle[1]))
        candle.append(float(raw_candle[2]))
        candle.append(float(raw_candle[3]))
        candle.append(float(raw_candle[4]))
        candle.append(float(raw_candle[5]))
        candles.append(candle)
    return candles
with open("candles1.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ts', 'Open', 'Hight', 'Low', 'Close', 'v'])
    batch = get_candlesticks('BTCUSDT', '1m', 1000, start_time=int(START_TIME.timestamp() * 1000))

    while batch and len(batch) > 0:
        print("Got results")
        for candle in batch:
            csvwriter.writerow(candle)
        batch = get_candlesticks('BTCUSDT', '1m', 1000, start_time=int(batch[-1][0].timestamp() * 1000))
        if batch[-1][0].timestamp() == datetime.datetime.now().replace(second=0, microsecond=0).timestamp():
            print("Reached the current time, stopping.")
            break