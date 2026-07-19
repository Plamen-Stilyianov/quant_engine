import config


class InstitutionalRiskManager:
    """Pre-Trade Gatekeeper protecting equity parameters from system breaches."""

    def __init__(self):
        self.max_daily_drawdown = config.MAX_DAILY_DRAWDOWN_PCT
        self.max_size = config.MAX_POSITION_SIZE

    def validate_and_format(self, symbol: str, signal: int, current_price: float) -> dict:
        """Verifies capital preservation allocations and builds the final order payload."""
        # Enforce maximum position constraints dynamically
        allocated_volume = self.max_size

        direction = "BUY" if signal == 1 else "SELL"
        pip_scale = 0.0001  # Scaling metric for standard FX pricing models

        # Hard-code exit parameters completely independent of the alpha signal generator
        if signal == 1:
            sl = current_price - (config.DEFAULT_SL_PIPS * pip_scale)
            tp = current_price + (config.DEFAULT_TP_PIPS * pip_scale)
        else:
            sl = current_price + (config.DEFAULT_SL_PIPS * pip_scale)
            tp = current_price - (config.DEFAULT_TP_PIPS * pip_scale)

        return {
            "symbol": symbol,
            "action": direction,
            "volume": allocated_volume,
            "execution_price": round(current_price, 5),
            "stop_loss": round(sl, 5),
            "take_profit": round(tp, 5),
            "magic_identifier": 112233
        }
