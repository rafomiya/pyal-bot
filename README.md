# Pyal Telegram Bot

This is a simple telegram bot for the game Pyal, a word guessing game inspired by [Wordle](https://www.powerlanguage.co.uk/wordle/).

## How does it work?

Differently from the original game, you can play it multiple times a day, but the rules are the pretty much same:

1. Your goal is to discover what's the hidden word.
2. You have six guesses to find out.
3. Each guess must be an existent word.
4. Each time you guess a word, the letters of it will have one of the following colors:

    - 🟩 Green: the letter is in the right place.
    - 🟪 Purple: the letter is in the word, but in the wrong place.
    - ⬛ Black: the letter isn't on the word.

5. If you are not able to guess the word after 6 tries, you loose.

## Start playing!

All you have to do is send `/start` to [@pyal_bot](t.me/pyal_bot).
