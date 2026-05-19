import asyncio
import aiohttp
import json
import time

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from telegram.request import HTTPXRequest

# =========================================
# SETTINGS
# =========================================

TOKEN = "8879555764:AAF3SSlxHyoG6wWrKre9SGp0jovSWzsgsmc"

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

CHANNEL_1 = -1003514329629
CHANNEL_2 = -1002687883616

# =========================================

channel1_running = False
channel2_running = False

last_issue = ""

# =========================================
# ULTRA FAST HEADERS
# =========================================

HEADERS = {

    "User-Agent":
    "Mozilla/5.0",

    "Accept":
    "*/*",

    "Connection":
    "keep-alive",

    "Cache-Control":
    "no-cache",

    "Pragma":
    "no-cache"

}

# =========================================
# START PANEL
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "▶️ CHANNEL 1 START",
                callback_data="c1_start"
            )
        ],

        [
            InlineKeyboardButton(
                "⛔ CHANNEL 1 STOP",
                callback_data="c1_stop"
            )
        ],

        [
            InlineKeyboardButton(
                "▶️ CHANNEL 2 START",
                callback_data="c2_start"
            )
        ],

        [
            InlineKeyboardButton(
                "⛔ CHANNEL 2 STOP",
                callback_data="c2_stop"
            )
        ],

        [
            InlineKeyboardButton(
                "🚀 START BOTH",
                callback_data="both_start"
            )
        ],

        [
            InlineKeyboardButton(
                "🛑 STOP BOTH",
                callback_data="both_stop"
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await update.message.reply_text(
        "⚡ HACKII ULTRA FAST PANEL ⚡",
        reply_markup=reply_markup
    )

# =========================================
# BUTTON SYSTEM
# =========================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global channel1_running
    global channel2_running

    query = update.callback_query

    await query.answer()

    data = query.data

    if data == "c1_start":

        channel1_running = True

        await query.edit_message_text(
            "✅ CHANNEL 1 STARTED"
        )

    elif data == "c1_stop":

        channel1_running = False

        await query.edit_message_text(
            "⛔ CHANNEL 1 STOPPED"
        )

    elif data == "c2_start":

        channel2_running = True

        await query.edit_message_text(
            "✅ CHANNEL 2 STARTED"
        )

    elif data == "c2_stop":

        channel2_running = False

        await query.edit_message_text(
            "⛔ CHANNEL 2 STOPPED"
        )

    elif data == "both_start":

        channel1_running = True
        channel2_running = True

        await query.edit_message_text(
            "🚀 BOTH CHANNELS STARTED"
        )

    elif data == "both_stop":

        channel1_running = False
        channel2_running = False

        await query.edit_message_text(
            "🛑 BOTH CHANNELS STOPPED"
        )

# =========================================
# FAST SEND
# =========================================

async def fast_send(bot, chat_id, text):

    try:

        await bot.send_message(
            chat_id=chat_id,
            text=text,
            disable_web_page_preview=True
        )

    except Exception as e:

        print("SEND ERROR :", e)

# =========================================
# SUPER FAST FETCH
# =========================================

async def fast_fetch(session):

    try:

        url = API_URL + "?t=" + str(time.time_ns())

        async with session.get(
            url,
            ssl=False
        ) as response:

            text = await response.text()

            data = json.loads(text)

            return data

    except Exception as e:

        print("FETCH ERROR :", e)

        return None

# =========================================
# ULTRA FAST LOOP
# =========================================

async def ultra_fast_loop(app):

    global last_issue

    timeout = aiohttp.ClientTimeout(
        total=1
    )

    connector = aiohttp.TCPConnector(
        limit=0,
        ttl_dns_cache=300,
        ssl=False
    )

    async with aiohttp.ClientSession(

        timeout=timeout,

        connector=connector,

        headers=HEADERS

    ) as session:

        while True:

            try:

                data = await fast_fetch(
                    session
                )

                if not data:
                    continue

                latest = data["data"]["list"][0]

                issue = str(
                    latest["issueNumber"]
                )

                # INSTANT DETECT
                if issue != last_issue:

                    last_issue = issue

                    number = int(
                        latest["number"]
                    )

                    period = issue[-4:]

                    # BIG SMALL
                    if number <= 4:

                        bet = "SMALL"

                    else:

                        bet = "BIG"

                    msg = f"""🔺WINGO 1 MINUTE🔺

PERIOD ➖ {period}

NUMBER ➖ {number}

BET ON ➖ {bet}"""

                    tasks = []

                    # CHANNEL 1
                    if channel1_running:

                        tasks.append(

                            fast_send(
                                app.bot,
                                CHANNEL_1,
                                msg
                            )

                        )

                    # CHANNEL 2
                    if channel2_running:

                        tasks.append(

                            fast_send(
                                app.bot,
                                CHANNEL_2,
                                msg
                            )

                        )

                    if tasks:

                        await asyncio.gather(
                            *tasks
                        )

                        print(
                            "⚡ INSTANT SENT :",
                            issue
                        )

            except Exception as e:

                print(
                    "MAIN ERROR :",
                    e
                )

            # FASTEST SAFE SPEED
            await asyncio.sleep(0.02)

# =========================================
# STARTUP
# =========================================

async def startup(app):

    asyncio.create_task(
        ultra_fast_loop(app)
    )

# =========================================
# MAIN
# =========================================

def main():

    request = HTTPXRequest(

        connection_pool_size=2000,

        read_timeout=120,

        write_timeout=120,

        connect_timeout=120,

        pool_timeout=120

    )

    app = Application.builder() \
        .token(TOKEN) \
        .request(request) \
        .build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(buttons)
    )

    app.post_init = startup

    print("⚡ ULTRA FAST BOT RUNNING ⚡")

    app.run_polling(
        drop_pending_updates=True,
        close_loop=False
    )

# =========================================

if __name__ == "__main__":
    main()
