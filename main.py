from telegram.ext import Updater, CommandHandler, Defaults
from telegram import ParseMode
from os import environ
from dotenv import load_dotenv
import logging
from commands import start, help, play, kill, guess, about


load_dotenv()
TELEGRAM_BOT_TOKEN = environ["TELEGRAM_BOT_TOKEN"]
PORT = environ.get("PORT", 8443)

config = Defaults(
    parse_mode=ParseMode.MARKDOWN_V2,
    disable_web_page_preview=True,
    allow_sending_without_reply=True,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def main():
    updater = Updater(
        token=TELEGRAM_BOT_TOKEN,
        use_context=True,
        defaults=config,
    )

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("play", play))
    dispatcher.add_handler(CommandHandler("kill", kill))
    dispatcher.add_handler(CommandHandler("guess", guess))
    dispatcher.add_handler(CommandHandler("about", about))

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url="https://pyal.herokuapp.com/" + TELEGRAM_BOT_TOKEN,
    )
    updater.idle()


if __name__ == "__main__":
    main()
