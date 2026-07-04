import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Stock Price Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Dashboard")

ticker = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
).upper().strip()

period = st.selectbox(
    "Select Time Period",
    (
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    )
)

interval_map = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1d",
    "5y": "1wk",
    "10y": "1wk",
    "max": "1mo"
}

if st.button("Fetch Data"):

    try:

        with st.spinner("Downloading data..."):

            data = yf.download(
                ticker,
                period=period,
                interval=interval_map[period],
                auto_adjust=True,
                progress=False,
                group_by="column"
            )

        if data.empty:
            st.error("No data available for this ticker.")
            st.stop()

        # Handle MultiIndex columns returned by latest yfinance
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if "Close" not in data.columns:
            st.error("Close price not found.")
            st.stop()

        close = data["Close"]

        # Convert to Series if still DataFrame
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        latest = float(close.iloc[-1])
        first = float(close.iloc[0])

        returns = ((latest - first) / first) * 100

        col1, col2 = st.columns(2)

        col1.metric(
            "Latest Close",
            f"{latest:.2f}"
        )

        col2.metric(
            "Return",
            f"{returns:.2f}%"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=close,
                mode="lines",
                name=ticker
            )
        )

        fig.update_layout(
            title=f"{ticker} Closing Price ({period})",
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Price",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Historical Data")

        st.dataframe(
            data.iloc[::-1],
            use_container_width=True
        )

        csv = data.to_csv(index=True).encode("utf-8")

        st.download_button(
            "Download CSV",
            csv,
            file_name=f"{ticker}_{period}.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
