import pandas as pd

lists = pd.read_csv('listings_with_rates.csv')
sold = pd.read_csv('sold_with_rates.csv')

def iqr_tuning(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower) & (df[col] <= upper)]

iqr_tuning(lists, 'ClosePrice')
iqr_tuning(lists, 'LivingArea')
iqr_tuning(lists, 'DaysOnMarket')

iqr_tuning(sold, 'ClosePrice')
iqr_tuning(sold, 'LivingArea')
iqr_tuning(sold, 'DaysOnMarket')

lists.to_csv('listings_with_rates.csv', index=False)
sold.to_csv('sold_with_rates.csv', index=False)
print("\nDatasets saved.")