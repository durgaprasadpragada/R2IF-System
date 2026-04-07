from data_loader import load_news_data, load_price_data
from preprocessing import preprocess
from nlp_model import apply_nlp
from severity_model import compute_severity
from risk_index import compute_r2if
from econometrics import run_adf, run_regression, run_granger, run_arima
import pandas as pd


def run_pipeline(news_df, price_df):
    news = preprocess(news_df)
    news = apply_nlp(news)
    news = compute_severity(news)

    r2if = compute_r2if(news)

    # Date alignment
    r2if['date'] = pd.to_datetime(r2if['date'], errors='coerce').dt.date
    price_df['date'] = pd.to_datetime(
        price_df['date'], errors='coerce').dt.date

    price_df = price_df.groupby('date').mean(numeric_only=True).reset_index()

    merged = pd.merge(r2if, price_df, on='date', how='inner')

    print("Merged Data:", merged.head())

    # Econometrics (optional, can be run later)
    # run_adf(merged['severity'])
    # run_regression(merged)
    # run_granger(merged[['severity', 'price']])

    return news, r2if, merged


def run_prediction(merged_df):
    # Run ARIMA on severity
    print("Running ARIMA on severity series of length:",
          len(merged_df['severity']))
    forecast = run_arima(merged_df['severity'])
    print("Prediction completed, forecast length:", len(forecast))
    return forecast


def main():
    news = load_news_data()
    prices = load_price_data()

    news, r2if, merged = run_pipeline(news, prices)

    # Econometrics
    run_adf(merged['severity'])
    run_regression(merged)
    run_granger(merged[['severity', 'price']])

    # Forecast
    forecast = run_prediction(merged)

    # Save outputs
    news.to_csv("classified_news.csv", index=False)
    news[['severity']].to_csv("severity_scores.csv", index=False)
    r2if.to_csv("r2if_timeseries.csv", index=False)

    return news, r2if, merged, forecast


if __name__ == "__main__":
    main()
