import os
from typing import Any, Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

TOKEN: Final = os.getenv("TOKEN") or ""
BOT_USERNAME: Final = os.getenv("BOT_USERNAME") or ""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Hello, I am telegram bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("I am telegram bot, send me some text. ")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("This is custom command.")


def handle_response(text: Any) -> str:
    text = text.lower()
    if "hello" in text:
        return "Hey there"
    if "how are you" in text:
        return "I am good"
    if "I love python" in text:
        return "remeber to subscribe"
    return "I do not understand what you wrote ..."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        messgae_type: str = update.message.chat.type
        text = update.message.text
        print(f'User ({update.message.chat.id}) in {messgae_type}: "{text}"')
    if messgae_type == "group":
        if text and BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print("Bot: ", response)
    if update.message:
        await update.message.reply_text(response)


async def error(update: Any, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# if __name__ == "__main__":
def run() -> None:
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("Pooling ...")
    app.run_polling(poll_interval=3)
