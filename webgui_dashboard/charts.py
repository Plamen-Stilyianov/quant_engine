import plotly.graph_objects as go
import pandas as pd


class RenderEngine:
    """Renders highly interactive dark-mode components without touching background calculation threads."""

    @staticmethod
    def draw_market_matrix(df: pd.DataFrame, threshold: float) -> go.Figure:
        fig = go.Figure()
        # Add basic asset tracking line
        fig.add_trace(
            go.Scatter(x=df.index, y=df["Price"], name="Asset Price (EUR_USD)", line=dict(color="#1f77b4", width=2)))

        # Filter rows where the interactive Z-Score calculation breaches parameters
        shorts = df[df["Z_Score_Signal"] == -1]
        buys = df[df["Z_Score_Signal"] == 1]

        # Add signal marker shapes
        fig.add_trace(go.Scatter(x=shorts.index, y=shorts["Price"], mode="markers", name="SHORT Signal Triggered",
                                 marker=dict(color="#d62728", size=10, symbol="triangle-down")))
        fig.add_trace(go.Scatter(x=buys.index, y=buys["Price"], mode="markers", name="LONG Signal Triggered",
                                 marker=dict(color="#2ca02c", size=10, symbol="triangle-up")))

        fig.update_layout(title="Asset Evaluation Matrix & Execution Triggers", template="plotly_dark", height=380,
                          margin=dict(l=20, r=20, t=40, b=20))
        return fig

    @staticmethod
    def draw_z_wave(df: pd.DataFrame, threshold: float) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Z_Score_Value"], name="Rolling Z-Score Wave",
                                 line=dict(color="#ff7f0e", width=1.5)))

        # Dynamic horizontal threshold boundary markers matching user sliders
        fig.add_hline(y=threshold, line_dash="dash", line_color="#d62728",
                      annotation_text=f"Short Boundary (+{threshold})")
        fig.add_hline(y=-threshold, line_dash="dash", line_color="#2ca02c",
                      annotation_text=f"Long Boundary (-{threshold})")

        fig.update_layout(title="Live Velocity Standard Deviation Waveform (Z-Score Matrix)", template="plotly_dark",
                          height=280, margin=dict(l=20, r=20, t=40, b=20))
        return fig
