import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "8208041739:AAHUJhFP8zZh8Tz-TzindfCkIrC5lT8l6dc"
OWNER_ID = 1135074603  # ganti dengan chat_id owner kamu

logging.basicConfig(level=logging.INFO)

# Ketika user kirim pesan → bot teruskan ke owner
async def forward_to_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    if user_id != OWNER_ID:
        await context.bot.send_message(
            OWNER_ID,
            f"[DARI USER {user_id}]\n{text}"
        )
    else:
        # Owner balas pakai format: IDUSER pesan
        try:
            target, reply = text.split(" ", 1)
            await context.bot.send_message(int(target), reply)
        except:
            await update.message.reply_text("Format salah.\nContoh:\n123456789 Halo user!")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_owner))

print("Bot berjalan...")
app.run_polling()
