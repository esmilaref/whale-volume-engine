import json
from datetime import datetime, timedelta

MEMORY_FILE = "whale_memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(spike):
    """
    spike = {
        "symbol": "ADAUSDT",
        "timeframe": "5m",
        "volume_change_percent": 23.5
    }
    """
    memory = load_memory()
    key = f"{spike['symbol']}_{spike['timeframe']}"

    now = datetime.now().isoformat()
    if key in memory:
        memory[key]["last_seen"] = now
        memory[key]["count"] += 1
        memory[key]["last_percent"] = spike["volume_change_percent"]
    else:
        memory[key] = {
            "first_seen": now,
            "last_seen": now,
            "count": 1,
            "last_percent": spike["volume_change_percent"]
        }

    save_memory(memory)
    return memory[key]

def should_reply(spike, hours=24):
    """
    بررسی اینکه آیا ریپلی پیام لازم است
    """
    memory = load_memory()
    key = f"{spike['symbol']}_{spike['timeframe']}"
    if key not in memory:
        return True

    last_seen = datetime.fromisoformat(memory[key]["last_seen"])
    if datetime.now() - last_seen >= timedelta(hours=hours):
        return True
    return False

def get_score(spike):
    """
    امتیازدهی: درصد حجم + دفعات تکرار
    """
    mem = update_memory(spike)
    score = spike["volume_change_percent"] * mem["count"]
    return round(score, 2)
