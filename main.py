import time
import os
import logging
import config
from core.orchestrator import QuantOrchestrator


def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(os.path.join(log_dir, "execution.log"))
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)


def bootstrap():
    setup_logging()
    logging.info("==================================================================")
    logging.info("🚀 Initializing Quant Engine System Orchestrator Bundle...")
    logging.info("⚙️ Execution Platform State: Python 3.13 Stable Container Layer")
    logging.info("==================================================================")

    orchestrator = QuantOrchestrator()

    try:
        while True:
            orchestrator.run_engine_cycle()
            time.sleep(config.POLLING_INTERVAL)
    except KeyboardInterrupt:
        logging.info("🔌 Interruption directive processed. Safe system shutdown complete.")


if __name__ == "__main__":
    bootstrap()
