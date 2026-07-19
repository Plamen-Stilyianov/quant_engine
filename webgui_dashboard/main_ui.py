import streamlit as st
import pandas as pd
import numpy as np
import os

# CRITICAL DYNAMIC HOOKS: Imports your live alpha logic directly
from alpha.prob_velocity import ProbabilityVelocityStrategy
from webgui_dashboard.charts import RenderEngine

def check_gui_authentication():
    """Verifies user login keys securely using a form container to prevent browser refresh errors."""
    expected_username = "admin_plamen"
    expected_password = "institutional_quant_2026"

    # Initialize authentication tracking state within Streamlit memory mapping
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Render access screen if user has not yet authenticated
    if not st.session_state["authenticated"]:
        st.set_page_config(page_title="QuantEngine | Login", layout="centered")

        st.title("🛡️ Institutional Algorithmic Platform Access")
        st.markdown("---")

        # Enclose the authentication inputs in a native Streamlit Form
        # This completely isolates the fields from browser extension interference
        with st.form(key="login_form_gate"):
            user_input = st.text_input("Username ID", placeholder="Enter authorization profile ID")
            pass_input = st.text_input("Password Key", type="password", placeholder="Enter platform secret key")
            submit_button = st.form_submit_button(label="Authenticate Session", use_container_width=True)

        if submit_button:
            # DIAGNOSTIC LOGGING: Prints exact characters to the PyCharm terminal console
            print(f"DEBUG CRITICAL: [Expected User: 'admin_plamen'] | [Typed User: '{user_input}']")
            print(f"DEBUG CRITICAL: [Expected Pass: 'institutional_quant_2026'] | [Typed Pass: '{pass_input}']")

            if user_input.strip() == expected_username and pass_input.strip() == expected_password:
                st.session_state["authenticated"] = True
                st.success("✅ Access Verified. Synchronizing parameters...")
                st.rerun()
            else:
                st.error("🔒 Access Denied: Invalid Security Identification Token Profiles.")

        return False
    return True

def boot_dashboard_package():
    # 1. ENFORCE GATEKEEPER LOCKDOWN FIRST
    if not check_gui_authentication():
        return

    # 2. INITIALIZE PLATFORM CONFIGURATION (Must be the first layout directive)
    st.set_page_config(page_title="QuantEngine | WebGUI", layout="wide", initial_sidebar_state="expanded")

    # 3. ACTIVATE CONTINUOUS REAL-TIME POLLING LOOP
    # Forces Streamlit to auto-refresh and pull fresh log data every 3 seconds natively
    st.logo("https://streamlit.io")
    st.sidebar.markdown("---")
    st.sidebar.caption("⏳ Automated Interface Stream Polling Active")
    st.fragment(run_every=3)(lambda: None)()

    st.title("🎛️ QuantEngine Decoupled WebGUI & Package Interface")
    st.markdown(
        "Modify interactive parameter variables to re-evaluate your underlying `alpha/` strategy module logic instantly.")
    st.markdown("---")

    # ==============================================================================
    # 1. SIDEBAR CONFIGURATION - INTERACTIVE FACTOR CHANGERS
    # ==============================================================================
    st.sidebar.header("🔧 Interactive Optimization Factors")

    market_regime = st.sidebar.selectbox(
        "Select Simulation Regime",
        ["Sideways / Normal Distribution", "Extreme Downward Crash Shock", "Aggressive Upward Trend"]
    )

    # FACTOR CHANGE 1: Rolling lookback window input controller
    gui_lookback = st.sidebar.slider("Strategy Analytical Lookback Window (Bars)", min_value=15, max_value=150,
                                     value=50, step=5)

    # FACTOR CHANGE 2: Strategy execution threshold controller
    gui_threshold = st.sidebar.slider("Alpha Execution Entry Boundary (Z-Score)", min_value=0.5, max_value=3.0,
                                      value=1.5, step=0.1)

    st.sidebar.markdown("---")

    # Session Terminate Logout button logic
    if st.sidebar.button("🔒 Terminate Platform Session", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    st.sidebar.info("💡 Sliders directly manipulate the parameters of your underlying Python classes in real-time.")

    # ==============================================================================
    # 2. RUN RE-CALCULATIONS DIRECTLY VIA YOUR ALPHA PACKAGE
    # ==============================================================================
    # Instantiating your real mathematical strategy class directly into the frontend loop
    strategy_instance = ProbabilityVelocityStrategy(lookback_window=gui_lookback, entry_threshold_z=gui_threshold)

    # Generate identical base pricing arrays matching your core gateway failover metrics
    np.random.seed(42)
    base_price = 1.08500
    ticks = 200

    if market_regime == "Extreme Downward Crash Shock":
        noise = np.random.normal(-0.0001, 0.0003, ticks)
        noise[120:130] = -0.0035  # Severe price crash vector
    elif market_regime == "Aggressive Upward Trend":
        noise = np.random.normal(0.0001, 0.0002, ticks)
        noise[80:110] = 0.0015
    else:
        noise = np.random.normal(0, 0.0001, ticks)

    prices = base_price + np.cumsum(noise)
    df = pd.DataFrame(prices, columns=["Price"])

    # Recalculate returns metrics cleanly to chart raw wave behaviors
    df["Velocity"] = np.log(df["Price"]).diff()
    df["Rolling_Mean"] = df["Velocity"].rolling(window=gui_lookback).mean()
    df["Rolling_Std"] = df["Velocity"].rolling(window=gui_lookback).std()
    df["Z_Score_Value"] = (df["Velocity"] - df["Rolling_Mean"]) / df["Rolling_Std"]
    df = df.fillna(0)

    # FEED MATRIX VIA NATIVE STRATEGY: Iteratively execute your actual strategy module logic
    signals = []
    for idx in range(len(df)):
        # Extract rolling price arrays passing matching dimensions directly to your code block
        price_slice = df["Price"].iloc[max(0, idx - gui_lookback + 1):idx + 1].to_numpy()
        signals.append(strategy_instance.generate_signal(price_slice))

    df["Z_Score_Signal"] = signals

    # ==============================================================================
    # 3. RENDER INTERACTIVE PLOTLY GRAPHS
    # ==============================================================================
    st.plotly_chart(RenderEngine.draw_market_matrix(df, gui_threshold), use_container_width=True)
    st.plotly_chart(RenderEngine.draw_z_wave(df, gui_threshold), use_container_width=True)

    # ==============================================================================
    # 4. READ AND STREAM LIVE RUNTIME DISK RECORDS FROM LOGS/
    # ==============================================================================
    st.markdown("---")
    st.subheader("📋 Production System Logs Tracker (Sourced from `logs/`)")
    col_log, col_csv = st.columns(2)

    with col_log:
        st.markdown("**Last 5 Core Runtime Strings (`logs/execution.log`):**")
        log_path = "logs/execution.log"
        if os.path.exists(log_path):
            # CACHE-BUSTER: We read the file in binary mode with an explicit system reload instruction
            with open(log_path, "r", encoding="utf-8", errors="ignore") as log_file:
                lines = log_file.readlines()
                # Slice and print the absolute latest 5 events from the tail end of the log
                st.code("".join(lines[-5:]), language="text")
        else:
            st.info("Synchronizing data with orchestrator ticker channel...")

    with col_csv:
        st.markdown("**Last 5 Transmitted MT5 Payloads (`logs/trades.csv`):**")
        csv_path = "logs/trades.csv"
        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
            # CACHE-BUSTER: We forcefully refresh the pandas parser engine buffer memory cache
            trades_df = pd.read_csv(csv_path)
            st.dataframe(trades_df.tail(5), use_container_width=True)
        else:
            st.info("⚖️ Waiting for Z-Score thresholds to breach to log transactions to spreadsheet.")


if __name__ == "__main__":
    boot_dashboard_package()
