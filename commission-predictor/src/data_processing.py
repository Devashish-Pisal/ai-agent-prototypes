import pandas as pd
from sklearn.model_selection import train_test_split
from src.config import DATASET_FILE_PATH, PROCESSED_DATA


# categorical columns we keep as features -> one-hot encoded later
CATEGORICAL_COLUMNS = ["REQUEST_TYPE", "USER_COUNTRY", "LISTING_TYPE", "SELLER_TYPE",
                        "STOCK_INFO", "BRAND_NAME", "CONDITION_CLASS"]

# numeric columns that have missing values
NUMERIC_COLUMNS_WITH_NA = ["LISTING_PRICE_EUR", "MARKET_PRICE_EUR_ESTIMATE", "MARKET_PRICE_DATA_STRENGTH_SCORE"]



def prepare_data(df: pd.DataFrame):
    df = clean_data(df)
    df.to_excel(PROCESSED_DATA, index=False)

    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["SALE_CONFIRMED"]
    )

    feature_columns = [c for c in df.columns if c not in ("SALE_CONFIRMED", "SALE_FEE_EUR")]
    # classification data
    X_train = train_df[feature_columns]
    y_train = train_df["SALE_CONFIRMED"]
    X_test = test_df[feature_columns]
    y_test = test_df["SALE_CONFIRMED"]
    # regression data
    train_sold = train_df[train_df["SALE_CONFIRMED"] == 1]
    test_sold = test_df[test_df["SALE_CONFIRMED"] == 1]
    X_train_fee = train_sold[feature_columns]
    y_train_fee = train_sold["SALE_FEE_EUR"]
    X_test_fee = test_sold[feature_columns]
    y_test_fee = test_sold["SALE_FEE_EUR"]

    y_test_actual_commission = test_df["SALE_FEE_EUR"]

    return (X_train, X_test, y_train, y_test,
            X_train_fee, X_test_fee, y_train_fee, y_test_fee,
            y_test_actual_commission)


def clean_data(df: pd.DataFrame):
    # Remove useless columns
    df = df.drop(["REQUEST_ID", "SALE_VALUE_EUR", "PAYMENT_TYPE", "SELLER_RECOMMENDED_BY_USER", "LISTING_ID",
                  "SCOPE_OF_DELIVERY_SUMMARISED", "PRICE_SEGMENT_NAME", "REFERENCE_VARIANT_ID"], axis=1)
    df = fill_missing_values(df)
    df = group_rare_brands(df)
    df["SALE_CONFIRMED"] = df["SALE_CONFIRMED"].map({False: 0, True: 1})
    df["SALE_FEE_EUR"] = df["SALE_FEE_EUR"].where(df["SALE_CONFIRMED"] == 1, 0)
    df = encode_categorical(df)
    return df



def fill_missing_values(df: pd.DataFrame):
    for col in NUMERIC_COLUMNS_WITH_NA:
        df[col] = df[col].fillna(df[col].median())
    df["BRAND_NAME"] = df["BRAND_NAME"].fillna("Unknown")
    return df


def group_rare_brands(df: pd.DataFrame, top_n=15):
    # BRAND_NAME has ~356 unique values, one-hot encoding all of them would create too many columns,
    top_brands = df["BRAND_NAME"].value_counts().head(top_n).index
    df["BRAND_NAME"] = df["BRAND_NAME"].where(df["BRAND_NAME"].isin(top_brands), "Other")
    return df



def encode_categorical(df: pd.DataFrame):
    df = pd.get_dummies(df, columns=CATEGORICAL_COLUMNS)
    return df



if __name__=="__main__":
    df = pd.read_excel(DATASET_FILE_PATH)
    print(f"Original Dataset Length: {len(df)}")
    X_train, X_test, y_train, y_test, X_train_fee, X_test_fee, y_train_fee, y_test_fee, y_test_actual_commission = prepare_data(df)
    print(len(X_train), len(X_test))
    print("rows used for the fee regression (converted only):", len(X_train_fee), len(X_test_fee))
