import datetime
import csv

from balance import balanced_position

def calculate_balanced_position(start: datetime.datetime, finish: datetime.datetime, quantity):
    position = None

    ts = []
    pnls = []
    with open('candles.csv', mode='r') as file:
    # Create a CSV reader with DictReader
        csv_reader = csv.DictReader(file)
        for candle in csv_reader:
            if datetime.datetime.fromisoformat(candle['ts']) >= start and datetime.datetime.fromisoformat(candle['ts']) <= finish:
                if position is None:
                    position = balanced_position(quantity, float(candle['Close']))
                    print(f"Initial Position: {position}")
                else:
                    position.apply_candlestick(candle)
                    # print(position)
                    pnl = position.calculate_profit_loss()
                    ts.append(candle['ts'])
                    pnls.append(pnl)
                # print(f"Profit/Loss: {pnl}, timestamp: {candle['ts']}")

    # Plotting the results
    print(f"Final Position: {position}")
    print(f"")

    # plt.plot(ts, pnls)
    # plt.xlabel('Time')
    # plt.ylabel('Profit/Loss')
    # plt.title('Profit/Loss over Time')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

# SHORT_START=datetime.datetime(2022, 1, 1)
# SHORT_END=datetime.datetime(2023, 1, 5)

# print(f"Shorting from {SHORT_START} to {SHORT_END}")
# calculate_balanced_position(SHORT_START, SHORT_END)
# print('\n')

# SAME_PRICE_START=datetime.datetime(2022, 1, 1)
# SAME_PRICE_END=datetime.datetime(2024, 5, 25)
# print(f"Price descending and returning from {SAME_PRICE_START} to {SAME_PRICE_END}")
# calculate_balanced_position(SAME_PRICE_START, SAME_PRICE_END)
# print('\n')

# LONG_START=datetime.datetime(2023, 1, 5)
# LONG_END=datetime.datetime(2024, 11, 20)
# print(f"Growing from {LONG_START} to {LONG_END}")
# calculate_balanced_position(LONG_START, LONG_END)

# LONG_START=datetime.datetime(2020, 12, 1)
# LONG_END=datetime.datetime(2022, 6, 1)
# print(f"взлет падение до той же цены в 20к {LONG_START} to {LONG_END}")
# calculate_balanced_position(LONG_START, LONG_END, 1_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 10_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 100_000_000)
# print('\n')

# LONG_START=datetime.datetime(2023, 1, 1)
# LONG_END=datetime.datetime(2025, 1, 1)
# print(f"лучший рост в истории {LONG_START} to {LONG_END}")
# calculate_balanced_position(LONG_START, LONG_END, 1_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 10_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 100_000_000)
# print('\n')

# LONG_START=datetime.datetime(2023, 1, 1)
# LONG_END=datetime.datetime(2025, 6, 1)
# print(f"если бы ты держал с ласт цикла ликвидность {LONG_START} to {LONG_END}")
# calculate_balanced_position(LONG_START, LONG_END, 1_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 10_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 100_000_000)
# print('\n')

# LONG_START=datetime.datetime(2024, 3, 1)
# LONG_END=datetime.datetime(2024, 10, 1)
# print(f"не оч сильные вверх вниз но при этом цена вернулась назад {LONG_START} to {LONG_END}")
# calculate_balanced_position(LONG_START, LONG_END, 1_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 10_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 100_000_000)
# print('\n')

# LONG_START=datetime.datetime(2021, 10, 1)
# LONG_END=datetime.datetime(2022, 6, 1)
# print(f"жоска падаем {LONG_START} to {LONG_END}")
# calculate_balanced_position(LONG_START, LONG_END, 1_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 10_000_000)
# calculate_balanced_position(LONG_START, LONG_END, 100_000_000)
# print('\n')

LONG_START=datetime.datetime(2021, 11, 1)
LONG_END=datetime.datetime(2025, 1, 1)
print(f"с хаев вниз потом на хаи {LONG_START} to {LONG_END}")
calculate_balanced_position(LONG_START, LONG_END, 1_000_000)
calculate_balanced_position(LONG_START, LONG_END, 10_000_000)
calculate_balanced_position(LONG_START, LONG_END, 100_000_000)