"""Cleaning utilities for the WFP price dataset."""

from __future__ import annotations

import pandas as pd
import logging
from datetime import datetime
from itertools import product


LOGGER = logging.getLogger(__name__)


def filter_target_scope(df: pd.DataFrame, markets: list[str], raw_commodity_map: dict[str, str]) -> pd.DataFrame:
    """Filter markets and relabel commodities.

    Market and commodity values should already be standardized by stripping
    whitespace and title-casing before this function runs.
    """
    filtered = df[df["market"].isin(markets)].copy()
    filtered["commodity"] = filtered["commodity"].replace(raw_commodity_map)
    return filtered


def normalize_units(df: pd.DataFrame, price_col: str = "price", unit_col: str = "unit") -> pd.DataFrame:
    """Add ``price_per_kg`` for supported WFP units and flag others."""
    cleaned = df.copy()
    cleaned["price_per_kg"] = pd.NA
    kg_mask = cleaned[unit_col].eq("KG")
    ninety_kg_mask = cleaned[unit_col].eq("90 KG")
    cleaned.loc[kg_mask, "price_per_kg"] = cleaned.loc[kg_mask, price_col]
    cleaned.loc[ninety_kg_mask, "price_per_kg"] = cleaned.loc[ninety_kg_mask, price_col] / 90
    cleaned["price_per_kg"] = pd.to_numeric(cleaned["price_per_kg"], errors="coerce")
    unhandled = sorted(cleaned.loc[~(kg_mask | ninety_kg_mask), unit_col].dropna().unique())
    if unhandled:
        message = f"Unhandled unit values; price_per_kg set to NaN: {unhandled}"
        LOGGER.warning(message)
        print(message)
    return cleaned


def resolve_pricetype(df: pd.DataFrame, preferred: str = "Wholesale", pricetype_col: str = "pricetype") -> pd.DataFrame:
    """Print pricetype counts and retain only the preferred pricetype."""
    print(df.groupby(["market", "commodity", pricetype_col]).size().rename("records"))
    return df[df[pricetype_col].eq(preferred)].copy()


def resolve_label_overlap(df: pd.DataFrame, date_col: str = "date", group_cols: tuple[str, ...] = ("market", "commodity")) -> pd.DataFrame:
    """Average overlapping rows after commodity labels have been merged."""
    keys = [*group_cols, date_col]
    duplicate_mask = df.duplicated(keys, keep=False)
    print(f"Overlapping (market, commodity, date) rows averaged: {int(duplicate_mask.sum())}")
    if not duplicate_mask.any():
        return df.copy()
    rows = []
    for _, group in df.groupby(keys, sort=False, dropna=False):
        row = group.iloc[0].copy()
        if "price_per_kg" in group:
            row["price_per_kg"] = group["price_per_kg"].mean()
        if "price" in group:
            row["price"] = group["price"].mean()
        rows.append(row)
    return pd.DataFrame(rows, columns=df.columns).reset_index(drop=True)


def build_monthly_calendar(markets: list[str], crops: list[str], start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    """Return every market-crop combination for each month in the range."""
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date)
    start_month = datetime(start_date.year, start_date.month, 1)
    end_month = datetime(end_date.year, end_date.month, 1)
    months = []
    current_month = start_month
    while current_month <= end_month:
        months.append(current_month)
        next_year = current_month.year + (current_month.month == 12)
        next_month = 1 if current_month.month == 12 else current_month.month + 1
        current_month = datetime(next_year, next_month, 1)
    return pd.DataFrame(
        product(markets, crops, months),
        columns=["market", "commodity", "month"],
    )


def quantify_missingness(observed_df: pd.DataFrame, calendar_df: pd.DataFrame, join_cols: tuple[str, ...] = ("market", "commodity", "month")) -> pd.DataFrame:
    """Summarize missing calendar months by market and commodity."""
    observed = observed_df[list(join_cols)].drop_duplicates().assign(_observed=True)
    panel = calendar_df[list(join_cols)].merge(observed, on=list(join_cols), how="left")
    summary = panel.assign(_missing=panel["_observed"].isna()).groupby(list(join_cols[:-1]))["_missing"].agg(missing_months="sum", expected_months="size")
    summary["missing_proportion"] = summary["missing_months"] / summary["expected_months"]
    print(f"Overall missingness: {panel['_observed'].isna().mean():.2%}")
    return summary.reset_index()


def forward_fill_short_gaps(df: pd.DataFrame, value_col: str = "price_per_kg", max_gap_months: int = 2, group_cols: tuple[str, ...] = ("market", "commodity")) -> pd.DataFrame:
    """Fill only complete missing runs no longer than ``max_gap_months``."""
    result = df.copy().sort_values([*group_cols, "month"]).reset_index(drop=True)
    result["was_imputed"] = False
    for _, index in result.groupby(list(group_cols), sort=False).groups.items():
        labels = list(index)
        position = 0
        while position < len(labels):
            label = labels[position]
            if pd.notna(result.at[label, value_col]):
                position += 1
                continue
            gap_start = position
            while position < len(labels) and pd.isna(result.at[labels[position], value_col]):
                position += 1
            gap_length = position - gap_start
            if gap_length <= max_gap_months and gap_start > 0:
                previous_value = result.at[labels[gap_start - 1], value_col]
                if pd.notna(previous_value):
                    for gap_position in range(gap_start, position):
                        result.at[labels[gap_position], value_col] = previous_value
                        result.at[labels[gap_position], "was_imputed"] = True
    return result


def flag_outliers_iqr(df: pd.DataFrame, value_col: str = "price_per_kg", group_cols: tuple[str, ...] = ("market", "commodity"), multiplier: float = 1.5) -> pd.DataFrame:
    """Add ``is_outlier`` using group-wise IQR bounds without removing values."""
    result = df.copy()
    grouped = result.groupby(list(group_cols))[value_col]
    q1 = grouped.transform("quantile", 0.25)
    q3 = grouped.transform("quantile", 0.75)
    iqr = q3 - q1
    result["is_outlier"] = result[value_col].notna() & ((result[value_col] < q1 - multiplier * iqr) | (result[value_col] > q3 + multiplier * iqr))
    return result


def forward_fill_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Backward-compatible alias for short-gap filling."""
    return forward_fill_short_gaps(df)


