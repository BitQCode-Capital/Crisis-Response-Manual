import ccxt
import os, time
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize Binance Futures connection
exchange = ccxt.binance({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,
    "options": {"defaultType": "future"},
})

def close_long_in_chunks(symbol="SOL/USDT", total_qty=8486.84, chunk_size=400):
    order_side = "sell"          # opposite of long
    position_side = "LONG"       # required for hedge mode
    remaining = total_qty
    chunk = 1

    print(f"⚙️  Closing {total_qty} {symbol} long in {chunk_size}-SOL chunks...")

    while remaining > 0:
        this_qty = min(remaining, chunk_size)
        try:
            order = exchange.create_market_order(
                symbol=symbol,
                side=order_side,
                amount=round(this_qty, 3),
                params={
                    "positionSide": position_side
                }
            )
            print(f"✅ Chunk {chunk}: closed {this_qty} {symbol} | Order ID: {order['id']}")
            remaining -= this_qty
            time.sleep(0.25)
        except Exception as e:
            msg = str(e)
            if "greater than max quantity" in msg:
                chunk_size = max(100, chunk_size // 2)
                print(f"⚠️ Chunk too big → reducing chunk size to {chunk_size}")
            else:
                print(f"❌ Chunk {chunk} failed: {msg}")
                break
        chunk += 1

    print(f"🎯 Done. Closed {total_qty - remaining}, Remaining {remaining}")

if __name__ == "__main__":
    close_long_in_chunks("SOL/USDT", 8486.84, chunk_size=400)
