from game import Game
from telegram import Update
from telegram.ext import Updater, CallbackContext
from utils import send_message
from exceptions import GameOverException, GuessException


opened_games = {}


def is_game_running(chat_id: int) -> bool:
    global opened_games

    return opened_games.get(chat_id) is not None


def help(update: Update, context: CallbackContext) -> None:
    initial_message = "*1.* Your goal is to discover what is the hidden word.\n"
    initial_message += "*2.* You have six guesses to find out.\n"
    initial_message += "*3.* Each guess must be an existent word.\n"
    initial_message += "*4.* Each time you guess a word, the letters of it will have one of the following colors:\n"
    initial_message += "\n"
    initial_message += "`  `- 🟩 Green: the letter is in the right place.\n"
    initial_message += "`  `- 🟪 Purple: the letter is on the word, but in the wrong place.\n"
    initial_message += "`  `- ⬛ Black: the letter isn't on the word.\n"
    initial_message += "\n"
    initial_message += "*5.* If you are not able to guess the word after 6 tries, you loose."

    send_message(update, initial_message)


def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "Welcome! This is a bot for the game Pyal, inspired by [Wordle](https://www.powerlanguage.co.uk/wordle/).\n"
    )
    welcome_message += "\n"
    welcome_message += "To play, use /play."

    send_message(update, welcome_message)


def play(update: Update, context: CallbackContext) -> None:
    global opened_games

    if is_game_running(update.effective_chat.id):
        send_message(update, "There's a game running already! Kill it with /kill.")
        return

    opened_games[update.effective_chat.id] = Game()
    send_message(update, "Game started! Use /guess to start playing.")


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

    user_guess = " ".join(context.args).lower()

    if not user_guess.replace(" ", ""):
        send_message(update, "Usage: /guess <guess>")
        return

    game = opened_games[update.effective_chat.id]

    try:
        guess_results = game.guess(user_guess)

        send_message(update, f"{guess_results.correction}\n{game.tries_left} tries remaining!")

    except GuessException as e:
        send_message(update, f"{str(e)}\n{game.tries_left} tries remaining!")

    except GameOverException as e:
        send_message(update, str(e))

        send_message(update, game.status())

        del opened_games[update.effective_chat.id]


def about(update: Updater, context: CallbackContext) -> None:
    message = "This bot was made only for learning purposes.\n"
    message += "\n"
    message += "Made by [rafomiya](https://github.com/rafomiya)"

    send_message(update, message)
