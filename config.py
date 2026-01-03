# ===============================
# Whale Volume Engine - Config
# ===============================

# ---- Telegram ----
BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
CHAT_ID = 131349718

# ---- Volume Detection ----
BASE_VOLUME_SPIKE = 15        # درصد شروع هشدار
REPLY_STEP = 10               # هر چند درصد ریپلی شود (هوشمند)
MAX_REPLY_HOURS = 24          # حافظه ریپلی (ساعت)

# ---- Timeframes (minutes) ----
TIMEFRAMES = [
    5,
    10,
    15,
    30,
    60,
    240,
    1440,     # Daily
    10080,    # Weekly
    43200     # Monthly
]

# ---- Market Scope ----
MAX_SYMBOLS = 5000            # تا ۵۰۰۰ ارز اول
SCAN_ALL_PAIRS = True         # همه pair ها (USDT, BTC, ETH, BNB ...)

# ---- Engine ----
SCAN_INTERVAL_SECONDS = 60    # اسکن لحظه‌ای (نه 1 دقیقه‌ای کند)
EXCHANGE_NAME = "BINANCE"

# ---- Emojis ----
EMOJI_UP = "🟢"
EMOJI_STRONG = "🔥"
EMOJI_WHALE = "🐳"
EMOJI_REPEAT = "🔁"
EMOJI_EXIT = "🟥"
