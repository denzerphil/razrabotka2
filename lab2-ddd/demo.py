from datetime import datetime, timedelta, timezone
from decimal import Decimal

from adapters.memory.scooter_repository import InMemoryScooterRepository
from adapters.memory.trip_repository import InMemoryTripRepository
from domain.aggregates.scooter import Scooter
from domain.exceptions import DomainInvariantViolation
from domain.services.finish_trip import FinishTripService
from domain.services.start_trip import StartTripService
from domain.value_objects import BatteryLevel, Money, ScooterId


def main() -> None:
    scooters = InMemoryScooterRepository()
    trips = InMemoryTripRepository()

    # Создаём самокат с достаточным зарядом
    scooter = Scooter(ScooterId.new(), BatteryLevel(80))
    scooters.save(scooter)

    start = StartTripService(scooters, trips)
    finish = FinishTripService(scooters, trips)

    t0 = datetime.now(timezone.utc)
    trip = start.start(scooter.id, t0)
    print(f"Поездка начата: {trip.id.value}, статус самоката: {scooter.status.value}")

    # Проверяем инвариант: нельзя начать поездку на уже арендованном самокате
    try:
        start.start(scooter.id, t0)
    except DomainInvariantViolation as e:
        print(f"Ожидаемая ошибка: {e}")

    # Завершаем поездку через 12 минут
    price_per_minute = Money(Decimal("5.00"))
    min_price = Money(Decimal("30.00"))
    cost = finish.finish(
        trip.id,
        t0 + timedelta(minutes=12),
        price_per_minute,
        min_price,
    )
    print(f"Поездка завершена, стоимость: {cost.amount} {cost.currency}")
    print(f"Статус самоката: {scooter.status.value}")

    # Пробуем завершить ещё раз
    try:
        finish.finish(
            trip.id,
            t0 + timedelta(minutes=20),
            price_per_minute,
            min_price,
        )
    except DomainInvariantViolation as e:
        print(f"Ожидаемая ошибка: {e}")

    # Пробуем создать самокат с некорректным зарядом
    try:
        BatteryLevel(150)
    except Exception as e:
        print(f"Ожидаемая ошибка: {e}")


if __name__ == "__main__":
    main()