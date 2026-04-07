import pandas as pd
import os


def load_news_data():
    paths = [
        "E:/datasets/cryptonews.csv",
        "E:/datasets/financial_news.csv",
        "E:/datasets/crypto_news/crypto_news_api.csv"
    ]

    dfs = []

    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            # 🔥 Convert all column names to lowercase
            df.columns = [col.lower() for col in df.columns]
            print(f"\nLoaded: {path}")
            print("Columns:", df.columns.tolist())

            # 🔥 Detect text column dynamically
            possible_cols = ['content', 'text', 'title',
                             'headline', 'body', 'article', 'description']

            found = None
            for col in possible_cols:
                if col in df.columns:
                    found = col
                    break

            if found is None:
                raise Exception(f"ERROR: No text column found in {path}")

            # Rename to 'content'
            df = df.rename(columns={found: 'content'})

            # Ensure date exists
            if 'date' not in df.columns:
                if 'published_at' in df.columns:
                    df = df.rename(columns={'published_at': 'date'})
                else:
                    raise Exception(f"ERROR: No date column in {path}")

            dfs.append(df[['date', 'content']])

    combined = pd.concat(dfs, ignore_index=True)

    print(f"\nTotal News Rows Loaded: {len(combined)}")
    return combined


def load_price_data():
    import pandas as pd
    import os

    folder = "E:/datasets/prices/"
    dfs = []

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            path = os.path.join(folder, file)

            df = pd.read_csv(path)

            # 🔥 Normalize column names
            df.columns = [col.lower() for col in df.columns]

            print(f"\nLoaded Price File: {file}")
            print("Columns:", df.columns.tolist())

            # 🔍 Detect date column
            date_cols = ['date', 'timestamp', 'time']
            date_col = None

            for col in date_cols:
                if col in df.columns:
                    date_col = col
                    break

            if date_col is None:
                raise Exception(f"ERROR: No date column in {file}")

            # 🔍 Detect price column
            price_cols = ['price', 'close', 'value', 'adj close']
            price_col = None

            for col in price_cols:
                if col in df.columns:
                    price_col = col
                    break

            if price_col is None:
                raise Exception(f"ERROR: No price column in {file}")

            # Rename columns
            df = df.rename(columns={
                date_col: 'date',
                price_col: 'price'
            })

            dfs.append(df[['date', 'price']])

    prices = pd.concat(dfs, ignore_index=True)

    print(f"\nTotal Price Rows Loaded: {len(prices)}")
    return prices


# New functions for uploaded files
def load_uploaded_news(file):
    df = pd.read_csv(file)
    df.columns = [col.lower() for col in df.columns]

    # Detect content column
    possible_cols = ['content', 'text', 'title',
                     'headline', 'body', 'article', 'description']
    content_col = None
    for col in possible_cols:
        if col in df.columns:
            content_col = col
            break
    if content_col is None:
        raise ValueError(
            "No suitable content column found. Expected: content, text, title, etc.")

    df = df.rename(columns={content_col: 'content'})

    # Detect date column
    date_cols = ['date', 'timestamp', 'time', 'published_at']
    date_col = None
    for col in date_cols:
        if col in df.columns:
            date_col = col
            break
    if date_col is None:
        # If no date, create a default date
        df['date'] = pd.Timestamp.today().date()
    else:
        df = df.rename(columns={date_col: 'date'})

    return df[['date', 'content']]


def load_uploaded_prices(file):
    df = pd.read_csv(file)
    df.columns = [col.lower() for col in df.columns]

    # Detect date column
    date_cols = ['date', 'timestamp', 'time']
    date_col = None
    for col in date_cols:
        if col in df.columns:
            date_col = col
            break
    if date_col is None:
        raise ValueError(
            "No suitable date column found. Expected: date, timestamp, time")

    # Detect price column
    price_cols = ['price', 'close', 'value', 'adj close']
    price_col = None
    for col in price_cols:
        if col in df.columns:
            price_col = col
            break
    if price_col is None:
        raise ValueError(
            "No suitable price column found. Expected: price, close, value, etc.")

    df = df.rename(columns={date_col: 'date', price_col: 'price'})

    return df[['date', 'price']]
