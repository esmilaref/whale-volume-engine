from whale_memory import add_signal, get_all_signals
import requests
from datetime import datetime

BOT_TOKEN = "8421756738:AAFeLglRcghEEBmkESvz-8oHBCznfm5Zt38"
CHAT_ID = 131349718

# ==================== ارسال یا ریپلی پیام ====================
def send_signal(signal_data):
    memory_entry = add_signal(signal_data)

    # ساخت متن پیام
    emoji = "🐋" if memory_entry["score"] > 80 else "⚡"
    history_text = "\n".join([f"{h['time']}: {h['volume_change']}%" for h in memory_entry["history"]])
    
    message = (
        f"{emoji} *Market Player Alert*\n"
        f"🏷️ Token: {memory_entry['symbol']}\n"
        f"🌐 Pair: {memory_entry['pair']}\n"
        f"⏱ Timeframe: {memory_entry['timeframe']}\n"
        f"🎯 Score: {memory_entry['score']}\n"
        f"📊 Volume Change History:\n{history_text}\n"
        f"🕒 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # بررسی آیا پیام قبلا ارسال شده
    message_id = memory_entry.get("telegram_message_id")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        if message_id:
            # ریپلی پیام قبلی با editMessageText
            url_edit = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
            data_edit = {
                "chat_id": CHAT_ID,
                "message_id": message_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            r = requests.post(url_edit, json=data_edit, timeout=10)
        else:
            # پیام جدید
            r = requests.post(url, json=data, timeout=10)
            # ذخیره message_id در حافظه
            res = r.json()
            if res.get("ok"):
                memory_entry["telegram_message_id"] = res["result"]["message_id"]
        
        print(f"✅ پیام ارسال/بروزرسانی شد: {memory_entry['symbol']} ({memory_entry['pair']})")
        return True
    except Exception as e:
        print(f"❌ خطا در ارسال سیگنال: {e}")
        return False

# ==================== امتیازدهی سیگنال ====================
def compute_score(volume_change_percent, timeframe_minutes, repeat_count):
    """
    - درصد تغییر حجم بالاتر → امتیاز بالاتر
    - تایم فریم طولانی‌تر → کمی امتیاز بیشتر
    - تعداد دفعات تکرار → افزایش اعتماد
    """
    score = volume_change_percent  # پایه: درصد تغییر حجم
    if timeframe_minutes >= 60:
        score += 5
    if repeat_count > 1:
        score += min(repeat_count * 2, 20)  # سقف 20 امتیاز اضافه
    return min(score, 100)  # حداکثر 100
