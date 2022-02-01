from words import Word
from guess import Guess
from exceptions import GameException, GameOverException, WinException, LostException, GuessException


class Game:
    CORRECT = "🟩"
    ALMOST = "🟪"
    WRONG = "⬛"

    def get_word() -> str:
        return Word.random().upper()

    def __init__(self):
        self.hidden_word = Game.get_word()
        self.guesses = []
        self.tries_left = 6
        self.wrong_letters = set()
        self.included_letters = set()
        self.progress_so_far = ["_"] * 5
        self.ended = False

    def status(self) -> str:
        result = self.results()
        result += "\n\n"
        result += "WORD:\n"
        result += f"`{''.join(self.progress_so_far)}`"
        result += "\n\n"
        result += "MISPLACED LETTERS:\n"
        result += " ".join(self.included_letters)
        result += "\n\n"
        result += "WRONG LETTERS:\n"
        result += " ".join(self.wrong_letters)

        if not self.ended:
            result += "\n\n"
            result += f"{self.tries_left} tries remaining!"

        return result

    def word_exists(guess: str) -> bool:
        return Word.exists(guess.lower())

    def solve_guess(self, guess: str) -> bool:
        correction = ""
        for index, (guess_letter, word_letter) in enumerate(zip(guess, self.hidden_word)):
            if guess_letter not in self.hidden_word:
                correction += Game.WRONG
                self.wrong_letters.add(guess_letter)

            elif guess_letter == word_letter:
                correction += Game.CORRECT
                self.progress_so_far[index] = guess_letter

            else:  # letter is in the word, but in the wrong place
                amount_letter = self.hidden_word.count(guess_letter)
                for i, l in enumerate(self.hidden_word):
                    if l == guess_letter:
                        if guess[i] == guess_letter:
                            amount_letter -= 1

                if amount_letter == 0:
                    correction += Game.WRONG

                else:
                    correction += Game.ALMOST
                    self.included_letters.add(guess_letter)

        # remove from the self.included_letters if in the self.progress_so_far
        for letter in (i for i in self.progress_so_far if i != "_"):
            if letter in self.included_letters:
                self.included_letters.remove(letter)

        self.guesses.append(Guess(guess, correction))

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
            self.ended = True
            raise WinException(f"You won! The word was {self.hidden_word}.")

        if self.tries_left == 0:
            self.tries_left = -1
            self.ended = True
            raise LostException(f"You're out of guesses. The word was {self.hidden_word}.")

        return Guess(guess, guess_correction, is_guess_correct)

    def results(self) -> str:
        amount_steps_needed = 6 - self.tries_left if self.tries_left != -1 else "X"

        result = f"[{amount_steps_needed}/6](t.me/pyal_bot)\n"
        result += "\n"
        result += "\n".join(guess.correction for guess in self.guesses)

        return result


if __name__ == "__main__":
    game = Game(None)
    # print(game.hidden_word)
    while True:
        try:
            guess = game.guess(input("Guess: ").upper())

            print(game.status())

        except GuessException as e:
            print(str(e))

        except GameOverException as e:
            print(str(e))
            print(game.status())
            break
