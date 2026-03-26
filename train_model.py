import pandas as pd
import os
import sys
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =====================================================
# 1. CHECK FILE EXISTS
# =====================================================

FILE_PATH = "protein_and_gene.xlsx"

if not os.path.exists(FILE_PATH):
    print("❌ ERROR: Dataset file not found:", FILE_PATH)
    sys.exit()


# =====================================================
# 2. LOAD DATASET SAFELY
# =====================================================

try:
    df = pd.read_excel(FILE_PATH)
    print("✅ Dataset loaded successfully")
except Exception as e:
    print("❌ ERROR loading dataset:", e)
    sys.exit()


# =====================================================
# 3. VALIDATE REQUIRED COLUMNS
# =====================================================

required_cols = [
    "Reviewed",
    "Entry Name",
    "Protein names",
    "Gene Names",
    "Organism",
    "Length"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    print("❌ Missing columns:", missing)
    sys.exit()

print("✅ Column validation passed")


# =====================================================
# 4. DROP UNUSED COLUMNS
# =====================================================

if "Entry" in df.columns:
    df = df.drop(columns=["Entry"])


# =====================================================
# 5. HANDLE MISSING VALUES
# =====================================================

if df.isnull().sum().sum() > 0:
    print("⚠ Missing values detected — filling with 'Unknown'")
    df = df.fillna("Unknown")


# =====================================================
# 6. ENCODE TEXT COLUMNS SAFELY
# =====================================================

encoders = {}

for col in df.columns:

    # Skip target column
    if col == "Length":
        continue

    try:
        df[col] = df[col].astype(str)

        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

        encoders[col] = le

    except Exception as e:
        print(f"❌ Encoding failed for column {col}:", e)
        sys.exit()

print("✅ Encoding successful")


# =====================================================
# 7. FINAL NUMERIC VALIDATION
# =====================================================

if not all(df.dtypes.apply(lambda x: x != "object")):
    print("❌ ERROR: Dataset still contains text columns")
    print(df.dtypes)
    sys.exit()

print("✅ All features numeric — ready for training")


# =====================================================
# 8. SEPARATE FEATURES & TARGET
# =====================================================

if "Length" not in df.columns:
    print("❌ Target column missing")
    sys.exit()

X = df.drop(columns=["Length"])
y = df["Length"]

if X.empty:
    print("❌ Feature set is empty")
    sys.exit()

print("✅ Feature split successful")


# =====================================================
# 9. TRAIN TEST SPLIT
# =====================================================

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    print("✅ Train/Test split successful")
except Exception as e:
    print("❌ Train-test split failed:", e)
    sys.exit()


# =====================================================
# 10. CREATE MODEL
# =====================================================

try:
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        random_state=42
    )
    print("✅ Model initialized")
except Exception as e:
    print("❌ Model creation failed:", e)
    sys.exit()


# =====================================================
# 11. TRAIN MODEL
# =====================================================

try:
    model.fit(X_train, y_train)
    print("✅ Model training complete")
except Exception as e:
    print("❌ Training failed:", e)
    sys.exit()


# =====================================================
# 12. PREDICT
# =====================================================

try:
    preds = model.predict(X_test)
except Exception as e:
    print("❌ Prediction failed:", e)
    sys.exit()


# =====================================================
# 13. EVALUATE MODEL
# =====================================================

try:
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print("\n📊 MODEL PERFORMANCE")
    print("MAE:", round(mae, 2))
    print("R2 Score:", round(r2, 3))

except Exception as e:
    print("❌ Evaluation failed:", e)
    sys.exit()


# =====================================================
# 14. SAVE MODEL FILES
# =====================================================

try:
    joblib.dump(model, "protein_rf_model.pkl")
    joblib.dump(encoders, "encoders.pkl")

    print("\n✅ Model + encoders saved successfully")

except Exception as e:
    print("❌ Saving failed:", e)
    sys.exit()