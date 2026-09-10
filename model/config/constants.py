"""Fixed project constants for the AgriSence crop price forecasting scope.

These values represent the agreed project boundaries defined in the project proposal.
"""

MARKETS = ["Nairobi", "Nakuru", "Mombasa", "Kisumu", "Eldoret"]
CROPS = ["tomatoes", "kale", "onions"]
HORIZONS = ["1_month", "2_month"]

TOTAL_COMBINATIONS = len(MARKETS) * len(CROPS) * len(HORIZONS)
