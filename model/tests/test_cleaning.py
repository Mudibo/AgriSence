"""Tests for preprocessing cleaning logic."""

import pandas as pd

from preprocessing.aggregation import aggregate_to_monthly
from preprocessing.cleaning import (
    build_monthly_calendar,
    filter_target_scope,
    flag_outliers_iqr,
    forward_fill_short_gaps,
    normalize_units,
)


def test_normalize_units_and_filter_scope():
    frame = pd.DataFrame(
        {
            "market": ["Nairobi", "Nairobi"],
            "commodity": ["Maize (White)", "Maize"],
            "price": [90, 10],
            "unit": ["90 KG", "KG"],
        }
    )

    filtered = filter_target_scope(frame, ["Nairobi"], {"Maize (White)": "Maize"})
    normalized = normalize_units(filtered)

    assert normalized["commodity"].tolist() == ["Maize", "Maize"]
    assert normalized["price_per_kg"].tolist() == [1, 10]


def test_calendar_aggregation_and_short_gap_fill():
    calendar = build_monthly_calendar(
        ["Nairobi"], ["Maize"], "2020-01-15", "2020-03-20"
    )
    assert len(calendar) == 3

    observations = pd.DataFrame(
        {
            "market": ["Nairobi", "Nairobi"],
            "commodity": ["Maize", "Maize"],
            "date": ["2020-01-05", "2020-01-20"],
            "price_per_kg": [10, 20],
        }
    )
    monthly = aggregate_to_monthly(observations)
    assert monthly.loc[0, "avg_price_per_kg"] == 15

    panel = pd.DataFrame(
        {
            "market": ["Nairobi"] * 9,
            "commodity": ["Maize"] * 9,
            "month": pd.date_range("2020-01-01", periods=9, freq="MS"),
            "price_per_kg": [10, None, None, 40, 50, None, None, None, 90],
        }
    )
    filled = forward_fill_short_gaps(panel)
    assert filled.loc[1:2, "price_per_kg"].tolist() == [10, 10]
    assert filled.loc[5:7, "price_per_kg"].isna().all()


def test_outlier_flag_is_non_destructive():
    frame = pd.DataFrame(
        {
            "market": ["Nairobi"] * 5,
            "commodity": ["Maize"] * 5,
            "price_per_kg": [10, 11, 10, 11, 100],
        }
    )

    flagged = flag_outliers_iqr(frame)

    assert "is_outlier" in flagged
    assert flagged.loc[4, "is_outlier"]
    assert flagged.loc[4, "price_per_kg"] == 100
