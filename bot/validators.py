from bot.market import get_symbol_info


def _get_precision(step_size: float) -> int:
    """
    Calculate decimal precision from step size
    Example: 0.001 → 3
    """
    step_str = f"{step_size:.10f}".rstrip("0")
    if "." in step_str:
        return len(step_str.split(".")[1])
    return 0


def validate_order(symbol, side, order_type, quantity, price=None):
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    # ---------------- BASIC VALIDATION ----------------
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if order_type not in ["MARKET", "LIMIT", "STOP"]:
        raise ValueError("Invalid order type")

    if quantity is None or quantity <= 0:
        raise ValueError("Quantity must be positive")

    if order_type in ["LIMIT", "STOP"]:
        if price is None or price <= 0:
            raise ValueError(f"{order_type} order requires valid price")

    # ---------------- EXCHANGE RULES ----------------
    symbol_info = get_symbol_info(symbol)
    filters = {f["filterType"]: f for f in symbol_info["filters"]}

    # -------- LOT SIZE --------
    lot_size = filters.get("LOT_SIZE")
    min_qty = float(lot_size["minQty"])
    max_qty = float(lot_size["maxQty"])
    step_size = float(lot_size["stepSize"])

    if quantity < min_qty:
        raise ValueError(f"Quantity too small. Min: {min_qty}")

    if quantity > max_qty:
        raise ValueError(f"Quantity too large. Max: {max_qty}")

    # FIXED step size validation (NO FLOAT MODULO)
    precision = _get_precision(step_size)
    if round(quantity, precision) != quantity:
        raise ValueError(f"Quantity must follow step size: {step_size}")

    # -------- PRICE FILTER (for LIMIT / STOP) --------
    if order_type in ["LIMIT", "STOP"]:
        price_filter = filters.get("PRICE_FILTER")
        tick_size = float(price_filter["tickSize"])

        price_precision = _get_precision(tick_size)
        if round(price, price_precision) != price:
            raise ValueError(f"Price must follow tick size: {tick_size}")

    # -------- MIN NOTIONAL --------
    if price:
        min_notional = float(filters["MIN_NOTIONAL"]["notional"])
        notional = quantity * price

        if notional < min_notional:
            raise ValueError(
                f"Order value too small: {notional:.2f}, min: {min_notional}"
            )

    return symbol, side, order_type