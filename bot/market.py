from bot.client import get_client

client = get_client()


def get_price(symbol):
    ticker = client.futures_symbol_ticker(symbol=symbol)
    return float(ticker["price"])


def get_symbol_info(symbol):
    info = client.futures_exchange_info()

    for s in info["symbols"]:
        if s["symbol"] == symbol:
            return s

    raise ValueError("Invalid symbol")