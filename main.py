import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

TOKEN = "8208041739:AAHUJhFP8zZh8Tz-TzindfCkIrC5lT8l6dc"
OWNER_ID = 1135074603  # Ganti dengan chat_id owner

logging.basicConfig(level=logging.INFO)


# Ketika user kirim pesan → diteruskan ke owner
async def forward_to_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    text = update.message.text

    # Jika yang chat BUKAN owner → forward ke owner
    if user_id != OWNER_ID:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"[DARI USER {user_id}]\n{text}"
        )
    else:
        # Owner format: IDUSER pesan
        try:
            target, reply = text.split(" ", 1)
            await context.bot.send_message(chat_id=int(target), text=reply)
        except:
            await update.message.reply_text(
                "Format salah.\nContoh:\n123456789 Halo user!"
            )


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif!")


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_owner))

    print("Bot berjalan...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
