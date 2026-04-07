from transformers import pipeline

# ✅ Stable FinBERT model (works without tokenizer issues)
finbert = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)


def apply_nlp(df):
    # Drop empty rows
    df = df[df['content'].str.strip() != ""]

    # Ensure content is string
    df['content'] = df['content'].astype(str)

    # Apply model to each row independently
    results = []
    for text in df['content']:
        output = finbert(text[:512])[0]  # Truncate to 512 chars
        results.append(output)

    df['label'] = [r['label'] for r in results]
    df['confidence'] = [r['score'] for r in results]

    print("First 5 NLP outputs:")
    print(df[['content', 'label', 'confidence']].head())

    # Validation (warning only)
    if df['label'].nunique() <= 1:
        print("WARNING: Model outputs are constant")
        print(df['content'].head())

    return df
