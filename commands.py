from game import Game
from telegram import Update, Message
from telegram.ext import Updater, CallbackContext
from utils import send_message, edit_message
from exceptions import GameOverException, GuessException


class GameMessage(Game):
    def __init__(self, message: Message):
        super().__init__()
        self.error_message = ""
        self.message = message

    def status(self):
        message = super().status()
        message += f"\n\n{self.error_message}"

        self.error_message = ""

        return message

    def update_message(self):
        edit_message(self.message, self.status())


opened_games: "dict[int, GameMessage]" = {}


def get_game_message():
    return


def is_game_running(chat_id: int) -> bool:
    global opened_games

    return opened_games.get(chat_id) is not None


def help(update: Update, context: CallbackContext) -> None:
    initial_message = "*1.* Your goal is to discover what is the hidden word.\n"
    initial_message += "*2.* The hidden word is a five letter word.\n"
    initial_message += "*3.* You have six guesses to find out.\n"
    initial_message += "*4.* Each guess must be an existent word.\n"
    initial_message += "*5.* Each time you guess a word, the letters of your guess will have "
    initial_message += "one of the following colors:\n"
    initial_message += "\n"
    initial_message += "  - 🟩 Green: the letter is in the right place.\n"
    initial_message += "  - 🟪 Purple: the letter is on the word, but in the wrong place.\n"
    initial_message += "  - ⬛ Black: the letter isn't on the word.\n"
    initial_message += "\n"
    initial_message += "*6.* If you are not able to guess the word after 6 tries, you loose."

    send_message(update, initial_message)


def start(update: Update, context: CallbackContext) -> None:
    welcome_message = "Welcome! This is a bot for the game Pyal, "
    welcome_message += "inspired by [Wordle](https://www.powerlanguage.co.uk/wordle/).\n"
    welcome_message += "\n"
    welcome_message += "To play, use /play."

    send_message(update, welcome_message)


def play(update: Update, context: CallbackContext) -> None:
    global opened_games

    if is_game_running(update.effective_chat.id):
        send_message(update, "There's a game running already! Kill it with /kill.")
        return

    opened_games[update.effective_chat.id] = GameMessage(
        send_message(update, "Game started! Use /guess to guess the five letter hidden word.")
    )


def kill(update: Update, context: CallbackContext) -> None:
    global opened_games

    if is_game_running(update.effective_chat.id):
        del opened_games[update.effective_chat.id]
        send_message(update, "Game killed! Start it again with /play.")
        return

    send_message(update, "No game to kill! Start it with /play.")


def guess(update: Update, context: CallbackContext) -> None:
    global opened_games

    if not is_game_running(update.effective_chat.id):
        send_message(update, "No game running! Start it with /play")
        return

    user_guess = " ".join(context.args).upper()

    if not user_guess.replace(" ", ""):
        send_message(update, "Usage: /guess word")
        return

    game = opened_games[update.effective_chat.id]

    try:
        game.guess(user_guess)

    except GuessException as e:
        game.error_message = str(e)

    except GameOverException as e:
        game.error_message = str(e)

        if game.tries_left != -1:
            send_message(update, "Share your results!")

        send_message(update, game.results())

        del opened_games[update.effective_chat.id]

    game.update_message()


def about(update: Updater, context: CallbackContext) -> None:
    message = "This bot was made only for learning purposes.\n"
    message = "If you have any ideas or suggestions, you can create an issue at the bot's [github page](https://github.com/rafomiya/pyal-bot) :D\n"
    message += "\n"
    message += "Made by [rafomiya](https://github.com/rafomiya) <3"

    send_message(update, message)
