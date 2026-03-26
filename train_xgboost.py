import pandas as pd
import os
import sys
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
from xgboost import XGBClassifier, XGBRegressor


# =====================================================
# 1. FILE CHECK
# =====================================================

FILE = "drug_discovery_virtual_screening.csv"

if not os.path.exists(FILE):
    print("❌ Dataset not found")
    sys.exit()

print("✅ File found")


# =====================================================
# 2. LOAD DATASET
# =====================================================

try:
    df = pd.read_csv(FILE)
    print("✅ Dataset loaded")
except Exception as e:
    print("❌ Failed to load dataset:", e)
    sys.exit()

print("Dataset shape:", df.shape)


# =====================================================
# 3. HANDLE MISSING VALUES
# =====================================================

df = df.fillna(0)


# =====================================================
# 4. DROP TRUE ID COLUMNS
# =====================================================

id_columns = ["compound_id", "protein_id"]

for col in id_columns:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)
        print(f"⚠ Dropped ID column: {col}")


# =====================================================
# 5. EXPLICIT TARGET SELECTION
# =====================================================

# 🔥 IMPORTANT: Set your real target column here
TARGET_COLUMN = "binding_affinity"   # ← CHANGE IF NEEDED

if TARGET_COLUMN not in df.columns:
    print(f"❌ Target column '{TARGET_COLUMN}' not found")
    sys.exit()

y = df[TARGET_COLUMN]
X = df.drop(columns=[TARGET_COLUMN])

print("✅ Target column:", TARGET_COLUMN)


# =====================================================
# 6. ENCODE NON-NUMERIC FEATURES
# =====================================================

encoders = {}

for col in X.columns:
    if not pd.api.types.is_numeric_dtype(X[col]):
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

print("✅ Encoding complete")


# =====================================================
# 7. DETECT PROBLEM TYPE
# =====================================================

if len(np.unique(y)) <= 10:
    problem_type = "classification"
else:
    problem_type = "regression"

print("🔍 Detected problem type:", problem_type)


# =====================================================
# 8. TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("✅ Train/Test split complete")


# =====================================================
# 9. HANDLE CLASS IMBALANCE (IF CLASSIFICATION)
# =====================================================

scale_pos_weight = 1

if problem_type == "classification":
    counts = y.value_counts()
    if len(counts) == 2:
        scale_pos_weight = counts[0] / counts[1]
        print("⚖ scale_pos_weight:", round(scale_pos_weight, 2))


# =====================================================
# 10. TRAIN MODEL
# =====================================================

try:

    if problem_type == "classification":
        model = XGBClassifier(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            random_state=42,
            eval_metric="logloss",
            scale_pos_weight=scale_pos_weight
        )
    else:
        model = XGBRegressor(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            random_state=42
        )

    model.fit(X_train, y_train)
    print("✅ Model trained successfully")

except Exception as e:
    print("❌ Training failed:", e)
    sys.exit()


# =====================================================
# 11. EVALUATE
# =====================================================

preds = model.predict(X_test)

print("\n📊 MODEL PERFORMANCE")

if problem_type == "classification":
    acc = accuracy_score(y_test, preds)
    print("Accuracy:", round(acc, 4))
    print(classification_report(y_test, preds))
else:
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print("MAE:", round(mae, 4))
    print("R²:", round(r2, 4))


# =====================================================
# 12. FEATURE IMPORTANCE
# =====================================================

importance = pd.Series(model.feature_importances_, index=X.columns)
importance = importance.sort_values(ascending=False)

print("\n🔥 Top 5 Important Features:")
print(importance.head())


# =====================================================
# 13. SAVE MODEL
# =====================================================

joblib.dump(model, "xgboost_model.pkl")
joblib.dump(encoders, "xgb_encoders.pkl")
joblib.dump(X.columns.tolist(), "feature_names.pkl")

print("\n✅ Model + encoders + feature names saved successfully")