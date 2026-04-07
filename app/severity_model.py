def compute_severity(df):

    country_keywords = ['us', 'china', 'india', 'eu', 'uk', 'russia']
    policy_keywords = ['ban', 'restrict', 'regulation',
                       'law', 'illegal', 'tax', 'compliance']
    coverage_keywords = ['global', 'market',
                         'worldwide', 'economy', 'crypto', 'exchange']

    def score(text, keywords):
        words = text.split()
        count = sum(1 for w in words if w in keywords)
        return count / (len(words) + 1)

    df['W'] = df['content'].apply(lambda x: score(x, country_keywords))
    df['P'] = df['content'].apply(lambda x: score(x, policy_keywords))
    df['C'] = df['content'].apply(lambda x: score(x, coverage_keywords))
    df['L'] = df['confidence']

    # Add length factor for variation
    df['length_factor'] = df['content'].apply(lambda x: len(x.split()) / 50)

    df['severity'] = (df['W'] + df['P'] + df['C'] +
                      df['L'] + df['length_factor']) / 5

    print("First 10 severity values:")
    print(df[['W', 'P', 'C', 'L', 'length_factor', 'severity']].head(10))

    if df['severity'].nunique() < 5:
        print("WARNING: Severity not varying enough")
        print(df['severity'].value_counts())

    return df
