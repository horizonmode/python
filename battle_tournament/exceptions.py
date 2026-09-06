class BattleError(Exception):
    """Base exception for battle errors."""


class BattleLimitReachedError(BattleError):
    pass
