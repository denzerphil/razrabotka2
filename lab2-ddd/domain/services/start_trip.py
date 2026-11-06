from datetime import datetime

from domain.aggregates.trip import Trip
from domain.ports.scooter_repository import ScooterRepository
from domain.ports.trip_repository import TripRepository
from domain.value_objects import ScooterId, TripId


class StartTripService:
    """
    Доменный сервис: старт поездки затрагивает два агрегата — Scooter и Trip.
    Ни один из них в одиночку эту операцию выполнить не может.
    """

    def __init__(
        self,
        scooters: ScooterRepository,
        trips: TripRepository,
    ):
        self._scooters = scooters
        self._trips = trips

    def start(self, scooter_id: ScooterId, started_at: datetime) -> Trip:
        scooter = self._scooters.get(scooter_id)
        scooter.mark_rented()
        trip = Trip(
            trip_id=TripId.new(),
            scooter_id=scooter.id,
            started_at=started_at,
        )
        self._scooters.save(scooter)
        self._trips.save(trip)
        return trip