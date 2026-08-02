from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from xgboost import XGBClassifier
import pandas as pd


# CLASSIFICATION

def train_logistic_regression(X_train, y_train):
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=10000, random_state=42)
    )
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost(X_train, y_train):
    model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    print(f"Accuracy         : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Balanced Accuracy: {balanced_accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision        : {precision_score(y_test, y_pred):.4f}")
    print(f"Recall           : {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score         : {f1_score(y_test, y_pred):.4f}")
    print(f"ROC AUC          : {roc_auc_score(y_test, y_prob):.4f}")


def feature_importance(model, feature_names, top_n=10):
    # on which features the model relies the most
    importance = (
        pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        })
        .sort_values("Importance", ascending=False)
        .head(top_n)
    )
    print(importance)






# REGRESSION

def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_random_forest_regressor(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def evaluate_regression_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    print(f"MAE : {mean_absolute_error(y_test, y_pred):.2f} EUR")
    print(f"RMSE: {rmse:.2f} EUR")
    print(f"R2  : {r2_score(y_test, y_pred):.4f}")


# COMBINED

def evaluate_combined(clf_model, reg_model, X_test, y_test_actual_commission):
    conversion_prob = clf_model.predict_proba(X_test)[:, 1]
    predicted_fee = reg_model.predict(X_test)
    expected_commission = conversion_prob * predicted_fee

    mae = mean_absolute_error(y_test_actual_commission, expected_commission)
    print(f"MAE of expected commission per request: {mae:.2f} EUR")
    print(f"Average actual commission per request  : {y_test_actual_commission.mean():.2f} EUR")
    print(f"Average predicted commission per request: {expected_commission.mean():.2f} EUR")
