import joblib

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, roc_auc_score

from src.ml.data_loader import load_loan_approval_training_data
from src.ml.feature_engineering import create_features, get_approval_model_features


# =========================
# LOAD DATA
# =========================
df = load_loan_approval_training_data()
df = create_features(df)

# =========================
# TARGET
# =========================
df["default_flag"] = (df["default_history_count"] > 0).astype(int)

features = get_approval_model_features()

X = df[features]
y = df["default_flag"]

# =========================
# CATEGORICAL COLUMNS
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

numerical_features = [
    col for col in features
    if col not in categorical_features
]

# =========================
# PREPROCESSOR
# =========================
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numerical_features)
    ]
)

# =========================
# MODEL (XGBOOST)
# =========================
model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42
)

# =========================
# PIPELINE (IMPORTANT FIX)
# =========================
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# TRAIN
# =========================
pipeline.fit(X_train, y_train)

# =========================
# PREDICT
# =========================
pred = pipeline.predict(X_test)
proba = pipeline.predict_proba(X_test)[:, 1]

print(classification_report(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, proba))

# =========================
# SAVE MODEL
# =========================
joblib.dump(pipeline, "src/ml/models/default_risk_model.pkl")

print("Model saved successfully")