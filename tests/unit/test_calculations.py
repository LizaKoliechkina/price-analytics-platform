import pandas as pd
import pytest

from calculations import calculate_sales_increase, calculate_local_deviation


@pytest.mark.parametrize(
    'row, expected_increase',
    (
            ({'sold_quantity': 1, 'previous_sold_quantity': 0}, 0),
            ({'sold_quantity': 0, 'previous_sold_quantity': 0}, 0),
            ({'sold_quantity': 70, 'previous_sold_quantity': 8}, 775),
            ({'sold_quantity': 187, 'previous_sold_quantity': 450}, -58.44),
            ({'sold_quantity': 98, 'previous_sold_quantity': 29}, 237.93),
    )
)
def test_calculate_sales_increase(row: dict, expected_increase: float) -> None:
    product_data = pd.Series(row)
    result = calculate_sales_increase(product_data)
    assert result == expected_increase


@pytest.mark.parametrize(
    'row, expected_deviation',
    (
            ({'local_price': -1, 'global_price': 0}, 0),
            ({'local_price': 77, 'global_price': 89}, -13.48),
            ({'local_price': 98, 'global_price': 29}, 237.93),
    )
)
def test_calculate_local_deviation(row: dict, expected_deviation: float) -> None:
    product_data = pd.Series(row)
    result = calculate_local_deviation(product_data)
    assert result == expected_deviation
