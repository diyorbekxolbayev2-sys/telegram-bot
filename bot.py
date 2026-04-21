import asyncio
import schedule
import time
import threading
import anthropic
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
ANTHROPIC_API_KEY  = "YOUR_ANTHROPIC_KEY"

CHANNELS = [
    "@your_channel",
]

POST_TIMES = ["09:00", "14:00", "19:00"]

CONTENT_TYPES = [
    {
        "type": "motivatsiya",
        "prompt": "O’zbek tilida qisqa va kuchli motivatsion post yoz. 3-4 qator, emoji bilan."
    },
    {
        "type": "qiziqarli_fakt",
        "prompt": "O’zbek tilida qiziqarli fakt yoz. 3-5 qator, emoji bilan."
    },
]

def generate_content():
    import random
    content_type = random.choice(CONTENT_TYPES)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=300,
            messages=[
                {"role": "user", "content": content_type["prompt"]}
            ]
        )
        return message.content[0].text.strip()

    except Exception as e:
        return "🚀 Bugun yangi imkoniyatlar kuni!"

async def send_post():
    content = generate_content()
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    for channel in CHANNELS:
        try:
            await bot.send_message(chat_id=channel, text=content)
            await asyncio.sleep(1)
        except TelegramError as e:
            print(e)

def run_post():
    asyncio.run(send_post())

def setup_schedule():
    for t in POST_TIMES:
        schedule.every().day.at(t).do(run_post)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(30)

def main():
    setup_schedule()

    thread = threading.Thread(target=run_scheduler)
    thread.start()

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
