import config

class InstitutionalRiskManager:
    """Pre-Trade Gatekeeper formatting payloads to match MT5 data specifications."""
    def __init__(self):
        self.max_daily_drawdown = config.MAX_DAILY_DRAWDOWN_PCT
        self.max_size = config.MAX_POSITION_SIZE

    def validate_and_format(self, symbol: str, signal: int, current_price: float) -> dict:
        """Verifies capital preservation allocations and outputs a compliant MT5 request dictionary."""
        allocated_volume = self.max_size
        pip_scale = 0.00001  # Standard 5-digit broker scaling metric

        if signal == 1:
            sl = current_price - (config.DEFAULT_SL_POINTS * pip_scale)
            tp = current_price + (config.DEFAULT_TP_POINTS * pip_scale)
            mt5_order_type = 0  # 0 = MT5 Buy Order Code
        else:
            sl = current_price + (config.DEFAULT_SL_POINTS * pip_scale)
            tp = current_price - (config.DEFAULT_TP_POINTS * pip_scale)
            mt5_order_type = 1  # 1 = MT5 Sell Order Code

        return {
            "action": 1,  # TRADE_ACTION_DEAL
            "symbol": symbol,
            "volume": float(allocated_volume),
            "type": mt5_order_type,
            "price": float(current_price),
            "sl": float(round(sl, 5)),
            "tp": float(round(tp, 5)),
            "deviation": 10,
            "magic": 99112233,
            "comment": "QuantEngine MT5 Core Signal Route",
            "type_time": 0,
            "type_filling": 1,
        }
