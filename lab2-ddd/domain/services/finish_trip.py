from datetime import datetime

from domain.aggregates.scooter import Scooter
from domain.aggregates.trip import Trip
from domain.ports.scooter_repository import ScooterRepository
from domain.ports.trip_repository import TripRepository
from domain.value_objects import Money, TripId


class FinishTripService:
    """
    Доменный сервис: завершение поездки — тоже операция над двумя агрегатами.
    """

    def __init__(
        self,
        scooters: ScooterRepository,
        trips: TripRepository,
    ):
        self._scooters = scooters
        self._trips = trips

    def finish(
        self,
        trip_id: TripId,
        ended_at: datetime,
        price_per_minute: Money,
        min_price: Money,
    ) -> Money:
        trip = self._trips.get(trip_id)
        scooter: Scooter = self._scooters.get(trip.scooter_id)

        cost = trip.finish(ended_at, price_per_minute, min_price)
        scooter.mark_free()

        self._trips.save(trip)
        self._scooters.save(scooter)
        return cost