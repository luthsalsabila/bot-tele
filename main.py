import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

TOKEN = "8208041739:AAHUJhFP8zZh8Tz-TzindfCkIrC5lT8l6dc"
OWNER_ID = 1135074603  # ganti dengan chat ID owner kamu

logging.basicConfig(level=logging.INFO)

# Simpan user yang terakhir ngirim pesan supaya owner bisa reply
last_user = {}

def forward_to_owner(update, context):
    message = update.message
    user_id = message.chat_id
    full_name = message.from_user.full_name

    # Kalau user biasa -> forward ke owner
    if user_id != OWNER_ID:
        last_user[OWNER_ID] = user_id  # simpan user terakhir

        if message.text:
            context.bot.send_message(
                OWNER_ID,
                f"📩 Pesan dari {full_name} ({user_id}):\n\n{message.text}"
            )

        elif message.photo:
            context.bot.send_photo(
                OWNER_ID,
                photo=message.photo[-1].file_id,
                caption=f"📷 Foto dari {full_name} ({user_id})"
            )

        elif message.sticker:
            context.bot.send_sticker(
                OWNER_ID,
                sticker=message.sticker.file_id
            )

    # Kalau owner reply -> kirim ke user asli
    else:
        # Harus reply message
        if message.reply_to_message:
            target_id = last_user.get(OWNER_ID)

            if not target_id:
                message.reply_text("❌ Tidak ada user yang bisa dibalas.")
                return

            # Balas teks
            if message.text:
                context.bot.send_message(target_id, message.text)

            # Balas foto
            elif message.photo:
                context.bot.send_photo(
                    target_id,
                    photo=message.photo[-1].file_id
                )

            # Balas stiker
            elif message.sticker:
                context.bot.send_sticker(
                    target_id,
                    message.sticker.file_id
                )
        else:
            message.reply_text("Balas pesan user dengan *reply*, bukan pesan baru.")


def start(update, context):
    update.message.reply_text("Bot aktif dan siap menerima pesan!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Tangani semua pesan teks/foto/stiker
    dp.add_handler(MessageHandler(
        Filters.text | Filters.photo | Filters.sticker,
        forward_to_owner
    ))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
