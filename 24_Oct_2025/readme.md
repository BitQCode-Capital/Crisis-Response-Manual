
---

# 🧾 Post-Mortem Report — Binance Position Closure Limitation

**Date:** 24-10-2025 

**Service:** Crypto Algorithmic Trading (Binance Futures) - M.G.

**Incident:** Exchange Rejection on Position Closure — `SOL/USDT:USDT`

**Severity:** Medium to High (Exchange-Driven Delay)

**Duration:** 30-45 minutes


---

## 🧩 **Summary**

During an automated short position closure on **Binance Futures**, the exchange unexpectedly **rejected a standard market-close order**, returning:

```
{"code": -4005, "msg": "Quantity greater than max quantity."}
```

This error originated from Binance’s internal **maximum order-size limitation**, which was not clearly documented or communicated through public API references.
As a result, the system’s initial request—well within typical operational parameters—was declined by the exchange.

A temporary workaround was deployed that submitted several smaller orders sequentially, which Binance accepted without issue.

---

## ⚠️ **Incident Details**

The incident was triggered by a manual test position placed within the firm’s internal matching engine (for documentation and screenshot purposes). The mismatch caused the internal matching logic to enter a large short position on Binance Futures.

The major incident was **Binance’s restrictive and undocumented quantity limits**, which prevented a valid market close order from executing.
Our trading infrastructure performed as designed, handling authentication, risk checks, and order logic correctly.
The new **chunk-based submission method** serves as a contingency for similar exchange-side limitations, ensuring uninterrupted trade execution even when external APIs behave unexpectedly.

### **Exchange Response**

* Error code: **–4005**
* Message: *“Quantity greater than max quantity.”*
* Behavior: Binance refused the closing order despite sufficient balance, margin, and account permissions.
* Impact: Position remained open for several minutes until smaller requests were accepted.


---

## 🧠 **Resolution**

To mitigate Binance’s restrictive order handling, a **chunk-based closing mechanism** was implemented:

* The total quantity (8,486.84 SOL) was split into smaller sub-orders (≈400 SOL each).
* Each chunk was sent sequentially with rate-limit-friendly timing.
* Binance successfully processed all partial orders.

This approach fully neutralized the position while working **within the exchange’s undocumented limitations**.

---

## 📊 **Impact Assessment**

| Area                     | Description                                                |
| ------------------------ | ---------------------------------------------------------- |
| **Exchange Reliability** | Binance’s API unexpectedly enforced a hidden quantity cap. |
| **Trading Operations**   | Temporary delay in closing the short position.             |
| **Capital Exposure**     | Slightly extended risk window due to exchange rejection.   |
| **Internal Systems**     | Functionality confirmed stable; failure caused externally. |

---

## 🪶 **Summary Statement**

Documentation, screenshots, and API key validations for new APIs must be completed before live trading. Support teams should be contacted, and all relevant parameters fixed prior to trading start — not during live execution. 

 A formal pre-trading API key check protocol must be implemented, including: verifying connectivity, permissions, account balances, and performing optional test orders. Sub-accounts or API keys must not be changed/deleted mid-strategy to avoid unexpected errors in trade operations. 
---
