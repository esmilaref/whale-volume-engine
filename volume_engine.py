import requests
from statistics import mean

BINANCE_API = "https://api.binance.com"

TIMEFRAMES = {
    "5m":  "5m",
    "15m": "15m",
    "30m": "30m",
    "1h":  "1h",
    "4h":  "4h",
    "1d":  "1d",
    "1w":  "1w",
    "1M":  "1M"
}

def get_klines(symbol, interval, limit=50):
    """
    دریافت کندل‌ها از بایننس
    فقط حجم مهم است
    """
    url = f"{BINANCE_API}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    r = requests.get(url, params=params, timeout=15)
    return r.json()


def analyze_volume(symbol, interval):
    """
    بررسی تغییر حجم
    خروجی:
    {
        symbol,
        timeframe,
        volume_change_percent,
        current_volume,
        average_volume,
        is_spike
    }
    """
    klines = get_klines(symbol, interval)

    if len(klines) < 10:
        return None

    volumes = [float(k[5]) for k in klines[:-1]]  # حجم‌های قبلی
    current_volume = float(klines[-1][5])        # حجم کندل فعلی
    avg_volume = mean(volumes)

    if avg_volume == 0:
        return None

    change_percent = ((current_volume - avg_volume) / avg_volume) * 100

    return {
        "symbol": symbol,
        "timeframe": interval,
        "current_volume": round(current_volume, 2),
        "average_volume": round(avg_volume, 2),
        "volume_change_percent": round(change_percent, 2),
        "is_spike": change_percent >= 15  # آستانه نهنگی
  }
