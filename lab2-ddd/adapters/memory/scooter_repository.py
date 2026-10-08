from domain.aggregates.scooter import Scooter
from domain.exceptions import DomainInvariantViolation
from domain.value_objects import ScooterId


class InMemoryScooterRepository:
    def __init__(self):
        self._items: dict[ScooterId, Scooter] = {}

    def get(self, scooter_id: ScooterId) -> Scooter:
        if scooter_id not in self._items:
            raise DomainInvariantViolation(
                f"Самокат {scooter_id.value} не найден"
            )
        return self._items[scooter_id]

    def save(self, scooter: Scooter) -> None:
        self._items[scooter.id] = scooter