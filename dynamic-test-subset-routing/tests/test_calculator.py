import pytest

from src.calculator import add, mean


def test_add() -> None:
    assert add(2, 3) == 5


def test_mean_rejects_empty_values() -> None:
    with pytest.raises(ValueError, match="at least one"):
        mean([])
