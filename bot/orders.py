from bot.client import get_client
import logging
from binance.exceptions import BinanceAPIException

client = get_client()


def _print_order_summary(payload):
    print("\n====== ORDER REQUEST ======")
    print(f"Symbol   : {payload['symbol']}")
    print(f"Side     : {payload['side']}")
    print(f"Type     : {payload['type']}")
    print(f"Quantity : {payload['quantity']}")
    if payload.get("price"):
        print(f"Price    : {payload['price']}")
    print("===========================\n")


def _print_order_response(response):
    print("====== ORDER RESPONSE ======")
    print(f"Order ID     : {response.get('orderId')}")
    print(f"Status       : {response.get('status')}")
    print(f"Executed Qty : {response.get('executedQty')}")
    print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
    print("============================")

    # Interpret status (this is what makes you stand out)
    status = response.get("status")

    if status == "NEW":
        print("→ Order placed but NOT filled yet (waiting in order book)")
    elif status == "FILLED":
        print("→ Order fully executed")
    elif status == "PARTIALLY_FILLED":
        print("→ Order partially filled")
    else:
        print(f"→ Status: {status}")

    print("\n✔ Order processed successfully\n")


def place_order(symbol, side, order_type, quantity, price=None):
    payload = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price
    }

    _print_order_summary(payload)

    try:
        # -------- ORDER EXECUTION --------
        if order_type == "MARKET":
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )

        elif order_type == "LIMIT":
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )

        elif order_type == "STOP":
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_MARKET",
                stopPrice=price,
                quantity=quantity
            )

        else:
            raise ValueError("Unsupported order type")

        # -------- LOGGING --------
        logging.info(f"REQUEST: {payload}")
        logging.info(f"RESPONSE: {response}")

        # -------- OUTPUT --------
        _print_order_response(response)

        return response

    except BinanceAPIException as e:
        logging.error(f"Binance API Error: {e.message}")
        print("\n Binance Error:")
        print(e.message)

    except Exception as e:
        logging.error(str(e))
        print("\n Unexpected Error:")
        print(str(e))