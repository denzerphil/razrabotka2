class DomainError(Exception):
    """Базовое исключение доменного слоя."""


class DomainInvariantViolation(DomainError):
    """Нарушение бизнес-правила (инварианта) предметной области."""


class InvalidValueObject(DomainError):
    """Некорректное значение объекта-значения."""