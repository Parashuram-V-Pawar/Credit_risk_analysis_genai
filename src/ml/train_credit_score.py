import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

from src.ml.data_loader import load_credit_training_data
from src.ml.feature_engineering import create_features, get_credit_score_features


# =========================
# 1. LOAD DATA
# =========================
df = load_credit_training_data()

# =========================
# 2. FEATURE ENGINEERING (MUST COME FIRST)
# =========================
df = create_features(df)

# =========================
# 3. VERIFY FEATURES EXIST (DEBUG STEP)
# =========================
required_features = get_credit_score_features()

missing = [f for f in required_features if f not in df.columns]

if missing:
    raise ValueError(f"Missing features in dataset: {missing}")

# =========================
# 4. SPLIT X / Y
# =========================
X = df[required_features].copy()
y = df["cibil_score"]

# =========================
# 5. CATEGORICAL FEATURES
# =========================
categorical_features = [
    "gender", "married", "education",
    "occupation", "employment_status",
    "business_type", "organization_type"
]

categorical_features = [c for c in categorical_features if c in X.columns]

numerical_features = [c for c in X.columns if c not in categorical_features]

# =========================
# 6. PREPROCESSOR
# =========================
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numerical_features)
    ]
)

# =========================
# 7. MODEL
# =========================
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# =========================
# 8. TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# =========================
# 9. TRAIN
# =========================
pipeline.fit(X_train, y_train)

# =========================
# 10. EVALUATE
# =========================
pred = pipeline.predict(X_test)

print("MAE:", mean_absolute_error(y_test, pred))
print("R2:", r2_score(y_test, pred))

# =========================
# 11. SAVE
# =========================
joblib.dump(pipeline, "src/ml/models/credit_score_model.pkl")

print("Model saved successfully")