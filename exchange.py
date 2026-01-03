import requests

BINANCE_API = "https://api.binance.com"

def get_all_spot_pairs():
    """
    دریافت تمام جفت‌ارزهای اسپات فعال از بایننس
    خروجی:
    [
        {
            'symbol': 'ADAUSDT',
            'base': 'ADA',
            'quote': 'USDT'
        },
        ...
    ]
    """
    url = f"{BINANCE_API}/api/v3/exchangeInfo"
    response = requests.get(url, timeout=15)
    data = response.json()

    pairs = []

    for s in data.get("symbols", []):
        if (
            s.get("status") == "TRADING"
            and s.get("isSpotTradingAllowed")
        ):
            pairs.append({
                "symbol": s["symbol"],
                "base": s["baseAsset"],
                "quote": s["quoteAsset"]
            })

    return pairs
