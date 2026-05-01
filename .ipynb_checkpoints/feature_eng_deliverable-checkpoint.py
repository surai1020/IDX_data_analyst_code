import pandas as pd

lists = pd.read_csv('listings_with_rates.csv')
sold = pd.read_csv('sold_with_rates.csv')

#ADDING CloseToOriginalList
sold['CloseToOriginalListRatio'] = sold['ClosePrice']/sold['OriginalListPrice']
lists['CloseToOriginalListRatio'] = lists['ClosePrice']/lists['OriginalListPrice']

#ADDING ListingToContractDays
sold['ListingToContractDays'] = sold['PurchaseContractDate'] - sold['ListingContractDate']
lists['ListingToContractDays'] = lists['PurchaseContractDate'] - lists['ListingContractDate']

#ADDING ContractToCloseDays
sold['ContractToCloseDays'] = sold['CloseDate'] - sold['PurchaseContractDate']
lists['ContractToCloseDays'] = lists['CloseDate'] - lists['PurchaseContractDate']

#SUMMARY 
def segment_summary(df, group_cols):
    return (
        df.groupby(group_cols)
        .agg(
            count=('ClosePrice', 'size'),
            median_price=('ClosePrice', 'median'),
            avg_price=('ClosePrice', 'mean'),
            median_ppsqft=('PricePerSqFt', 'median'),
            avg_ppsqft=('PricePerSqFt', 'mean'),
            avg_dom=('DaysOnMarket', 'mean'),
            avg_price_ratio=('PriceRatio', 'mean'),
            avg_list_to_contract=('ListingToContractDays', 'mean'),
            avg_contract_to_close=('ContractToCloseDays', 'mean')
        )
        .sort_values('count', ascending=False)
    )
prop_summ = segment_summary(sold, ['PropertyType', 'PropertySubType'])
loc_summ = segment_summary(sold, ['CountyOrParish', 'MLSAreaMajor'])
list_off_summ = segment_summary(sold, ['ListOfficeName'])
buy_off_summ = segment_summary(sold, ['BuyerOfficeName'])


prop_summ.to_csv('property_type_comparison.csv')
loc_summ.to_csv('location_comparison.csv')

#UPDATE CURR CSVs
lists.to_csv('listings_with_rates.csv', index=False)
sold.to_csv('sold_with_rates.csv', index=False)
print("\nDatasets saved.")