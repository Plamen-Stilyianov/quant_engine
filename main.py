import time
import config
from core.orchestrator import QuantOrchestrator


def bootstrap():
    print("==================================================================")
    print("🚀 Initializing Quant Engine System Orchestrator Bundle...")
    print("==================================================================")

    # Initialize the runtime coordinator
    orchestrator = QuantOrchestrator()

    try:
        while True:
            orchestrator.run_engine_cycle()
            time.sleep(config.POLLING_INTERVAL)
    except KeyboardInterrupt:
        print("\n🔌 Interruption directive processed. Safe system shutdown complete.")


if __name__ == "__main__":
    bootstrap()
