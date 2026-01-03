import requests
from datetime import datetime
import time

# ==================== تنظیمات ====================
MIN_VOLUME_CHANGE = 15  # درصد افزایش حجم برای ارسال سیگنال
TIMEFRAMES = ["5m", "10m", "30m", "1h", "4h", "12h", "1d", "1w", "1M"]  # تایم فریم‌ها
MAX_COINS = 5000  # حداکثر تعداد ارز برای بررسی

# حافظه ریپلی
REPLAY_MEMORY = {}

# ==================== شبیه‌سازی گرفتن داده‌های حجم ====================
def get_market_data():
    """
    این تابع فرضی داده بازار رو میاره. تو نسخه واقعی باید با صرافی وصل بشه
    یا API معتبری برای گرفتن حجم واقعی هر جفت ارز استفاده بشه
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }

    all_coins = []
    for page in range(1, (MAX_COINS // 250) + 1):
        params["page"] = page
        response = requests.get(url, params=params, timeout=15)
        coins = response.json()
        if not coins:
            break
        all_coins.extend(coins)
        time.sleep(0.5)
    return all_coins

# ==================== محاسبه تغییر حجم ====================
def calculate_volume_change(old, new):
    if old == 0:
        return 0
    return ((new - old) / old) * 100

# ==================== اسکن تمام جفت‌ها ====================
def scan_all_pairs():
    signals = []
    data = get_market_data()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for coin in data:
        symbol = coin.get("symbol", "").upper()
        name = coin.get("name", "")
        price = coin.get("current_price", 0)
        volume = coin.get("total_volume", 0)
        market_cap = coin.get("market_cap", 0)

        # برای هر تایم فریم شبیه‌سازی تغییر حجم
        for tf in TIMEFRAMES:
            key = f"{symbol}_{tf}"
            old_volume = REPLAY_MEMORY.get(key, 0)
            change = calculate_volume_change(old_volume, volume)

            if abs(change) >= MIN_VOLUME_CHANGE:
                emoji = "📈" if change > 0 else "📉"
                signal = (
                    f"{emoji} *MarketPlayer Alert*\n"
                    f"━━━━━━━━━━━━━━\n"
                    f"🏷️ Token: {name} ({symbol})\n"
                    f"⏱️ Timeframe: {tf}\n"
                    f"💰 Price: `${price:,.4f}`\n"
                    f"📊 Volume Change: `{change:+.2f}%`\n"
                    f"🏦 Market Cap: `${market_cap:,.0f}`\n"
                    f"🕒 {now}\n"
                    f"🎯 Type: Sudden Volume Spike\n"
                    f"🔔 Pair: All available trading pairs"
                )
                signals.append(signal)

            # حافظه ریپلی به‌روز میشه
            REPLAY_MEMORY[key] = volume

    # مرتب‌سازی بر اساس درصد تغییر حجم
    signals.sort(key=lambda x: float(x.split("`")[1].replace("%","")), reverse=True)
    return signals
