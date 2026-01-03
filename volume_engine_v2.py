import time
import requests
from datetime import datetime
from signal_manager import send_signal, compute_score
from whale_memory import get_all_pairs, update_pair_volume

# ==================== تنظیمات ====================
BOT_TOKEN = "8421756738:AAFeLglRcghEEBmkESvz-8oHBCznfm5Zt38"
CHAT_ID = 131349718

TIMEFRAMES = [5, 10, 30, 60, 240, 1440, 10080, 43200]  # دقیقه: 5m,10m,30m,1h,4h,1d,1w,1M
VOLUME_THRESHOLD = 15  # درصد تغییر حجم برای ارسال سیگنال

# ==================== شبیه‌سازی داده بازار ====================
# در نسخه واقعی باید API صرافی یا دیتای لحظه‌ای جایگزین شود
def fetch_market_data(pair, timeframe):
    """
    - pair: جفت ارز مثلا 'ADA/USDT'
    - timeframe: دقیقه
    خروجی: درصد تغییر حجم در تایم فریم مشخص
    """
    # نمونه داده تصادفی برای تست
    import random
    return random.uniform(0, 50)  # درصد تغییر حجم بین 0 تا 50

# ==================== موتور حجم لحظه‌ای ====================
def volume_engine():
    print("🚀 Volume Engine Started - Monitoring all pairs")
    while True:
        try:
            all_pairs = get_all_pairs()  # لیست همه جفت ارزها از حافظه یا دیتابیس
            for pair in all_pairs[:5000]:  # محدود به 5000 جفت اول
                for tf in TIMEFRAMES:
                    volume_change = fetch_market_data(pair, tf)

                    if volume_change >= VOLUME_THRESHOLD:
                        # بررسی تعداد دفعات تکرار در حافظه
                        repeat_count = update_pair_volume(pair, tf, volume_change)
                        score = compute_score(volume_change, tf, repeat_count)
                        signal_data = {
                            "symbol": pair.split("/")[0],
                            "pair": pair,
                            "timeframe": f"{tf}m",
                            "volume_change": round(volume_change, 2),
                            "score": score,
                            "history": get_all_pairs()[pair]["history"]
                        }
                        send_signal(signal_data)

            # چرخه بعدی، هر 60 ثانیه
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Error in volume engine: {e}")
            time.sleep(10)
