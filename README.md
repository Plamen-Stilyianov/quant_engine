# QuantEngine: High-Performance Algorithmic Trading Architecture

QuantEngine is an institutional-grade, decoupled, object-oriented automated trading platform engineered for low-latency market analysis and strict pre-trade risk enforcement. Written completely in native **Python 3.13**, this framework utilizes an indicator-less probability-based strategy engine instead of traditional lagging technical signals.

The architecture is built from the ground up to follow a strict **Separation of Concerns (SoC)** pipeline. This modularity ensures the system can seamlessly scale from a local development workspace to cloud-native production environments without altering the underlying core quantitative code.

---

## ☁️ Live Cloud Production Deployment (Oracle Cloud Infrastructure)

The platform is actively built, verified, and running in production using a fully automated multi-architecture deployment pipeline.

* **Live Platform URL**: http://141.148.65.238/
* **👤 Username ID**: `admin_plamen`
* **🔑 Password Key**: `institutional_quant_2026`

### 🏗️ Live Cloud Infrastructure Architecture
![QuantEngine Live OCI Production Dashboard Interface](docs/oci_trading_engine.png)

---

## 🎛️ Interactive WebGUI Analytics Control Dashboard

The platform features a fully decoupled, interactive execution and simulation dashboard package. This interface allows quantitative operators to actively mutate alpha factors, lookback windows, and standard deviation thresholds to visualize real-time strategy behavior across multiple simulated market structures.

### 📊 Regime 1: Sideways / Normal Distribution (Mean-Reversion Profile)
Tracks the statistical engine navigating range-bound markets, successfully firing alternating long and short execution triggers at distribution extremes.
![QuantEngine Sideways Market Regime UI](docs/nd_dashboard_metrics.png)

### 🚨 Regime 2: Extreme Downward Crash Shock (Volatility Shock Profile)
Tracks the automated gateway intercepting a severe structural price crash, bypassing broker timeouts via the internal failover core to route absolute institutional order blocks.
![QuantEngine Market Crash Volatility UI](docs/crash_dashboard_metrics.png)

---

## 🎯 Strategic Deployment & Hybrid Cloud Roadmap

To minimize execution risks and optimize hardware efficiency, the platform follows a strict, three-phase environmental escalation and deployment pipeline:

### 🪟 Phase 1: Local Windows Sandboxed Prototyping (Completed)
* **Environment**: Windows 11 Desktop + Docker Desktop for Windows + PyCharm.
* **Objective**: Rapid algorithm prototyping, UI visualization tuning, and configuration locking via local `.env` parameter injections. Containers leverage local shared volumes for immediate data persistence on the Windows host system.

### 🦎 Phase 2: openSUSE Tumbleweed Bare-Metal Workstation Migration (Active Testing)
* **Environment**: Native rolling-release openSUSE Tumbleweed workstation running a low-latency Linux kernel.
* **Objective**: Eliminate hypervisor translation overhead by executing directly on the bare-metal Linux POSIX runtime to minimize thread latency.
* **Toolchain Integration**: Utilizing native container engines (`podman`/`docker`) along with **Docker Buildx** pipelines to securely cross-compile and verify x86_64 and arm64 system layers locally before pushing to cloud registries.

### ☁️ Phase 3: Cloud Orchestration via Kubernetes (K8s) on Oracle Cloud Infrastructure (OCI)
* **Environment**: OCI Container Engine for Kubernetes (OKE) running on high-efficiency, dedicated AMD64 Compute Shapes.
* **Objective**: High-availability, production-grade automated scaling utilizing sidecar pod containers.
* **Architecture Mapping**:
  * **Stateless Pod Isolation**: The `quant_bot` core engine and the `webgui_dashboard` application are split into completely independent container runtimes sharing an absolute `/app/logs` volume, maximizing computing lanes.
  * **Wine Integration Gateway**: The `mt5-bridge` component runs inside an isolated, pinned x86_64 node workspace to allow seamless Linux-to-Windows API translation for MetaTrader 5 routing.
  * **Flexible Load Balancer Ingress**: Fronted by an automated OCI Load Balancer shaping web requests dynamically to keep interface delivery snappy and concurrent.

---

## 🗂️ Project Directory Layout & File References

Every component of the repository is strictly categorized to prevent tight coupling and preserve repository security:

```text
quant_engine/
│
├── docs/                 # Media directory hosting repository presentation graphics
│   ├── nd_dashboard_metrics.png        # Select Simulation Regime - Sideways / Normal Distribution
│   ├── crash_dashboard_metrics.png     # Select Simulation Regime - Extreme Downward Crash Shock
│   └── oci_trading_engine.png          # Active Live Production Dashboards Telemetry layout
│
├── .env                   # Secure local environment variables (API tokens, private parameters)
├── .gitignore             # Strict exclusion map preventing secret leaks and cache clutter to GitHub
├── config.py              # Single source of truth for runtime values and global risk limits
├── main.py                # System bootstrapping layer and dual-destination logging handler
├── Dockerfile.linux       # Production multi-stage AMD64/ARM64 Buildx container construction blueprint
├── docker-compose-linux.yml # Orchestration layout for hot-reloading and openSUSE data persistence
│
├── logs/                  # Persistent data directory mapped out to physical host storage
│   ├── execution.log      # Active historical telemetry containing all trade cycles and anomalies
│   └── trades.csv         # Structured transaction ledger output mapping signal timestamps
│
├── core/                  # Core infrastructure engine execution loop
│   ├── __init__.py        # Exposes the core execution modules
│   ├── gateway.py         # OANDA REST v20 connector with integrated automated data failover engine
│   └── orchestrator.py    # Main system heartbeat routing data to strategy and risk blocks
│
├── alpha/                 # Alpha Generation & Mathematical Probability Packages
│   ├── __init__.py        # Exposes statistical strategy modules
│   ├── base_strategy.py   # Abstract Base Class contract enforcing strict platform type signatures
│   └── prob_velocity.py   # Indicator-less price velocity log distribution strategy model
│
├── risk/                  # Failsafe Pre-Trade Gatekeeper Guardrails
│   ├── __init__.py        # Exposes structural protection modules
│   └── risk_manager.py    # Isolated drawdown validation and MT5-compliant payload constructor
│
└── webgui_dashboard/      # Visual Interface Python Package
    ├── __init__.py        # Package exposure mapping script
    ├── charts.py          # Plotly analytics charting module
    └── main_ui.py         # Core web layout engine and factor controller
```

---

## 🔍 Core Component Analysis & File Interactions

### 1. Root Configuration & Security Guardrails
* **`.env`**: Locks down private keys locally (such as your `OANDA_ACCESS_TOKEN` and account IDs). These are injected dynamically into the container runtime memory at boot.
* **`.gitignore`**: Explicitly untracks `.env`, local `logs/`, `__pycache__/`, and local environment configurations to maintain compliance with clean Git repository rules.
* **`config.py`**: Intercepts environment injections. Defines symbol targets (`EUR_USD`), system polling loops, and establishes capital preservation parameters.

### 2. `core/` Infrastructure Package
* **`core/gateway.py`**: Connects your container to external endpoints. It contains an advanced **Automated Failover Mitigation Engine**. If the broker server goes offline or returns an execution block (e.g., weekend HTTP 403 closures), the gateway intercepts the drop, prevents a system crash, and injects realistic statistical pricing vectors to keep the alpha matrix alive.
* **`core/orchestrator.py`**: Manages data flow. Every tick, it requests a price slice from the gateway, triggers the alpha math loop, checks triggers against risk rules, and routes finalized orders back to execution.

### 3. `alpha/` Statistical Strategy Package
* **`alpha/base_strategy.py`**: Outlines the platform's programming interface contract using Python's `abc` module. Any new quantitative concept simply inherits from this block, ensuring the engine remains infinitely extensible.
* **`alpha/prob_velocity.py`**: The quantitative core. It converts price bars into rolling log returns (Price Velocity Distribution). It calculates real-time Z-scores using standard deviations. If current returns velocity breaches statistical thresholds, it generates entry metrics.
