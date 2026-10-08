from typing import Protocol

from domain.aggregates.trip import Trip
from domain.value_objects import TripId


class TripRepository(Protocol):
    def get(self, trip_id: TripId) -> Trip: ...
    def save(self, trip: Trip) -> None: ...