class Guess:
    def __init__(self, word: str, correction: str, is_correct: bool = False):
        self.word = word
        self.correction = correction
        self.is_correct = is_correct
