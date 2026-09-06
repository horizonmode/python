from typing import Protocol


class BattleIdGenerator(Protocol):
    def new_id(self) -> str: ...
