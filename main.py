import time
from datetime import datetime
from threading import Thread
from volume_engine_v3 import scan_all_pairs
import requests

# ==================== تنظیمات ربات ====================
BOT_TOKEN = "8421756738:AAFeLglRcghEEBmkESvz-8oHBCznfm5Zt38"
CHAT_ID = 131349718

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=data, timeout=10)
        print(f"✅ پیام ارسال شد: {datetime.now().strftime('%H:%M:%S')}")
        return True
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")
        return False

# ==================== حلقه اصلی ====================
def main_loop():
    cycle = 0
    send_telegram(
        "🤖 *MarketPlayer Bot Activated*\n"
        "━━━━━━━━━━━━━━\n"
        "🔍 اسکن همه ارزها و تمام جفت‌ها\n"
        "🎯 تمرکز روی تغییر حجم مشکوک و ورود بازیگر\n"
        "⏰ فرکانس: هر 3 دقیقه"
    )

    while True:
        try:
            cycle += 1
            print(f"\n🌀 چرخه #{cycle} - {datetime.now().strftime('%H:%M:%S')}")
            signals = scan_all_pairs()
            if signals:
                print(f"✅ {len(signals)} سیگنال جدید")
                for sig in signals[:20]:  # فقط ۲۰ سیگنال برتر هر چرخه
                    send_telegram(sig)
                    time.sleep(1)
            else:
                print("🔍 هیچ سیگنالی یافت نشد")

            print("💤 انتظار 3 دقیقه...")
            time.sleep(180)

        except KeyboardInterrupt:
            send_telegram("🛑 MarketPlayer Bot متوقف شد")
            break
        except Exception as e:
            print(f"⚠️ خطا در حلقه اصلی: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main_thread = Thread(target=main_loop, daemon=True)
    main_thread.start()
    main_thread.join()
