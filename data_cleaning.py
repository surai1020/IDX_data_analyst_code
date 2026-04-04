import pandas as pd
listing_1 = pd.read_csv('raw/CRMLSListing202402.csv')
sold_1 = pd.read_csv('raw/CRMLSSold202402.csv')
listing_2 = pd.read_csv('raw/CRMLSListing202602.csv')
sold_2 = pd.read_csv('raw/CRMLSSold202602.csv')

pd.set_option('display.max_columns', None)
listings = [listing_1, listing_2]
sellings = [sold_1, sold_2]

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
    df['PriceRatio'] = df['ClosePrice']/df['OriginalListPrice']
    df['PricePerSqFt'] = df['ClosePrice']/df['LivingArea']
    df['YearMonth'] = df['CloseDate'].dt.to_period('M')
    return df

listings = pd.concat([added_cols(correct_types(remove_duplicates(df.dropna(axis=1, how = 'all')))) for df in listings])
sellings = pd.concat([added_cols(correct_types(remove_duplicates(df.dropna(axis=1, how = 'all')))) for df in sellings])

listings.to_csv('list_clean')
sellings.to_csv('sold_clean')


