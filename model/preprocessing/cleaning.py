"""Cleaning utilities for missing values and outlier handling.

The approach applies forward-fill for short gaps and an IQR-based method for anomalous
price observations before forecasting features are generated.
"""

from __future__ import annotations

import pandas as pd


def forward_fill_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill short missing value gaps in a time series DataFrame."""
    # TODO: apply forward fill with a controlled maximum gap threshold.
    return df.copy()


def flag_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Flag values that are outside the IQR-based outlier bounds for a column."""
    # TODO: compute Q1/Q3, identify outliers, and add a flag column.
    return df.copy()
