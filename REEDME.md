# QuantEngine: High-Performance Algorithmic Trading Architecture

QuantEngine is an institutional-grade, decoupled, object-oriented automated trading platform engineered for low-latency market analysis and strict pre-trade risk enforcement. Written completely in native Python, this framework utilizes an indicator-less probability-based strategy engine instead of traditional lagging technical signals.

The architecture is built from the ground up to follow a strict **Separation of Concerns (SoC)** pipeline. This modularity ensures the system can seamlessly scale from a local development workspace to cloud-native production environments without altering the underlying core quantitative code.

---

## 🎯 Strategic Deployment Roadmap

The platform follows a deliberate, multi-phase scaling strategy to eliminate configuration risks:
1. **Phase 1 (Current)**: Local prototyping and hot-reload development using **Windows Docker Desktop + PyCharm**.
2. **Phase 2**: Bare-metal environment migration onto an **openSUSE Tumbleweed** workstation.
3. **Phase 3**: Automated continuous deployment to **Oracle Cloud Infrastructure (OCI)** targeting high-efficiency **ARM64 Kubernetes (K8s)** clusters.

---

## 🗂️ Project Directory Layout & File References

Every component of the repository is strictly categorized to prevent tight coupling:

```text
quant_engine/
│
├── config.py              # Global runtime parameters and institutional risk limits
├── main.py                # System bootstrapping layer and dual-destination logging handler
├── requirements.txt       # Hard-pinned data science and operational dependencies
├── Dockerfile             # Multi-stage lightweight Linux container construction blueprint
├── docker-compose.yml     # Orchestration layout for hot-reloading and data persistence
│
├── logs/                  # Persistent data directory mapped out to physical host storage
│   └── execution.log      # Active historical telemetry containing all trade cycles and anomalies
│
├── core/                  # Core infrastructure engine execution loop
│   ├── __init__.py        # Exposes the core execution modules
│   ├── gateway.py         # Hardware network abstractor (REST/WebSocket interface)
│   └── orchestrator.py    # Main system heartbeat routing data to strategy and risk blocks
│
├── alpha/                 # Alpha Generation & Mathematical Probability Packages
│   ├── __init__.py        # Exposes statistical strategy modules
│   ├── base_strategy.py   # Abstract Base Class contract enforcing strict platform type signatures
│   └── prob_velocity.py   # Indicator-less price velocity distribution strategy model
│
└── risk/                  # Failsafe Pre-Trade Gatekeeper Guardrails
    ├── __init__.py        # Exposes structural protection modules
    └── risk_manager.py    # Isolated drawdown validation and dynamic exit calculator
```

---

## 🔍 Core Component Analysis & File Interactions

### 1. Root Configuration & Bootstrapping
* **`config.py`**: Acts as the single source of truth for execution states. Defines symbol pairings (`EURUSD`), tick polling intervals, and sets critical risk mandates such as the `MAX_DAILY_DRAWDOWN_PCT` and maximum execution position constraints.
* **`main.py`**: Initializes the global environment. Configures a robust dual-destination logger that formats and routes runtime strings simultaneously to the visual console and to disk. It acts as the system bootstrap by calling the central orchestrator.
* **`requirements.txt`**: Pins explicit data science and networking binaries (`numpy`, `pandas`, `scipy`, `requests`) to preserve numerical processing reproducibility.

### 2. `core/` Infrastructure Package
* **`core/gateway.py`**: Decouples network boundaries from strategy logic. It handles all raw data ingestion and order serialization. By abstracting data polling, this file can be completely swapped to target broker interfaces (e.g., MT5 API or Alpaca) without touching any code inside the analytical engine.
* **`core/orchestrator.py`**: Connects the components. Every session tick, it calls the `gateway` for a price matrix slice, triggers the `alpha` strategy engine calculation, channels actionable returns to the `risk` manager, and pushes verified results back to the `gateway` execution pipe.

### 3. `alpha/` Statistical Strategy Package
* **`alpha/base_strategy.py`**: Defines the software interface contract. By leveraging Python's `abc` module, any new model (Machine Learning, Order Flow, or alternative Quantitative scripts) simply inherits from this class, making the framework infinitely extensible.
* **`alpha/prob_velocity.py`**: An indicator-less statistical arb core. It converts raw prices into rolling log returns (Price Velocity Distribution). It evaluates the mathematical expectancy of deviations via real-time Z-scores. Trades are only triggered when the Z-score breaches outer standard distribution bands, removing reliance on lagging crossovers.

### 4. `risk/` Capital Preservation Package
* **`risk/risk_manager.py`**: The ultimate gatekeeper. It has no knowledge of how signals are generated; it evaluates account stats independently. It calculates hard-coded stop-loss and take-profit brackets based on strict capital caps before passing order payloads to execution.

---

## 🛠️ Local Installation & Development in PyCharm

### 1. Prerequisites
* Install [Docker Desktop for Windows](https://docker.com).
* Ensure **Expose daemon on tcp://localhost:2375 without TLS** is enabled in Docker Settings.
* Set up [PyCharm Professional or Community Edition](https://jetbrains.com).

### 2. Containerized Orchestration via Docker Compose
To launch the complete engine with full hot-reloading (any changes you make inside PyCharm instantly sync inside the running container) and persistent disk log mapping, right-click on **`docker-compose.yml`** within PyCharm and select **Run**.

Alternatively, execute the service through your system command line:
```bash
docker-compose up --build
```

### 3. Verification of System Telemetry
Once running, check the `logs/execution.log` file generated dynamically on your local directory. It tracks performance and records statistical processing ticks continuously:
```text
2026-07-19 14:30:00,105 [INFO] ==================================================================
2026-07-19 14:30:00,105 [INFO] 🚀 Initializing Quant Engine System Orchestrator Bundle...
2026-07-19 14:30:00,105 [INFO] ==================================================================
2026-07-19 14:30:15,412 [INFO] 🔄 Polling fresh data matrix arrays for EURUSD...
2026-07-19 14:30:15,789 [INFO] 📊 Quantitative Alpha Matrix -> Real-Time Price Velocity Z-Score: 0.4125
2026-07-19 14:30:15,790 [INFO] ⚖️ Market distribution is normal. Holding positions.
```

---

## 🛡️ License
Institutional Proprietary Framework - All Rights Reserved.

