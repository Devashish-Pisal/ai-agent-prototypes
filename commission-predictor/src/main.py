import pandas as pd
from src.config import DATASET_FILE_PATH
from src.train_and_eval import train_logistic_regression, train_random_forest, train_xgboost, evaluate_model
from src.data_processing import prepare_classification_ds

if __name__ == '__main__':
    df = pd.read_excel(DATASET_FILE_PATH)
    X_train, X_test, y_train, y_test = prepare_classification_ds(df)
    logistic_model = train_logistic_regression(X_train, y_train)
    evaluate_model(logistic_model, X_test, y_test)
    print("="*100)

    random_forest_model = train_random_forest(X_train, y_train)
    evaluate_model(random_forest_model, X_test, y_test)
    print("="*100)

    xgboost_model = train_xgboost(X_train, y_train)
    evaluate_model(xgboost_model, X_test, y_test)
    print("="*100)