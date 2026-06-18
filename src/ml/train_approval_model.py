import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from src.ml.data_loader import load_loan_approval_training_data
from src.ml.feature_engineering import create_features
from src.ml.feature_registry import APPROVAL_MODEL_FEATURES


# =========================
# LOAD DATA
# =========================
df = load_loan_approval_training_data()
df = create_features(df)

# =========================
# TARGET
# =========================
df["loan_approved"] = (df["loan_status"] == "Approved").astype(int)
y = df["loan_approved"]

# =========================
# FEATURES (SAFE SOURCE)
# =========================
features = [f for f in APPROVAL_MODEL_FEATURES if f in df.columns]

X = df[features].copy()

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

categorical_features = [c for c in categorical_features if c in X.columns]

numerical_features = [c for c in X.columns if c not in categorical_features]

# =========================
# PREPROCESSOR
# =========================
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ("num", "passthrough", numerical_features)
])

# =========================
# SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# MODEL
# =========================
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42,
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
# EVAL
# =========================
pred = pipeline.predict(X_test)
proba = pipeline.predict_proba(X_test)[:, 1]

print(classification_report(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, proba))

# =========================
# SAVE (SAFE)
# =========================
joblib.dump(pipeline, "src/ml/models/loan_approval_model.pkl")

print("Model saved successfully")