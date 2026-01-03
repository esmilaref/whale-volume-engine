import requests
from datetime import datetime

# ==================== تنظیمات ====================
VOLUME_THRESHOLD = 15  # درصد تغییر حجم اولیه برای هشدار
EMOJIS = {
    "high_volume": "📈",
    "medium_volume": "⚡",
    "low_volume": "🔹"
}

# ==================== تابع امتیازدهی ====================
def score_signal(volume_change, liquidity, active_pairs):
    """
    محاسبه امتیاز سیگنال بر اساس تغییر حجم، نقدینگی و تعداد جفت‌های فعال
    امتیاز: 0 تا 100
    """
    score = 0
    # وزن‌دهی حجم
    if volume_change >= 50:
        score += 40
    elif volume_change >= 25:
        score += 25
    elif volume_change >= 15:
        score += 15

    # وزن‌دهی نقدینگی
    if liquidity >= 500_000:
        score += 30
    elif liquidity >= 100_000:
        score += 20
    elif liquidity >= 50_000:
        score += 10

    # وزن‌دهی تعداد جفت‌های فعال
    if active_pairs >= 5:
        score += 30
    elif active_pairs >= 3:
        score += 20
    elif active_pairs >= 1:
        score += 10

    return min(score, 100)

# ==================== فرمت پیام تلگرام ====================
def format_signal_message(coin_name, coin_symbol, pair, volume_change, liquidity, active_pairs):
    score = score_signal(volume_change, liquidity, active_pairs)

    # انتخاب شکلک بر اساس امتیاز
    if score >= 70:
        emoji = EMOJIS["high_volume"]
    elif score >= 40:
        emoji = EMOJIS["medium_volume"]
    else:
        emoji = EMOJIS["low_volume"]

    message = (
        f"{emoji} *MarketPlayer Alert*\n"
        f"━━━━━━━━━━━━━━\n"
        f"🏷️ Token: {coin_name} ({coin_symbol})\n"
        f"🔗 Pair: {pair}\n"
        f"💹 Volume Change: {volume_change:.2f}%\n"
        f"💧 Liquidity: ${liquidity:,.0f}\n"
        f"🔄 Active Pairs: {active_pairs}\n"
        f"🎯 Score: {score}/100\n"
        f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return message

# ==================== نمونه تابع گرفتن سیگنال ها ====================
def scan_all_pairs():
    """
    نمونه تابع که تغییر حجم همه جفت‌ها و ارزها رو بررسی می‌کنه
    خروجی: لیست پیام‌های آماده تلگرام
    """
    # این بخش با API صرافی مثل بایننس یا کوین‌گکو پر میشه
    # اینجا فقط نمونه ساختگی برای نمایش فرمت
    signals = []

    sample_data = [
        {"name": "Cardano", "symbol": "ADA", "pair": "ADA/USDT", "volume_change": 20, "liquidity": 120000, "active_pairs": 3},
        {"name": "Ethereum", "symbol": "ETH", "pair": "ETH/BTC", "volume_change": 55, "liquidity": 800000, "active_pairs": 7},
        {"name": "Solana", "symbol": "SOL", "pair": "SOL/USDT", "volume_change": 12, "liquidity": 60000, "active_pairs": 2},
    ]

    for coin in sample_data:
        if coin["volume_change"] >= VOLUME_THRESHOLD:
            msg = format_signal_message(
                coin_name=coin["name"],
                coin_symbol=coin["symbol"],
                pair=coin["pair"],
                volume_change=coin["volume_change"],
                liquidity=coin["liquidity"],
                active_pairs=coin["active_pairs"]
            )
            signals.append(msg)

    return signals
