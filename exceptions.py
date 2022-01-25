class GameException(Exception):
    pass


class GuessException(GameException):
    pass


class GameOverException(GameException):
    pass


class WinException(GameOverException):
    pass


class LostException(GameOverException):
    pass
