import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from src.config import DATASET_FILE_PATH, PROCESSED_DATA

STRING_COLUMNS = ["REQUEST_TYPE", "USER_COUNTRY", "PAYMENT_TYPE", "LISTING_TYPE", "SELLER_TYPE", "STOCK_INFO", "BRAND_NAME", "CONDITION_CLASS", "SCOPE_OF_DELIVERY_SUMMARISED"]

def data_preprocessing(df: pd.DataFrame):
    pass


def covert_to_numbers(df: pd.DataFrame):
    mapping = lambda x: {item: idx for idx, item in enumerate(x)}
    for col in df.columns:
        if col in STRING_COLUMNS:
            uniques = df[col].unique()
            df[col] = df[col].map(mapping(uniques))
            print(col + "=",  mapping(uniques))
    print(df.head())
    return df



def prepare_classification_ds(df: pd.DataFrame):
    df = df.drop(["REQUEST_ID", "SALE_VALUE_EUR", "SALE_FEE_EUR", "PAYMENT_TYPE", "SELLER_RECOMMENDED_BY_USER", "LISTING_ID",
                  "SCOPE_OF_DELIVERY_SUMMARISED",  "PRICE_SEGMENT_NAME", "REFERENCE_VARIANT_ID"], axis=1)
    df = df.dropna(axis=0)
    df["SALE_CONFIRMED"] = df["SALE_CONFIRMED"].map({False:0, True:1})
    df = covert_to_numbers(df)
    df.to_excel(PROCESSED_DATA, index=False)
    y = df["SALE_CONFIRMED"]
    X = df.drop(["SALE_CONFIRMED"], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    return X_train, X_test, y_train, y_test



if __name__=="__main__":
    df = pd.read_excel(DATASET_FILE_PATH)
    print(f"Original Dataset Length: {len(df)}")
    x_train, x_test, y_train, y_test = prepare_classification_ds(df)
    print(len(x_train), len(x_test))
    print(len(y_train), len(y_test))
