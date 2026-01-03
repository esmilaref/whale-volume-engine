import time
from datetime import datetime
from threading import Thread

from volume_engine_v2 import scan_all_pairs  # موتور حجم پیشرفته
from signal_manager import process_signals    # مدیریت سیگنال‌ها با امتیاز و ریپلی

from telegram_bot import send_telegram        # ارسال تلگرام

# ==================== چرخه اصلی ربات ====================
def main_loop():
    cycle = 0
    send_telegram(
        "🤖 *MarketPlayer Bot Activated - V14*\n"
        "━━━━━━━━━━━━━━\n"
        "🔍 اسکن تمام جفت‌ها و ارزها با تمرکز روی تغییر حجم مشکوک و ورود بازیگر\n"
        "🎯 سیستم امتیازدهی و حافظه ریپلی فعال\n"
        "⏰ فرکانس: هر 3 دقیقه"
    )

    while True:
        try:
            cycle += 1
            print(f"\n🌀 چرخه #{cycle} - {datetime.now().strftime('%H:%M:%S')}")

            # ==================== گرفتن سیگنال‌ها ====================
            signals = scan_all_pairs()  # تمام جفت‌ها و تایم فریم‌ها

            if signals:
                print(f"✅ {len(signals)} سیگنال جدید")
                process_signals(signals)  # پردازش، امتیازدهی، ریپلی و ارسال به تلگرام
            else:
                print("🔍 هیچ سیگنالی یافت نشد")

            print("💤 انتظار 3 دقیقه...")
            time.sleep(180)  # چرخه بعدی
        except KeyboardInterrupt:
            send_telegram("🛑 MarketPlayer Bot متوقف شد")
            break
        except Exception as e:
            print(f"⚠️ خطا در چرخه اصلی: {e}")
            time.sleep(60)

# ==================== اجرای ربات ====================
if __name__ == "__main__":
    main_thread = Thread(target=main_loop, daemon=True)
    main_thread.start()
    main_thread.join()
