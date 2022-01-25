from telegram import Update, Message


def escape_special_chars(text: str) -> str:
    reserved_chars = "!._-+<>"

    for char in reserved_chars:
        text = text.replace(char, "\\" + char)

    return text


def send_message(update: Update, text: str, quote=True) -> Message:
    return update.message.reply_text(escape_special_chars(text), quote=quote)
