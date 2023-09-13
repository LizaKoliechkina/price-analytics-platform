import pandas as pd
import numpy as np


def percentage_increase(numerator: float, denominator: float) -> float:
    result = ((numerator / denominator) - 1) * 100 if denominator != 0 else 0.0
    return round(result, 2)


def calculate_local_deviation(row: pd.Series) -> float:
    if np.isnan(row['global_price']) or (row['global_price'] == 0):
        return 0.0
    else:
        return percentage_increase(row['local_price'], row['global_price'])


def calculate_sales_increase(row: pd.Series) -> float:
    if np.isnan(row['previous_sold_quantity']) or (row['previous_sold_quantity'] == 0):
        return 0.0
    else:
        return percentage_increase(row['sold_quantity'], row['previous_sold_quantity'])
