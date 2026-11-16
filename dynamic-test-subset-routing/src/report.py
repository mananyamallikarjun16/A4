"""Example downstream module that depends on the calculator."""

from .calculator import mean


def summary(values: list[float]) -> str:
    return f"average={mean(values):.2f}"
