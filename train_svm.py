import pandas as pd
import sys
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


# =====================================================
# 1. FILE CHECK
# =====================================================

FILE = "miRNA.xlsx"

if not os.path.exists(FILE):
    print("❌ Dataset not found")
    sys.exit()

print("✅ File found")


# =====================================================
# 2. LOAD DATASET
# =====================================================

try:
    df = pd.read_excel(FILE, header=None)
    print("✅ Dataset loaded")
except Exception as e:
    print("❌ Load failed:", e)
    sys.exit()


# =====================================================
# 3. SET HEADER ROW
# =====================================================

df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)

# FIX COLUMN NAME TYPES
df.columns = df.columns.astype(str).str.strip()

print("✅ Header fixed")


# =====================================================
# 4. REMOVE DUPLICATE COLUMNS
# =====================================================

df = df.loc[:, ~df.columns.duplicated()]

print("✅ Duplicate columns removed if any")


# =====================================================
# 5. HANDLE MISSING VALUES
# =====================================================

if df.isnull().sum().sum() > 0:
    print("⚠ Missing values detected → filling")
    df = df.fillna(0)


# =====================================================
# 6. ENCODE TEXT COLUMNS
# =====================================================

encoders = {}

for col in df.columns:

    if df[col].dtype == "object":
        try:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        except Exception as e:
            print(f"❌ Encoding failed for {col}:", e)
            sys.exit()

print("✅ Encoding done")


# =====================================================
# 7. CONVERT ALL TO NUMERIC
# =====================================================

try:
    df = df.astype(float)
except Exception as e:
    print("❌ Numeric conversion failed:", e)
    sys.exit()

print("✅ Numeric conversion done")


# =====================================================
# 8. REMOVE CONSTANT COLUMNS (IMPORTANT)
# =====================================================

constant_cols = [col for col in df.columns if df[col].nunique() <= 1]

if constant_cols:
    print("⚠ Removing constant columns:", constant_cols)
    df = df.drop(columns=constant_cols)


# =====================================================
# 9. FEATURES & TARGET
# =====================================================

if df.shape[1] < 2:
    print("❌ Not enough columns for training")
    sys.exit()

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

if X.empty:
    print("❌ Features empty")
    sys.exit()

print("✅ Features prepared")


# =====================================================
# 10. SCALE FEATURES
# =====================================================

try:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("✅ Scaling complete")
except Exception as e:
    print("❌ Scaling failed:", e)
    sys.exit()


# =====================================================
# 11. TRAIN TEST SPLIT
# =====================================================

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y,
        test_size=0.2,
        random_state=42
    )
    print("✅ Split complete")
except Exception as e:
    print("❌ Split failed:", e)
    sys.exit()


# =====================================================
# 12. TRAIN SVM MODEL
# =====================================================

try:
    model = SVR(kernel="rbf", C=100, gamma="scale")
    model.fit(X_train, y_train)
    print("✅ Model trained")
except Exception as e:
    print("❌ Training failed:", e)
    sys.exit()


# =====================================================
# 13. PREDICT
# =====================================================

try:
    preds = model.predict(X_test)
except Exception as e:
    print("❌ Prediction failed:", e)
    sys.exit()


# =====================================================
# 14. EVALUATE
# =====================================================

try:
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print("\n📊 MODEL PERFORMANCE")
    print("MAE:", round(mae, 3))
    print("R²:", round(r2, 3))

except Exception as e:
    print("❌ Evaluation failed:", e)
    sys.exit()


# =====================================================
# 15. SAVE MODEL
# =====================================================

try:
    joblib.dump(model, "svm_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(encoders, "encoders.pkl")

    print("\n✅ Model + scaler + encoders saved successfully")

except Exception as e:
    print("❌ Saving failed:", e)
    sys.exit()