from abc import ABC, abstractmethod
import numpy as np

class BaseStrategy(ABC):
    """Abstract Base Class layout defining strict strategy signature contracts."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_signal(self, price_matrix: np.ndarray) -> int:
        """
        Analyzes quantitative vectors.
        Returns: 1 (Buy), -1 (Sell), 0 (Neutral/Hold)
        """
        pass
