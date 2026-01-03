from datetime import datetime

# ==================== تابع امتیازدهی ====================
def score_signal(signal_data):
    """
    دریافت یک سیگنال از موتور حجم و محاسبه امتیاز آن
    signal_data باید شامل:
    - 'symbol': نام توکن
    - 'pair': جفت ارز
    - 'volume_change_percent': درصد تغییر حجم
    - 'liquidity': حجم نقدینگی
    - 'num_pairs': تعداد جفت‌هایی که حجم تغییر داشته
    """
    base_score = 0

    # امتیاز بر اساس درصد تغییر حجم
    vol_change = signal_data.get('volume_change_percent', 0)
    if vol_change >= 50:
        base_score += 50
    elif vol_change >= 30:
        base_score += 30
    elif vol_change >= 15:
        base_score += 15

    # امتیاز بر اساس نقدینگی
    liquidity = signal_data.get('liquidity', 0)
    if liquidity > 1_000_000:
        base_score += 20
    elif liquidity > 500_000:
        base_score += 10

    # امتیاز بر اساس تعداد جفت‌های فعال
    num_pairs = signal_data.get('num_pairs', 1)
    if num_pairs > 3:
        base_score += 20
    elif num_pairs > 1:
        base_score += 10

    # جمع نهایی
    signal_data['score'] = base_score
    signal_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # اضافه کردن شکلک برای سرعت تشخیص نوع سیگنال
    if base_score >= 80:
        signal_data['emoji'] = "🔥"  # نهنگ خیلی فعال
    elif base_score >= 50:
        signal_data['emoji'] = "🚀"  # نهنگ متوسط
    else:
        signal_data['emoji'] = "🐋"  # نهنگ ضعیف

    return signal_data

# ==================== قالب پیام تلگرام ====================
def format_signal_message(signal_data):
    msg = (
        f"{signal_data['emoji']} *MARKET PLAYER SIGNAL*\n"
        f"━━━━━━━━━━━━━━\n"
        f"🏷️ Token: {signal_data.get('symbol','')}\n"
        f"🌐 Pair: {signal_data.get('pair','')}\n"
        f"📊 Volume Change: `{signal_data.get('volume_change_percent',0):+.2f}%`\n"
        f"💧 Liquidity: `${signal_data.get('liquidity',0):,.0f}`\n"
        f"🎯 Active Pairs: {signal_data.get('num_pairs',1)}\n"
        f"⭐ Score: {signal_data.get('score',0)}\n"
        f"🕒 Time: {signal_data.get('timestamp','')}\n"
        f"━━━━━━━━━━━━━━"
    )
    return msg
