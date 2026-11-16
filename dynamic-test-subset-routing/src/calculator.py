"""Small example module used by the routing demonstration."""


def add(left: int, right: int) -> int:
    return left + right


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)
