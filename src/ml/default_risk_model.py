import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from src.ml.data_loader import load_loan_approval_training_data
from src.ml.feature_engineering import (
create_features,
get_approval_model_features
)

# =========================
# LOAD DATA
# =========================

df = load_loan_approval_training_data()

# Feature Engineering

df = create_features(df)

# =========================
# TARGET
# =========================

df["default_flag"] = (
df["default_history_count"] > 0
).astype(int)

y = df["default_flag"]

# =========================
# FEATURES
# =========================

features = get_approval_model_features()

# Remove target/leakage columns if present

leakage_cols = [
"default_flag",
"loan_status",
"loan_approved"
]

features = [
col for col in features
if col not in leakage_cols
]

X = df[features].copy()

print("\nTarget Distribution:")
print(y.value_counts())

# =========================
# CATEGORICAL FEATURES
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

categorical_features = [
col for col in categorical_features
if col in X.columns
]

# =========================
# NUMERICAL FEATURES
# =========================

numerical_features = [
col for col in X.columns
if col not in categorical_features
]

# =========================
# PREPROCESSOR
# =========================

preprocessor = ColumnTransformer(
transformers=[
(
"cat",
OneHotEncoder(handle_unknown="ignore"),
categorical_features
),
(
"num",
"passthrough",
numerical_features
)
]
)

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.20,
random_state=42,
stratify=y
)

# =========================
# CLASS IMBALANCE
# =========================

scale_pos_weight = (
len(y_train[y_train == 0])
/
max(len(y_train[y_train == 1]), 1)
)

# =========================
# MODEL
# =========================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

# =========================
# PIPELINE
# =========================

pipeline = Pipeline([
("preprocessor", preprocessor),
("model", model)
])

# =========================
# TRAIN
# =========================

pipeline.fit(X_train, y_train)

# =========================
# PREDICT
# =========================

y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

# =========================
# EVALUATION
# =========================

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nROC-AUC Score:")
print(roc_auc_score(y_test, y_proba))

# =========================
# SAVE MODEL
# =========================

joblib.dump(
pipeline,
"src/ml/models/default_risk_model.pkl"
)

print(
"\nModel saved to "
"src/ml/models/default_risk_model.pkl"
)
