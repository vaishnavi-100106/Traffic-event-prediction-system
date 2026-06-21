import joblib

model = joblib.load("gridlock2_model.pkl")

print(model.feature_names_in_)
