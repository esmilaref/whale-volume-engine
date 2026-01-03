from replay_engine import check_and_replay
from telegram_bot import send_telegram

# ==================== مدیریت سیگنال‌ها ====================
def process_signals(signals):
    """
    سیگنال‌ها رو می‌گیره، امتیازدهی می‌کنه، بررسی حافظه ریپلی می‌کنه
    و در صورت نیاز به تلگرام ارسال می‌کنه
    """
    for sig in signals:
        # ==================== محاسبه امتیاز سیگنال ====================
        # مثال: حجم، نقدینگی و تعداد جفت‌های فعال
        volume_pct = sig.get("volume_change_pct", 0)
        liquidity = sig.get("liquidity", 0)
        active_pairs = sig.get("active_pairs", 1)

        # الگوریتم امتیازدهی ساده و قابل توسعه
        score = round((volume_pct * 2) + (liquidity/1000000) + active_pairs, 2)
        sig["score"] = score

        # ==================== تعیین آیدی یکتا ====================
        # ترکیب نام ارز و جفت
        signal_id = f"{sig['symbol']}_{sig['pair']}"

        # ==================== بررسی حافظه و ریپلی ====================
        if check_and_replay(signal_id, sig, score):
            # ==================== آماده‌سازی پیام تلگرام ====================
            emoji = "🔥" if score > 50 else "⚡" if score > 30 else "🔔"
            msg = (
                f"{emoji} *SIGNAL ALERT*\n"
                f"🏷️ Token: {sig['symbol']}\n"
                f"💹 Pair: {sig['pair']}\n"
                f"💰 Price: ${sig['price']:.6f}\n"
                f"📊 Volume Change: {sig['volume_change_pct']:.2f}%\n"
                f"💧 Liquidity: ${sig['liquidity']:.0f}\n"
                f"🎯 Score: {score}\n"
                f"🕒 Time: {sig['time']}"
            )
            send_telegram(msg)
