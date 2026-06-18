import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder

from src.ml.data_loader import load_credit_training_data
from src.ml.utils import remove_new_to_credit_customers
from src.ml.feature_engineering import create_features, get_credit_score_features

# Load data
df = load_credit_training_data()
numeric_cols = df.select_dtypes(
    include=["int64", "float64"]
).columns

# Create new features(Feature Engineering)
df = create_features(df)

# Remove new customers from dataset
df = remove_new_to_credit_customers(df)

# Define x and y
features = get_credit_score_features()
X = df[features]
y = df["cibil_score"]

# defining categorical columns
categorical_features = [
    "gender", "married", "education",
    "occupation", "employment_status",
    "business_type","organization_type"
]

# defining numerical columns
numerical_features = [feature
                     for feature in features
                     if feature not in categorical_features
                    ]

# Preprocessing dataset to normalize all columns
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

# Split dataset for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# create model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

# Pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# Training the model
pipeline.fit(X_train, y_train)

# Testing model on testing data
predictions = pipeline.predict(X_test)

# Evaluating model performance
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"MAE : {mae:.2f}")
print(f"R²  : {r2:.4f}")

joblib.dump(
    pipeline,
    "src/ml/models/credit_score_model.pkl"
)