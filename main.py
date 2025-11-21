import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

TOKEN = "8208041739:AAHUJhFP8zZh8Tz-TzindfCkIrC5lT8l6dc"
OWNER_ID = 1135074603  # ganti dengan chat ID owner kamu

logging.basicConfig(level=logging.INFO)

# Ketika user kirim pesan -> dikirim ke owner
def forward_to_owner(update, context):
    user_id = update.message.chat_id
    text = update.message.text

    if user_id != OWNER_ID:
        context.bot.send_message(
            OWNER_ID,
            f"[DARI USER {user_id}]\n{text}"
        )
    else:
        # Owner balas pakai format: IDUSER pesan
        try:
            target, reply = text.split(" ", 1)
            context.bot.send_message(int(target), reply)
        except:
            update.message.reply_text("Format salah.\nContoh:\n123456789 Halo user!")

def start(update, context):
    update.message.reply_text("Bot aktif!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_to_owner))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
