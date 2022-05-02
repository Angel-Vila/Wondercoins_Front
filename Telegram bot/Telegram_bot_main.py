from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Proximamente...")


token = open("TOKEN_TELEGRAM.txt").read()
updater = Updater(token=token, use_context=True)
start_handler = CommandHandler('start', start)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)

if __name__ == "__main__":
    updater.start_polling()
