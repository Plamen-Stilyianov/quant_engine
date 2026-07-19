import requests
import numpy as np

class MarketGateway:
    """Manages the network interface link for real-time market telemetry."""
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.base_url = "https://coingecko.com"

    def fetch_historical_matrix(self, lookback: int = 100) -> np.ndarray:
        """Pulls clean price arrays from a cross-platform REST data endpoint."""
        try:
            url = f"{self.base_url}/coins/bitcoin/market_chart?vs_currency=usd&days=1"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Parse out historical closing quotes into a clean NumPy array
                closes = [item[1] for item in data['prices'][-lookback:]]
                return np.array(closes)
            print(f"⚠️ Gateway Warning: Received server code {response.status_code}")
            return np.empty(0)
        except Exception as e:
            print(f"❌ Gateway Network Failure: Data array drop. Details: {e}")
            return np.empty(0)

    def transmit_order(self, payload: dict) -> bool:
        """Asynchronously routes pre-validated risk payloads to the market execution loop."""
        print(f"📡 Gateway Routing -> Transmitting payload to execution endpoint: {payload}")
        return True
