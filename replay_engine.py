import json
from datetime import datetime

# ==================== حافظه ریپلی ====================
# این فایل ذخیره محلی برای سیگنال‌هایی هست که قبلا ارسال شدند
REPLAY_FILE = "replay_memory.json"

def load_memory():
    try:
        with open(REPLAY_FILE, "r") as f:
            memory = json.load(f)
        return memory
    except:
        return {}

def save_memory(memory):
    with open(REPLAY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# ==================== مدیریت سیگنال ====================
def check_and_replay(signal_id, signal_content, score):
    """
    بررسی می‌کنه که آیا سیگنال قبلا ارسال شده یا نه.
    اگر جدید بود، به حافظه اضافه می‌کنه و True برمی‌گردونه
    اگر قبلا بوده، بسته به تغییر امتیاز ممکنه دوباره ریپلی بده
    """
    memory = load_memory()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # اگر سیگنال جدید باشه
    if signal_id not in memory:
        memory[signal_id] = {"last_score": score, "last_time": now}
        save_memory(memory)
        return True  # ارسال جدید

    # اگر قبلا بود، بررسی تغییر امتیاز
    prev_score = memory[signal_id]["last_score"]
    if score != prev_score:
        memory[signal_id]["last_score"] = score
        memory[signal_id]["last_time"] = now
        save_memory(memory)
        return True  # ریپلی برای امتیاز جدید

    # هیچ تغییری نداشت
    return False
