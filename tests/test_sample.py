import pytest

from sample import add


@pytest.mark.parametrize(("x", "y", "correct"), [(1, 1, 2), (5, -1, 4)])
def test_add(x: int, y: int, correct: int) -> None:
    """
    加算処理のテスト

    Parameters
    ----------
    x : int
    y : int
    correct : int
        加算結果の正解値
    """
    assert add(x, y) == correct
