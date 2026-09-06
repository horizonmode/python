from uuid import uuid4


class UuidBattleIdGenerator:
    def new_id(self) -> str:
        return uuid4().hex[:12].upper()
