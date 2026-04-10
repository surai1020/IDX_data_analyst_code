import pandas as pd
from pathlib import Path
listings_raw = []
sellings_raw = []

listings_clean = pd.read_csv('list_clean')
sellings_clean = pd.read_csv('sold_clean')

for f in Path("raw").iterdir():
    if f.name.startswith('CRMLSListing') and f.name.endswith('.csv'):
        listings_raw.append(pd.read_csv(f))
    elif f.name.startswith('CRMLSSold') and f.name.endswith('.csv'):
        sellings_raw.append(pd.read_csv(f))

listings_raw = pd.concat(listings_raw, ignore_index=True)
sellings_raw = pd.concat(sellings_raw, ignore_index=True)


#Summary of Missing Columns
missing_list_cols = set(listings_clean.columns) - set(listings_raw.columns)
missing_sold_cols = set(sellings_clean.columns) - set(sellings_raw.columns)

print("Missing columns in listings (90% Missing):")
listings_raw_null_pct = listings_raw.isna().mean() * 100
for col in listings_raw_null_pct[listings_raw_null_pct > 90].index:
    print(col)


sellings_raw_null_pct = sellings_raw.isna().mean() * 100
print("\nMissing columns in sellings (90% Missing):")
for col in sellings_raw_null_pct[sellings_raw_null_pct > 90].index:
    print(col)

#Unique Property Types
unique_property_types = sellings_clean['PropertyType'].unique()
print("\nUnique Property Types in Sold Data:")
for prop_type in unique_property_types:
    print(prop_type)


#Summary of Sold Data Numeric Distributions
summary = sellings_clean[['ClosePrice', 'LivingArea', 'DaysOnMarket']].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95])
summary.to_csv('numeric_distribution_summary.csv')

print("\n=== NUMERIC DISTRIBUTION SUMMARY ===")
print(summary)