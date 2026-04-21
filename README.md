# Binance Futures Testnet Trading Bot

## What this project does

This is a simple Python CLI app that places orders on Binance Futures Testnet.

It supports:

* MARKET and LIMIT orders
* BUY and SELL sides
* Input validation before sending requests

The focus was on correctness, validation, and clean structure rather than adding unnecessary features.

---

## How it works

* `cli.py` → takes user input
* `validators.py` → validates order using Binance rules
* `orders.py` → places the order
* `market.py` → fetches price and symbol info
* `client.py` → connects to Binance API

Validation is done **before API calls** to avoid unnecessary failures.

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
API_KEY=your_testnet_key
API_SECRET=your_testnet_secret
BASE_URL=https://testnet.binancefuture.com
```

Use **Futures Testnet keys only**.

---

## Usage (Commands + Output)

### 1. Get current price

**Command:**

```bash
python cli.py --symbol BTCUSDT --get_price
```

**Output:**

```text
Current price of BTCUSDT: 75567.6
```

---

### 2. Place MARKET order

**Command:**

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005
```

**Output:**

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

### 3. Place LIMIT order (not immediately filled)

**Command:**

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.005 --price 90000
```

**Output:**

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

### 4. Invalid order example (validation)

**Command:**

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.00003 --price 20000
```

**Output:**

```text
Validation/Error: Quantity too small. Min: 0.0001
```

---

## Validation handled

* Quantity follows LOT_SIZE (step size + min/max)
* Price follows tick size
* Minimum order value (MIN_NOTIONAL)
* Basic input validation

One issue I encountered was floating-point precision while checking step size. Using `%` caused errors, so I switched to precision-based rounding.

---

## Logs

Logs are saved in:

```text
logs/bot.log
```

Includes:

* API request payload
* API response
* Errors

---

## Notes

* LIMIT orders only execute if price matches market conditions
* MARKET orders execute instantly
* API errors are handled and logged

---

## What I would improve

* Add order status tracking
* Improve CLI (interactive mode)
* Add more advanced strategies

---

This project focuses on building a clean, reliable base trading system with proper validation and structure.
