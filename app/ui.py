import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from main import run_pipeline, run_prediction
from data_loader import load_uploaded_news, load_uploaded_prices

st.set_page_config(
    layout="wide", page_title="CRIS - Cryptocurrency Regulatory Risk Analysis System",
    initial_sidebar_state="expanded")

# Light theme CSS
st.markdown("""
<style>
body {
    background-color: white;
    color: black;
}
.stMetric {
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 5px;
}
.stDataFrame {
    background-color: white;
}
.st-theme-dark .plotly text {
    fill: white !important;
}
.st-theme-light .plotly text {
    fill: black !important;
}
.st-theme-dark .plotly .hoverlayer .hovertext {
    background-color: #333 !important;
    color: white !important;
}
.st-theme-light .plotly .hoverlayer .hovertext {
    background-color: white !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

st.title("CRIS - Cryptocurrency Regulatory Risk Analysis System")

# Initialize session state
if 'news' not in st.session_state:
    st.session_state.news = None
if 'r2if' not in st.session_state:
    st.session_state.r2if = None
if 'merged' not in st.session_state:
    st.session_state.merged = None
if 'forecast' not in st.session_state:
    st.session_state.forecast = None
if 'news_df' not in st.session_state:
    st.session_state.news_df = None
if 'price_df' not in st.session_state:
    st.session_state.price_df = None

# Input Section
st.header("Input Data")

st.info("""
**Upload CSV files with following format:**

📰 **NEWS FILE:**
- Required columns: `content` (text) OR `text` OR `title`
- Optional: `date` column (if missing, current date is used)

💰 **PRICE FILE:**
- Required columns: `date` (or `timestamp`) AND `price` (or `close`)
- Example: date, price columns

**OR** Enter manual input below.
""")

input_method = st.radio("Choose input method:", [
                        "Upload Files", "Manual Input"])

news_df = None
price_df = None

if input_method == "Upload Files":
    col1, col2 = st.columns(2)
    with col1:
        news_file = st.file_uploader("Upload News CSV", type="csv")
    with col2:
        price_file = st.file_uploader("Upload Price CSV", type="csv")

    if news_file and price_file:
        try:
            st.session_state.news_df = load_uploaded_news(news_file)
            st.session_state.price_df = load_uploaded_prices(price_file)
            st.success("Files loaded successfully!")
        except Exception as e:
            st.error(f"Error loading files: {e}")

elif input_method == "Manual Input":
    col1, col2 = st.columns(2)
    with col1:
        news_text = st.text_input("Enter news content:")
        news_date = st.date_input("News date:")
    with col2:
        price_value = st.number_input("Enter price:", min_value=0.0, step=0.01)
        price_date = st.date_input("Price date:")

    if st.button("Add Manual Data"):
        if news_text and price_value:
            st.session_state.news_df = pd.DataFrame({
                'date': [news_date],
                'content': [news_text]
            })
            st.session_state.price_df = pd.DataFrame({
                'date': [price_date],
                'price': [price_value]
            })
            st.success("Manual data added!")
        else:
            st.error("Please fill in all fields.")

# Run Analysis Button
if st.button("Run Analysis", disabled=(st.session_state.news_df is None or st.session_state.price_df is None)):
    with st.spinner("Running analysis..."):
        try:
            news, r2if, merged = run_pipeline(
                st.session_state.news_df, st.session_state.price_df)
            st.session_state.news = news
            st.session_state.r2if = r2if
            st.session_state.merged = merged
            st.success("Analysis completed!")
        except Exception as e:
            st.error(f"Error during analysis: {e}")

# Display results if available
if st.session_state.news is not None:
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total News", len(st.session_state.news))
    with col2:
        st.metric("Average Severity", round(
            st.session_state.news['severity'].mean(), 3))
    with col3:
        st.metric("Maximum Severity", round(
            st.session_state.news['severity'].max(), 3))

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Results", "Risk Analysis", "Prediction"])

    # Add table styling for readability
    st.markdown("""
    <style>
    .dataframe th, .dataframe td {
        font-size: 16px !important;
        padding: 10px !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        max-width: 450px !important;
        overflow-wrap: anywhere !important;
    }
    .dataframe {
        background-color: #ffffff;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

    with tab1:
        st.subheader("Processed News Data")
        st.dataframe(st.session_state.news[['content', 'label', 'confidence', 'severity']].head(
            20), use_container_width=True)

        st.subheader("R2IF Time Series")
        st.dataframe(st.session_state.r2if.head(20), use_container_width=True)

    with tab2:
        st.subheader("R2IF Over Time")
        fig1 = px.line(
            st.session_state.r2if,
            x='date',
            y='severity',
            title="Regulatory Risk Index Trend"
        )
        fig1.update_layout(
            xaxis=dict(title_font=dict(size=14), tickfont=dict()),
            yaxis=dict(title_font=dict(size=14), tickfont=dict()),
            hoverlabel=dict(bgcolor="white", font_size=14,
                            font_family="Arial"),
            hovermode='x unified'
        )
        fig1.update_traces(
            hovertemplate='<b>%{x}</b><br><b>Severity: %{y:.4f}</b><extra></extra>')
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Severity vs Price")
        fig2 = px.scatter(
            st.session_state.merged,
            x='price',
            y='severity',
            hover_data=['date'],
            title="Risk vs Market Price"
        )
        fig2.update_layout(
            xaxis=dict(title_font=dict(size=14), tickfont=dict()),
            yaxis=dict(title_font=dict(size=14), tickfont=dict()),
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial")
        )
        fig2.update_traces(
            hovertemplate='<b>Price: %{x:.2f}</b><br><b>Severity: %{y:.4f}</b><br><b>Date: %{customdata[0]}</b><extra></extra>')
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Severity Forecasting")

        if st.button("Run Prediction"):
            with st.spinner("Running ARIMA prediction..."):
                try:
                    forecast = run_prediction(st.session_state.merged)
                    st.session_state.forecast = forecast
                    st.success("Prediction completed!")
                except Exception as e:
                    st.error(f"Error during prediction: {e}")

        if st.session_state.forecast is not None:
            # Validate forecast data
            if len(st.session_state.forecast) == 0:
                st.warning("No forecast data available")
            else:
                st.subheader("Forecast vs Actual Severity")

                # Convert forecast to list of floats
                try:
                    forecast_values = [float(val)
                                       for val in st.session_state.forecast]
                except Exception as e:
                    st.error(f"Error converting forecast values: {e}")
                    forecast_values = []

                if forecast_values:
                    # Create combined figure
                    fig3 = go.Figure()

                    actual_len = len(st.session_state.merged)

                    # Add actual data
                    fig3.add_trace(go.Scatter(
                        x=list(range(actual_len)),
                        y=st.session_state.merged['severity'].tolist(),
                        mode='lines+markers',
                        name='Actual Severity',
                        line=dict(color='blue', width=2),
                        marker=dict(size=6)
                    ))

                    # Add forecast data
                    forecast_index = list(
                        range(actual_len, actual_len + len(forecast_values)))
                    fig3.add_trace(go.Scatter(
                        x=forecast_index,
                        y=forecast_values,
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='red', width=2, dash='dash'),
                        marker=dict(size=6)
                    ))

                    fig3.update_layout(
                        title="Severity Forecast (ARIMA)",
                        xaxis_title="Time Index",
                        yaxis_title="Severity Score",
                        hovermode='x unified',
                        height=500,
                        xaxis=dict(title_font=dict(size=14), tickfont=dict()),
                        yaxis=dict(title_font=dict(size=14), tickfont=dict()),
                        hoverlabel=dict(bgcolor="white",
                                        font_size=14, font_family="Arial")
                    )
                    fig3.update_traces(
                        hovertemplate='<b>Time: %{x}</b><br><b>Severity: %{y:.4f}</b><extra></extra>')
                    st.plotly_chart(fig3, use_container_width=True)

                    # Display forecast values
                    st.subheader("Forecast Values")
                    forecast_df = pd.DataFrame({
                        'Time Index': forecast_index,
                        'Forecast Value': forecast_values
                    })
                    st.dataframe(forecast_df, use_container_width=True)
        else:
            st.info("Click 'Run Prediction' button above to generate forecast")

else:
    st.info("Please provide input data and run analysis to see results.")
