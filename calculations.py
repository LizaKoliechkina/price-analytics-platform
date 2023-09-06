import pandas as pd
import numpy as np


def calculate_local_deviation(row: pd.Series) -> float:
    if np.isnan(row['global_price']) or (row['global_price'] == 0):
        return 0.0
    else:
        return ((row['local_price'] / row['global_price']) - 1) * 100


def calculate_sales_increase(row: pd.Series) -> float:
    if np.isnan(row['previous_sold_quantity']) or (row['previous_sold_quantity'] == 0):
        return 100.0
    else:
        return ((row['sold_quantity'] / row['previous_sold_quantity']) - 1) * 100
