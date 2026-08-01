import json
import pandas as pd
from pprint import pprint
from src.config import DATASET_FILE_PATH, DATASET_INFO_FILE_PATH

dataset_df = pd.read_excel(DATASET_FILE_PATH)
colums_with_types = dataset_df.dtypes.to_dict()

print("Number of rows: ", len(dataset_df))
print("Number of colums:", len(colums_with_types))
print("Colums and their types:")
pprint(colums_with_types)
print("Dataset info:", dataset_df.info)

"""
Number of rows:  37672
Number of colums: 21

Colums and their types:
{'BRAND_NAME': <StringDtype(storage='python', na_value=nan)>,
 'CONDITION_CLASS': <StringDtype(storage='python', na_value=nan)>,
 'HANDLING_TIME_IN_DAYS': dtype('int64'),
 'LISTING_ID': dtype('int64'),
 'LISTING_PRICE_EUR': dtype('float64'),
 'LISTING_TYPE': <StringDtype(storage='python', na_value=nan)>,
 'MARKET_PRICE_DATA_STRENGTH_SCORE': dtype('float64'),
 'MARKET_PRICE_EUR_ESTIMATE': dtype('float64'),
 'PAYMENT_TYPE': <StringDtype(storage='python', na_value=nan)>,
 'PRICE_SEGMENT_NAME': <StringDtype(storage='python', na_value=nan)>,
 'REFERENCE_VARIANT_ID': dtype('float64'),
 'REQUEST_ID': dtype('int64'),
 'REQUEST_TYPE': <StringDtype(storage='python', na_value=nan)>,
 'SALE_CONFIRMED': dtype('bool'),
 'SALE_FEE_EUR': dtype('float64'),
 'SALE_VALUE_EUR': dtype('float64'),
 'SCOPE_OF_DELIVERY_SUMMARISED': <StringDtype(storage='python', na_value=nan)>,
 'SELLER_RECOMMENDED_BY_USER': <StringDtype(storage='python', na_value=nan)>,
 'SELLER_TYPE': <StringDtype(storage='python', na_value=nan)>,
 'STOCK_INFO': <StringDtype(storage='python', na_value=nan)>,
 'USER_COUNTRY': <StringDtype(storage='python', na_value=nan)>}

Dataset info: <bound method DataFrame.info of        REQUEST_ID  ... MARKET_PRICE_DATA_STRENGTH_SCORE
0               1  ...                             51.0
1               2  ...                              NaN
2               3  ...                              NaN
3               4  ...                             38.0
4               5  ...                             97.0
...           ...  ...                              ...
37667       63763  ...                              NaN
37668       63764  ...                             77.0
37669       63765  ...                             64.0
37670       63767  ...                            100.0
37671       63768  ...                              NaN

[37672 rows x 21 columns]>
"""