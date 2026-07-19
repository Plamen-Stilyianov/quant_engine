import numpy as np
from alpha.base_strategy import BaseStrategy


class ProbabilityVelocityStrategy(BaseStrategy):
    """Indicator-less statistical strategy measuring asset rate return velocity."""

    def __init__(self, lookback_window: int = 50, entry_threshold_z: float = 1.5):
        super().__init__(name="ProbabilityVelocityEngine")
        self.lookback = lookback_window
        self.threshold = entry_threshold_z

    def generate_signal(self, price_matrix: np.ndarray) -> int:
        if price_matrix.size < 10:
            return 0

        # Calculate mathematical price log returns
        returns = np.diff(price_matrix) / price_matrix[:-1]

        mean_vel = np.mean(returns)
        std_vel = np.std(returns)
        current_vel = returns[-1] if len(returns) > 0 else 0

        # Formulate statistical Z-Score distribution boundaries
        z_score = (current_vel - mean_vel) / std_vel if std_vel > 0 else 0
        print(f"📊 Quantitative Alpha Matrix -> Real-Time Price Velocity Z-Score: {z_score:.4f}")

        if z_score > self.threshold:
            return -1  # Overextended upwards -> Mean reversion correction
        elif z_score < -self.threshold:
            return 1  # Compressed downwards -> Mean reversion snapback

        return 0  # Balanced distribution state
