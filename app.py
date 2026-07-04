import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Price Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Price Dashboard")

ticker = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
)

period = st.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    ],
    index=0
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

    with st.spinner("Downloading data..."):

        data = yf.download(
            ticker,
            period=period,
            interval=interval_map[period],
            auto_adjust=True,
            progress=False
        )

    if data.empty:
        st.error("No data found.")
    else:

        st.success("Data Loaded Successfully")

        latest = data["Close"].iloc[-1]
        first = data["Close"].iloc[0]
        returns = ((latest - first) / first) * 100

        c1, c2 = st.columns(2)

        c1.metric(
            "Latest Close",
            f"{latest:.2f}"
        )

        c2.metric(
            "Return",
            f"{returns:.2f}%"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Close Price"
            )
        )

        fig.update_layout(
            title=f"{ticker} Closing Price ({period})",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Historical Data")

        st.dataframe(
            data[::-1],
            use_container_width=True
        )

        csv = data.to_csv().encode()

        st.download_button(
            "Download CSV",
            csv,
            file_name=f"{ticker}_{period}.csv",
            mime="text/csv"
        )
