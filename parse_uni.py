import datetime
import requests
import matplotlib.pyplot as plt
import csv
import os

START_TIME=datetime.datetime(2022, 8, 1)

# 1375726
def get_candlesticks(id, interval, limit, to_time=None):
    """
    Fetch candlestick data for a given symbol and interval.
    """
    print(f"to time {to_time}")
    r = requests.get(f'https://api.coinmarketcap.com/kline/v3/k-line/candles/1/{id}?reverse-order=false&usd=true&pm=p&type={interval}&countBack={limit}&to={to_time}')
    raw_candles = r.json()['data']
    print(f"{raw_candles}")

    candles = []
    for raw_candle in raw_candles:
        candle = []
        # Convert timestamp to datetime
        candle.append(datetime.datetime.fromtimestamp(raw_candle['time'] / 1000))
        # Convert prices to float
        candle.append(float(raw_candle['open']))
        candle.append(float(raw_candle['high']))
        candle.append(float(raw_candle['low']))
        candle.append(float(raw_candle['close']))
        candle.append(float(raw_candle['volume']))
        candles.append(candle)
    return candles

now = datetime.datetime.now().replace(second=0, microsecond=0)
counter = 0


batch = get_candlesticks('1375726', '1m', 1000, to_time=int(now.timestamp() * 1000))
while batch and len(batch) > 0:
    counter += 1
    print("Got results")
    with open(f"temp.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ts', 'Open', 'Hight', 'Low', 'Close', 'v'])
        for candle in batch:
            csvwriter.writerow(candle)
        print(f"FROM -- {batch[0][0].timestamp()}")
        with open(f"candles_uni.csv", 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for line in csvreader:
                csvwriter.writerow(line)
    os.remove("./candles_uni.csv")
    os.rename("./temp.csv", "./candles_uni.csv")
    batch = get_candlesticks('1375726', '1m', 1000, to_time=int(batch[0][0].timestamp() * 1000))

    
        # if batch[-1][0].timestamp() == datetime.datetime.now().replace(second=0, microsecond=0).timestamp():
        #     print("Reached the current time, stopping.")
        #     break