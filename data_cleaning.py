import pandas as pd
from pathlib import Path

listings = []
sellings = []
for f in Path("raw").iterdir():
    if f.name.startswith('CRMLSListing') and f.name.endswith('.csv'):
        listings.append(pd.read_csv(f))
    elif f.name.startswith('CRMLSSold') and f.name.endswith('.csv'):
        sellings.append(pd.read_csv(f))

def remove_duplicates(df):
    drop = []
    for col in df.columns:
        if col.endswith('.1'):
            drop.append(col)
    return df.drop(columns = drop)
def correct_types(df):
    date_cols = df.columns[df.columns.str.contains('Date')]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    return df
def added_cols(df):
    if 'ClosePrice' in df.columns and 'OriginalListPrice' in df.columns:
        df['PriceRatio'] = df['ClosePrice'] / df['OriginalListPrice'].replace(0, pd.NA)

    if 'ClosePrice' in df.columns and 'LivingArea' in df.columns:
        df['PricePerSqFt'] = df['ClosePrice'] / df['LivingArea'].replace(0, pd.NA)

    # YearMonth
    if 'CloseDate' in df.columns:
        df['YearMonth'] = df['CloseDate'].dt.to_period('M')

    return df


listings = pd.concat([
    added_cols(
        correct_types(
            remove_duplicates(
                df.dropna(axis=1, thresh=len(df) * 0.1)
            )
        )
    )
    for df in listings
], ignore_index=True)

sellings = pd.concat([
    added_cols(
        correct_types(
            remove_duplicates(
                df.dropna(axis=1, thresh=len(df) * 0.1)
            )
        )
    )
    for df in sellings
], ignore_index=True)

listings.to_csv('list_clean.csv', index=False)
sellings.to_csv('sold_clean.csv', index=False)


