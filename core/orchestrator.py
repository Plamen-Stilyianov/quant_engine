import time
import os
import csv
from datetime import datetime
import config
from core.gateway import MarketGateway
from alpha.prob_velocity import ProbabilityVelocityStrategy
from risk.risk_manager import InstitutionalRiskManager


class QuantOrchestrator:
    """The central core execution engine routing event traffic between components."""

    def __init__(self):
        self.gateway = MarketGateway(symbol=config.SYMBOL)
        self.strategy = ProbabilityVelocityStrategy(lookback_window=50, entry_threshold_z=1.5)
        self.risk_manager = InstitutionalRiskManager()

    def run_engine_cycle(self):
        print(f"\n🔄 Polling fresh data matrix arrays for {config.SYMBOL}...")

        data_matrix = self.gateway.fetch_historical_matrix(lookback=100)
        if data_matrix.size == 0:
            return

        current_price = data_matrix[-1]
        signal = self.strategy.generate_signal(data_matrix)

        if signal != 0:
            print(f"🎯 Actionable strategy signal detected ({signal}). Querying risk gates...")
            trade_payload = self.risk_manager.validate_and_format(config.SYMBOL, signal, current_price)

            if trade_payload:
                self.gateway.transmit_order(trade_payload)

                try:
                    # Strictly translate the alpha signal output:
                    # signal == 1  --> BUY (0)
                    # signal == -1 --> SELL (1)
                    execution_side = 0 if signal == 1 else 1

                    log_trade_to_csv(
                        symbol=trade_payload.get('symbol', config.SYMBOL),
                        side=execution_side,  # ◄ FIXED: Prevents everything defaulting to 1 (SELL)
                        price=trade_payload.get('price', current_price),
                        volume=trade_payload.get('volume', 0.1),
                        sl=trade_payload.get('sl', 0.0),
                        tp=trade_payload.get('tp', 0.0),
                        magic=trade_payload.get('magic', 99112233)
                    )
                    print("✅ Transaction packet logged successfully to /app/logs/trades.csv")
                except Exception as csv_error:
                    print(f"⚠️ Telemetry mapping intercept failed: {csv_error}")

        else:
            print("⚖️ Market distribution is normal. Holding positions.")


# ==============================================================================
# STANDALONE LOCAL LOGGER (Placed here to completely break the import deadlock)
# ==============================================================================
def log_trade_to_csv(symbol, side, price, volume, sl, tp, magic):
    """
    Appends execution payloads directly to /app/logs/trades.csv
    bypassing circular module dependency constraints.
    """
    csv_path = "/app/logs/trades.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    file_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0

    action_string = "BUY" if side == 0 else "SELL"

    row_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Symbol": symbol,
        "Action": action_string,
        "Price": price,
        "Lots": volume,
        "StopLoss": sl,
        "TakeProfit": tp,
        "MagicID": magic
    }

    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)
