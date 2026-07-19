import time
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

        # 1. Pull historical price arrays via Gateway
        data_matrix = self.gateway.fetch_historical_matrix(lookback=100)
        if data_matrix.size == 0:
            return

        current_price = data_matrix[-1]

        # 2. Extract signal calculation from the Alpha engine
        signal = self.strategy.generate_signal(data_matrix)

        # 3. If an actionable trade triggers, verify against pre-trade risk guardrails
        if signal != 0:
            print(f"🎯 Actionable strategy signal detected ({signal}). Querying risk gates...")
            trade_payload = self.risk_manager.validate_and_format(config.SYMBOL, signal, current_price)

            # 4. Transmit order through the execution gateway if approved
            if trade_payload:
                self.gateway.transmit_order(trade_payload)
        else:
            print("⚖️ Market distribution is normal. Holding positions.")
