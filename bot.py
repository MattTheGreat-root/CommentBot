import os
import random
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not RENDER_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL is not set")

TEXT_FILE = "comments.txt"

def load_texts(path: str) -> list[str]:
    if not os.path.exists(path):
        raise RuntimeError(f"{path} file not found")

    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

TEXTS = load_texts(TEXT_FILE)

if not TEXTS:
    raise RuntimeError("Text file is empty")


app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if update.message.chat.type not in ("group", "supergroup"):
        return

    if random.randint(1, 15) == 1:
        user = update.message.from_user.first_name
        roast_text = random.choice(TEXTS)
        await update.message.reply_text(f"{user} {roast_text}")

telegram_app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, roast)
)

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "ok"

async def setup():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(f"{RENDER_URL}/webhook")

if __name__ == "__main__":
    asyncio.run(setup())
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)