from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from domain.exceptions import InvalidValueObject


@dataclass(frozen=True)
class ScooterId:
    value: UUID

    @staticmethod
    def new() -> "ScooterId":
        return ScooterId(uuid4())


@dataclass(frozen=True)
class TripId:
    value: UUID

    @staticmethod
    def new() -> "TripId":
        return TripId(uuid4())


@dataclass(frozen=True)
class BatteryLevel:
    percent: int

    def __post_init__(self):
        if not 0 <= self.percent <= 100:
            raise InvalidValueObject(
                f"Уровень заряда должен быть в диапазоне 0..100, "
                f"получено {self.percent}"
            )

    def is_below(self, threshold: int) -> bool:
        return self.percent < threshold


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidValueObject("Сумма не может быть отрицательной")
        if self.currency != "RUB":
            raise InvalidValueObject("Поддерживается только валюта RUB")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise InvalidValueObject("Нельзя складывать разные валюты")
        return Money(self.amount + other.amount)


@dataclass(frozen=True)
class TimePeriod:
    started_at: datetime
    ended_at: datetime | None = None

    def __post_init__(self):
        if self.ended_at is not None and self.ended_at < self.started_at:
            raise InvalidValueObject(
                "Время окончания не может быть раньше времени начала"
            )

    def is_open(self) -> bool:
        return self.ended_at is None

    def duration_minutes(self) -> int:
        if self.ended_at is None:
            raise InvalidValueObject("Поездка ещё не завершена")
        delta = self.ended_at - self.started_at
        return max(1, int(delta.total_seconds() // 60))