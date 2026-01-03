import json
from datetime import datetime

MEMORY_FILE = "whale_memory.json"

# ==================== بارگذاری حافظه ====================
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# ==================== ذخیره حافظه ====================
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# ==================== افزودن سیگنال جدید ====================
def add_signal(signal_data):
    """
    سیگنال جدید را در حافظه ذخیره می‌کند.
    اگر سیگنال قبلا وجود داشته باشد، فقط تغییر حجم اضافه می‌شود.
    """
    memory = load_memory()
    symbol = signal_data["symbol"]
    pair = signal_data["pair"]
    timeframe = signal_data["timeframe"]
    key = f"{symbol}_{pair}_{timeframe}"

    if key in memory:
        # اگر سیگنال موجود است، فقط تاریخ و حجم اضافه شود
        memory[key]["history"].append({
            "volume_change": signal_data["volume_change_percent"],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # بروز رسانی امتیاز
        memory[key]["score"] = max(memory[key]["score"], signal_data["score"])
    else:
        # سیگنال جدید
        memory[key] = {
            "symbol": symbol,
            "pair": pair,
            "timeframe": timeframe,
            "score": signal_data["score"],
            "history": [{
                "volume_change": signal_data["volume_change_percent"],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }]
        }

    save_memory(memory)
    return memory[key]

# ==================== گرفتن تمام سیگنال‌ها ====================
def get_all_signals():
    return load_memory()
