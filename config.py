import os

SYMBOL = "EUR_USD"
POLLING_INTERVAL = 15

# Security Mapping: Pulled straight from your local Windows .env file
API_KEY = os.getenv("OANDA_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")

# Pre-Trade Risk Rules
MAX_DAILY_DRAWDOWN_PCT = 0.02
MAX_POSITION_SIZE = 0.1          # Standard institutional lot size allocation
DEFAULT_SL_POINTS = 200          # Mapped to points to stay 100% compatible with MT5
DEFAULT_TP_POINTS = 400
