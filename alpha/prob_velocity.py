import numpy as np
import logging
from alpha.base_strategy import BaseStrategy


class ProbabilityVelocityStrategy(BaseStrategy):
    """
    Indicator-less quantitative strategy that models asset price returns velocity.
    Evaluates rolling standard deviation distribution (Z-Scores) instead of
    relying on lagging technical crossover charts.
    """

    def __init__(self, lookback_window: int = 50, entry_threshold_z: float = 1.5):
        super().__init__(name="ProbabilityVelocityEngine")
        self.lookback = lookback_window
        self.threshold = entry_threshold_z

    def generate_signal(self, price_matrix: np.ndarray) -> int:
        """
        Processes multi-dimensional array prices and evaluates standard dev bands.
        Returns:
            1  -> Strong Buy (Underpriced / Compressed Downward)
            -1 -> Strong Sell (Overpriced / Overextended Upward)
            0  -> Neutral State (Balanced Distribution)
        """
        # 1. Structural Validation Protection Check
        if price_matrix is None or price_matrix.size < self.lookback:
            logging.warning(
                f"Alpha Core: Insufficient price history matrix capacity. "
                f"Available size: {price_matrix.size if price_matrix is not None else 0}/{self.lookback}"
            )
            return 0

        try:
            # 2. Extract out the exact historical slice matching our lookback window
            target_slice = price_matrix[-self.lookback:]

            # 3. Calculate mathematical log returns (Asset Price Velocity)
            # Log returns prevent skew anomalies during high market volatility sessions
            log_returns = np.diff(np.log(target_slice))

            # 4. Generate statistical rolling matrices
            mean_velocity = np.mean(log_returns)
            std_velocity = np.std(log_returns)
            current_velocity = log_returns[-1]

            # 5. Formulate standard deviation profile (Z-Score)
            # Protect against division-by-zero crashes in flat sideways markets
            if std_velocity > 0:
                z_score = (current_velocity - mean_velocity) / std_velocity
            else:
                z_score = 0.0

            logging.info(
                f"📊 [Alpha Math Core] Current Velocity: {current_velocity:.8f} | "
                f"Rolling Mean: {mean_velocity:.8f} | Standard Deviation: {std_velocity:.8f} | "
                f"Z-Score Output: {z_score:.4f}"
            )

            # 6. Evaluate Statistical Expectancy Anomalies (Mean Reversion Triggers)
            if z_score > self.threshold:
                logging.info(
                    f"⚠️ Extreme Upward Outlier Detected (Z > {self.threshold}). Distribution favors SHORT snapback.")
                return -1

            elif z_score < -self.threshold:
                logging.info(
                    f"⚠️ Extreme Downward Outlier Detected (Z < -{self.threshold}). Distribution favors LONG snapback.")
                return 1

            # Distribution is balanced within standard mathematical probability tolerances
            return 0

        except Exception as error:
            logging.error(f"❌ Critical Failure inside Alpha Strategy Calculation Block: {error}")
            return 0
