import requests
from datetime import datetime

# ==================== تنظیمات تلگرام ====================
BOT_TOKEN = "8421756738:AAFeLglRcghEEBmkESvz-8oHBCznfm5Zt38"
CHAT_ID = 131349718  # چت آی‌دی

# ==================== ارسال پیام تلگرام ====================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print(f"✅ پیام ارسال شد: {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"❌ خطا در ارسال پیام: {response.text}")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")

# ==================== ارسال سیگنال ====================
def send_signal(signal_data):
    """
    ایجاد و ارسال سیگنال تلگرامی
    """
    symbol = signal_data['symbol']
    volume_change = signal_data['volume_change_percent']
    score = signal_data['score']
    timeframe = signal_data['timeframe']
    volume = signal_data['volume']
    price = signal_data['price']

    # انتخاب شکلک بر اساس نوع سیگنال
    if volume_change >= 15:
        emoji = "🚀"
    elif volume_change >= 10:
        emoji = "⚡"
    else:
        emoji = "🔹"

    message = (
        f"{emoji} *New Market Player Signal - {symbol}*\n"
        f"━━━━━━━━━━━━━━\n"
        f"🏷️ Symbol: {symbol}\n"
        f"⏱️ Timeframe: {timeframe}\n"
        f"💰 Price: ${price:,.4f}\n"
        f"📊 Volume: {volume:,}\n"
        f"📈 Change: {volume_change:+.2f}%\n"
        f"🎯 Score: {score}\n"
        f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🔔 Action: Watch closely!"
    )

    send_telegram(message)
