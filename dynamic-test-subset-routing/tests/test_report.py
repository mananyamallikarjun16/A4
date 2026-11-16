from src.report import summary


def test_summary_uses_mean() -> None:
    assert summary([2, 4]) == "average=3.00"
