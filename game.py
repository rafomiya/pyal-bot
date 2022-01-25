from words import Word
from guess import Guess
from exceptions import WinException, LostException, GuessException


class Game:
    CORRECT = "🟩"
    ALMOST = "🟪"
    WRONG = "⬛"

    def get_word() -> str:
        return Word.random()

    def __init__(self):
        self.hidden_word = Game.get_word().lower()
        self.guesses = []
        self.tries_left = 6

    def status(self) -> str:
        amount_steps_needed = 6 - self.tries_left if self.tries_left != -1 else "X"

        result = f"[{amount_steps_needed}/6](t.me/pyal_bot)\n"
        result += "\n"
        result += "\n".join(guess.correction for guess in self.guesses)

        return result

    def word_exists(guess: str) -> bool:
        return Word.exists(guess)

    def solve_guess(self, guess: str) -> bool:
        correction = ""
        for guess_letter, word_letter in zip(guess, self.hidden_word):
            if guess_letter == word_letter:
                correction += Game.CORRECT
            elif guess_letter in self.hidden_word:
                correction += Game.ALMOST
            else:
                correction += Game.WRONG

        self.guesses.append(Guess(guess, correction, None))

        return correction

    def guess(self, guess: str) -> Guess:
        if len(guess) != 5:
            raise GuessException("Wrong amount of letters.")

        if not Game.word_exists(guess):
            raise GuessException("Not in word list.")

        self.tries_left -= 1

        guess_correction = self.solve_guess(guess)
        is_guess_correct = guess_correction == 5 * Game.CORRECT

        if is_guess_correct:
            raise WinException(f"You won! The word was {self.hidden_word}.")

        if self.tries_left == 0:
            self.tries_left = -1

            raise LostException(f"You're out of guesses. The word was {self.hidden_word}.")

        return Guess(guess, guess_correction, is_guess_correct)
