from bot.market import get_price

def simple_strategy(symbol):
    price = get_price(symbol)

    print(f"Strategy check → Price: {price}")

    # Dumb logic (but better than nothing)
    if price < 75000:
        return "BUY"
    elif price > 80000:
        return "SELL"
    else:
        return "HOLD"