# Binance Futures Testnet Trading Bot

A minimal CLI-based trading bot for Binance Futures Testnet.

The goal was simple: build something that **doesn't send invalid orders to the exchange**.
Most beginner bots ignore this and fail at runtime — this one validates everything before execution.

---

## What this actually does

* Place MARKET and LIMIT orders
* Supports BUY and SELL
* Validates orders using real Binance rules before sending them

This project focuses on the execution layer — making sure orders are **correct and accepted**, not just sent.

---

## How the flow works

1. `cli.py` → takes user input
2. `validators.py` → checks order validity using exchange filters
3. `market.py` → fetches symbol info and price
4. `orders.py` → sends request to Binance
5. `client.py` → handles API connection

The key idea:
👉 validation happens **before** the API call, not after failure

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
API_KEY=your_testnet_key
API_SECRET=your_testnet_secret
BASE_URL=https://testnet.binancefuture.com
```

Use **Binance Futures Testnet keys only**.

---

## Usage

### Get current price

```bash
python cli.py --symbol BTCUSDT --get_price
```

Output:

```text
Current price of BTCUSDT: 75567.6
```

---

### Place MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005
```

Output:

```text
====== ORDER RESPONSE ======
Order ID     : 13058400001
Status       : FILLED
Executed Qty : 0.005
Avg Price    : 75560.12
============================

→ Order fully executed

✔ Order processed successfully
```

---

### Place LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.005 --price 90000
```

Output:

```text
====== ORDER RESPONSE ======
Order ID     : 13058468392
Status       : NEW
Executed Qty : 0.0000
Avg Price    : 0.00
============================

→ Order placed but NOT filled yet (waiting in order book)

✔ Order processed successfully
```

---

### Validation example (failure case)

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.00003 --price 20000
```

Output:

```text
Validation/Error: Quantity too small. Min: 0.0001
```

---

## Validation handled

* LOT_SIZE → min quantity + step size
* MIN_NOTIONAL → minimum order value
* Basic input validation (side, type, etc.)

One issue I ran into was floating-point precision while validating step size.
Using `%` caused valid quantities to fail.

Fixed it by rounding values to the exchange precision instead of relying on raw float math.

---

## Logs

Logs are written to:

```text
logs/bot.log
```

Includes:

* request payloads
* API responses
* errors

---

## Notes

* LIMIT orders only execute if market reaches the price
* MARKET orders execute immediately
* API errors are caught and logged

---

## What’s missing

* No position tracking yet
* No PnL monitoring
* No strategy logic (manual CLI execution only)

This is intentional — focus was on building a **reliable execution layer first**.

---

## Summary

This is a simple but reliable trading CLI that focuses on **correctness over features**.

It ensures orders follow Binance rules before hitting the API, which avoids unnecessary failures and makes the system more predictable.
