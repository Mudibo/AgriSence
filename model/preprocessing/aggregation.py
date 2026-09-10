"""Aggregation utilities for converting raw daily observations to monthly views."""

from __future__ import annotations

import pandas as pd


def aggregate_to_monthly(
    df: pd.DataFrame,
    group_cols: list[str],
    value_col: str,
) -> pd.DataFrame:
    """Aggregate a raw time series to monthly values by market, crop, and related groups."""
    # TODO: group by month and compute a summary statistic for the target column.
    return df.copy()
