import pandas as pd

lists = pd.read_csv('listings_with_rates.csv')
sold = pd.read_csv('sold_with_rates.csv')
before_row_count = {'lists' : len(lists),
                   'sold' : len(sold)}


#CONVERTING TO DATETTIME
dt_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
lists[dt_cols] = lists[dt_cols].apply(pd.to_datetime)
sold[dt_cols] = sold[dt_cols].apply(pd.to_datetime)



#INITIAL CLEANING
def flagging(df):
    df['invalid_closeprice_flag'] = df['ClosePrice'] <= 0
    df['invalid_livingarea_flag'] = df['LivingArea'] <= 0
    df['invalid_dom_flag'] = df['DaysOnMarket'] < 0
    df['invalid_bed_flag'] = df['BedroomsTotal'] < 0
    df['invalid_bath_flag'] = df['BathroomsTotalInteger'] < 0
flagging(lists)
flagging(sold)


#CHECKING VALID DATETIME ORDER
def dt_order(df):
    df['listing_after_close_flag'] = (
        (df['ListingContractDate'] > df['CloseDate']) &
        df['CloseDate'].notna()
    )

    df['purchase_after_close_flag'] = (
        (df['PurchaseContractDate'] > df['CloseDate']) &
        df['CloseDate'].notna()
    )

    df['negative_timeline_flag'] = (
        ((df['PurchaseContractDate'] < df['ListingContractDate']) & df['PurchaseContractDate'].notna()) |
        ((df['CloseDate'] < df['PurchaseContractDate']) & df['CloseDate'].notna())
    )   
dt_order(lists)
dt_order(sold)

#CHECKING VALID GEO ORDER
def geo_check(df):
    df['invalid_geo_flag'] = (
        df['Latitude'].isna() | df['Longitude'].isna() |
        (df['Latitude'] == 0) | (df['Longitude'] == 0) |
        (df['Longitude'] > 0) |
        (df['Latitude'] < 32) | (df['Latitude'] > 42) |
        (df['Longitude'] < -125) | (df['Longitude'] > -114)
    )
    return df
geo_check(lists)
geo_check(sold)


###############SUMMARY###############
flag_cols = [
    'invalid_closeprice_flag', 'invalid_livingarea_flag',
    'invalid_dom_flag', 'invalid_bed_flag', 'invalid_bath_flag',
    'listing_after_close_flag', 'purchase_after_close_flag',
    'negative_timeline_flag', 'invalid_geo_flag'
]

def summarize_flags(df, name):
    print(f"\n--- {name.upper()} DATA QUALITY SUMMARY ---")
    for col in flag_cols:
        print(f"{col}: {df[col].sum()} flagged rows")
        
summarize_flags(lists, "lists")
summarize_flags(sold, "sold")

#GEO SUMMARY
def geo_summary(df, name):
    total_invalid = df['invalid_geo_flag'].sum()
    print(f"\n--- {name.upper()} GEO SUMMARY ---")
    print("Invalid coordinate records:", total_invalid)

geo_summary(lists, "lists")
geo_summary(sold, "sold")

#DROPPING INVALIDS + ROW SUMMARY
lists = lists[~lists[flag_cols].any(axis=1)].drop(columns = flag_cols)
sold = sold[~sold[flag_cols].any(axis=1)].drop(columns = flag_cols)
after_row_count = {
    'lists': len(lists),
    'sold': len(sold)
}
print("\n--- ROW COUNT SUMMARY ---")
print("Lists: before =", before_row_count['lists'],
      "| after =", after_row_count['lists'],
      "| removed =", before_row_count['lists'] - after_row_count['lists'])

print("Sold: before =", before_row_count['sold'],
      "| after =", after_row_count['sold'],
      "| removed =", before_row_count['sold'] - after_row_count['sold'])

#SAVING DATASETS
lists.to_csv('listings_with_rates.csv', index=False)
sold.to_csv('sold_with_rates.csv', index=False)
print("\nDatasets saved.")