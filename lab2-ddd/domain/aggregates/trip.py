from datetime import datetime

from domain.exceptions import DomainInvariantViolation
from domain.value_objects import (
    Money,
    ScooterId,
    TimePeriod,
    TripId,
)


class Trip:
    def __init__(
        self,
        trip_id: TripId,
        scooter_id: ScooterId,
        started_at: datetime,
    ):
        self._id = trip_id
        self._scooter_id = scooter_id
        self._period = TimePeriod(started_at=started_at)
        self._cost: Money | None = None

    @property
    def id(self) -> TripId:
        return self._id

    @property
    def scooter_id(self) -> ScooterId:
        return self._scooter_id

    @property
    def period(self) -> TimePeriod:
        return self._period

    @property
    def cost(self) -> Money | None:
        return self._cost

    def is_finished(self) -> bool:
        return not self._period.is_open()

    def finish(
        self,
        ended_at: datetime,
        price_per_minute: Money,
        min_price: Money,
    ) -> Money:
        if self.is_finished():
            raise DomainInvariantViolation("Поездка уже завершена")

        # TimePeriod сам проверит, что ended_at >= started_at
        self._period = TimePeriod(
            started_at=self._period.started_at,
            ended_at=ended_at,
        )
        minutes = self._period.duration_minutes()
        total = Money(
            amount=price_per_minute.amount * minutes,
            currency=price_per_minute.currency,
        )
        if total.amount < min_price.amount:
            total = min_price
        self._cost = total
        return total