from domain.aggregates.trip import Trip
from domain.exceptions import DomainInvariantViolation
from domain.value_objects import TripId


class InMemoryTripRepository:
    def __init__(self):
        self._items: dict[TripId, Trip] = {}

    def get(self, trip_id: TripId) -> Trip:
        if trip_id not in self._items:
            raise DomainInvariantViolation(f"Поездка {trip_id.value} не найдена")
        return self._items[trip_id]

    def save(self, trip: Trip) -> None:
        self._items[trip.id] = trip