class Position:
    def __init__(self, entry_btc_quanity, entry_usdt_quantity, entry_btc_price):
        self.volume = 0
        self.entry_btc_quanity = entry_btc_quanity
        self.entry_usdt_quantity = entry_usdt_quantity
        self.entry_btc_price = entry_btc_price
        self.current_btc_quantity = entry_btc_quanity
        self.current_usdt_quantity = entry_usdt_quantity
        self.current_btc_price = entry_btc_price

    def calculate_profit_loss(self):
        return ((self.current_btc_price * self.current_btc_quantity) - (self.entry_btc_price * self.entry_btc_quanity)) + (self.current_usdt_quantity - self.entry_usdt_quantity)
    
    def calculate_delta(self, new_price: float):
        btc_quote = self.current_btc_quantity * new_price 
        share_diff = btc_quote / (btc_quote + self.current_usdt_quantity)
        amount_to_change = self.current_btc_quantity * (0.5 - share_diff) / 2
        # btc, usdt
        return amount_to_change, amount_to_change * new_price

    def apply_candlestick(self, candle):
        # delta = (float(candle['Close']) - self.current_btc_price) * self.current_btc_quantity
        (btc_delta, usdt_delta) = self.calculate_delta(float(candle['Close']))
        # if self.current_usdt_quantity - delta > 0:
        # print(f"btc delta {btc_delta} usdt delta {usdt_delta}")
        if self.current_usdt_quantity - usdt_delta > 0 and self.current_btc_quantity + btc_delta > 0:

            # self.current_btc_quantity += delta / self.current_btc_price
            self.current_btc_quantity += btc_delta
            self.current_usdt_quantity -= usdt_delta
            self.volume += abs(usdt_delta)
            self.current_btc_price = float(candle['Close'])

    def __str__(self):
        old_value = self.entry_btc_quanity * self.entry_btc_price + self.entry_usdt_quantity
        new_value = self.current_btc_price * self.current_btc_quantity + self.current_usdt_quantity
        pos_percent = (new_value - old_value) / old_value * 100
        hodl_old_value = self.entry_btc_quanity * 2 * self.entry_btc_price
        hodl_new_value = self.entry_btc_quanity * 2 * self.current_btc_price
        hodl_percent = (hodl_new_value - hodl_old_value) / hodl_old_value * 100
        ff_old_value = old_value
        ff_new_value = self.entry_btc_quanity * self.current_btc_price + self.entry_usdt_quantity
        ff_percent = (ff_new_value - ff_old_value) / ff_old_value * 100

        return f"""
    Position: (BTC: {self.current_btc_quantity}, USDT:{self.current_usdt_quantity}, Price: {self.current_btc_price}, Total Volume: {self.volume}, Value: {new_value}, Percent: {pos_percent}) 
    HODL: (BTC: {self.entry_btc_quanity * 2}, Initial price: {self.entry_btc_price}, Close price: {self.current_btc_price}, Value: {hodl_new_value}, Percent: {hodl_percent})
    50/50: (BTC: {self.entry_btc_quanity}, USDT:{self.entry_usdt_quantity}, Value: {ff_new_value}, Percent: {ff_percent})
    """


def balanced_position(usdt_quantity, price: float):
    """
    Calculate the balanced position based on quantity and price.
    """
    entry_usdt_quantity = usdt_quantity / 2
    entry_btc_quantity = entry_usdt_quantity / price
    return Position(entry_btc_quantity, entry_usdt_quantity, price)
