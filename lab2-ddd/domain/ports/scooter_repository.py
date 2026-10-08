from typing import Protocol

from domain.aggregates.scooter import Scooter
from domain.value_objects import ScooterId


class ScooterRepository(Protocol):
    def get(self, scooter_id: ScooterId) -> Scooter: ...
    def save(self, scooter: Scooter) -> None: ...