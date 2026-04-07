import pandas as pd


def compute_r2if(df):
    df['date'] = pd.to_datetime(df['date']).dt.date

    r2if = df.groupby('date')['severity'].mean().reset_index()

    print(f"Unique Dates: {r2if['date'].nunique()}")
    print(f"R2IF shape: {r2if.shape}")
    print(r2if.head())

    # Warning instead of exception for small datasets
    if r2if['severity'].nunique() == 1:
        print("WARNING: R2IF has only 1 unique value (single date or constant severity)")
        print("This is normal for single-entry manual input")

    return r2if
