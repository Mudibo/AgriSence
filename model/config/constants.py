"""Fixed project constants for the AgriSence crop price forecasting scope.

"""

MARKETS = ["Nairobi", "Nakuru", "Mombasa", "Kisumu"]
CROPS = ["tomatoes", "kale", "onions"]
HORIZONS = ["1_month", "2_month"]

TOTAL_COMBINATIONS = len(MARKETS) * len(CROPS) * len(HORIZONS)
