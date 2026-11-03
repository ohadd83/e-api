import pytest

from app.main import calculate_discount


def test_calculate_discount():

    result = calculate_discount(100, 10)

    assert result == 90


def test_zero_discount():

    result = calculate_discount(100, 0)

    assert result == 100


def test_full_discount():

    result = calculate_discount(100, 100)

    assert result == 0


def test_negative_price():

    with pytest.raises(ValueError):
        calculate_discount(-100, 10)


def test_invalid_discount():

    with pytest.raises(ValueError):
        calculate_discount(100, 150)
