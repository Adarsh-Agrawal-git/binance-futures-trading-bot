import argparse
import time

from bot.validators import validate_order
from bot.orders import place_order
from bot.logging_config import setup_logging
from bot.market import get_price
from bot.strategy import simple_strategy

setup_logging()

parser = argparse.ArgumentParser(description="Trading Bot CLI")

# Core argument
parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")

# Order arguments
parser.add_argument("--side", help="BUY or SELL")
parser.add_argument("--type", help="MARKET or LIMIT")
parser.add_argument("--quantity", type=float, help="Order quantity")
parser.add_argument("--price", type=float, help="Price (required for LIMIT)")

# Modes
parser.add_argument("--get_price", action="store_true", help="Fetch current price")
parser.add_argument("--auto", action="store_true", help="Run auto trading strategy")

args = parser.parse_args()


# MODE 1: GET PRICE
if args.get_price:
    try:
        price = get_price(args.symbol)
        print(f"\nCurrent price of {args.symbol}: {price}")
    except Exception as e:
        print(f"\n Error fetching price: {str(e)}")
    exit()


# MODE 2: AUTO STRATEGY
if args.auto:
    print("\nRunning auto trading strategy...\n")

    try:
        while True:
            price = get_price(args.symbol)
            decision = simple_strategy(price)

            print(f"Price: {price} | Decision: {decision}")

            if decision:
                place_order(args.symbol, decision, "MARKET", 0.001)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n Auto trading stopped by user.")
    except Exception as e:
        print(f"\n Error in auto mode: {str(e)}")

    exit()


# MODE 3: MANUAL ORDER
if not args.side or not args.type or not args.quantity:
    parser.error("--side, --type, and --quantity are required for placing orders")

try:
    symbol, side, order_type = validate_order(
        args.symbol,
        args.side,
        args.type,
        args.quantity,
        args.price
    )

    place_order(
        symbol,
        side,
        order_type,
        args.quantity,
        args.price
    )

except Exception as e:
    print(f"\n Validation/Error: {str(e)}")