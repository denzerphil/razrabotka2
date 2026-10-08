from enum import Enum

from domain.exceptions import DomainInvariantViolation
from domain.value_objects import BatteryLevel, ScooterId


class ScooterStatus(Enum):
    FREE = "free"
    RENTED = "rented"
    MAINTENANCE = "maintenance"


class Scooter:
    MIN_BATTERY_PERCENT = 15

    def __init__(self, scooter_id: ScooterId, battery: BatteryLevel):
        self._id = scooter_id
        self._battery = battery
        self._status = ScooterStatus.FREE

    @property
    def id(self) -> ScooterId:
        return self._id

    @property
    def status(self) -> ScooterStatus:
        return self._status

    @property
    def battery(self) -> BatteryLevel:
        return self._battery

    def ensure_available_for_rent(self) -> None:
        if self._status is not ScooterStatus.FREE:
            raise DomainInvariantViolation(
                f"Самокат не свободен (статус: {self._status.value})"
            )
        if self._battery.is_below(self.MIN_BATTERY_PERCENT):
            raise DomainInvariantViolation(
                f"Заряд {self._battery.percent}% ниже порога "
                f"{self.MIN_BATTERY_PERCENT}%"
            )

    def mark_rented(self) -> None:
        self.ensure_available_for_rent()
        self._status = ScooterStatus.RENTED

    def mark_free(self) -> None:
        if self._status is not ScooterStatus.RENTED:
            raise DomainInvariantViolation(
                "Освободить можно только арендованный самокат"
            )
        self._status = ScooterStatus.FREE

    def send_to_maintenance(self) -> None:
        if self._status is ScooterStatus.RENTED:
            raise DomainInvariantViolation(
                "Нельзя отправить на обслуживание арендованный самокат"
            )
        self._status = ScooterStatus.MAINTENANCE