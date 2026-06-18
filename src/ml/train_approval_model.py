import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from xgboost import XGBClassifier

from src.ml.data_loader import load_loan_approval_training_data
from src.ml.feature_engineering import create_features, get_approval_model_features


# =========================
# Step 1: Load Data
# =========================
df = load_loan_approval_training_data()
df = create_features(df)

print("\nLoan Status Distribution:")
print(df["loan_status"].value_counts())

# =========================
# Step 2: TARGET (APPROVAL MODEL)
# =========================
df["loan_approved"] = (df["loan_status"] == "Approved").astype(int)

y = df["loan_approved"]

# =========================
# Step 3: FEATURES
# =========================
features = get_approval_model_features()

# 🚨 SAFETY: remove any leakage-like columns if present
leakage_cols = [
    "default_history_count",
    "loan_status",
    "loan_approved"
]

features = [f for f in features if f not in leakage_cols]

X = df[features].copy()

# =========================
# Step 4: Categorical Columns
# =========================
categorical_features = [
    "gender",
    "married",
    "education",
    "occupation",
    "employment_status",
    "business_type",
    "organization_type",
    "purpose_of_loan",
    "property_area"
]

# ensure categorical columns exist in dataset
categorical_features = [col for col in categorical_features if col in X.columns]

numerical_features = [
    col for col in X.columns if col not in categorical_features
]

# =========================
# Step 5: Preprocessor
# =========================
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numerical_features)
    ]
)

# =========================
# Step 6: Train-Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# Step 7: Model (XGBoost)
# =========================
model = XGBClassifier(
    n_estimators=400,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=(
        len(y_train[y_train == 0]) / max(len(y_train[y_train == 1]), 1)
    ),
    random_state=42,
    n_jobs=-1,
    eval_metric="logloss"
)

# =========================
# Step 8: Pipeline
# =========================
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# =========================
# Step 9: Train
# =========================
pipeline.fit(X_train, y_train)

# =========================
# Step 10: Predict
# =========================
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

# =========================
# Step 11: Evaluation
# =========================
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nROC-AUC Score:")
print(roc_auc_score(y_test, y_proba))

# =========================
# Step 12: Save Model
# =========================
joblib.dump(pipeline, "src/ml/models/loan_approval_model.pkl")

print("\nModel saved to src/ml/models/loan_approval_model.pkl")