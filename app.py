from flask import Flask, request, render_template
import joblib
import numpy as np
import pandas as pd
import os



app = Flask(__name__)


# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use a relative path for the scaler file
scaler_path = os.path.join(BASE_DIR, "models", "sc.sav")
model_path = os.path.join(BASE_DIR, "models", "lgb_model.pkl")

# Load the scaler and model
scaler = joblib.load(scaler_path)
model = joblib.load(model_path)

# Define feature names used in training
feature_names = [
    "item_weight", "item_fat_content", "item_visibility", "item_type", 
    "item_mrp", "outlet_establishment_year", "outlet_size", 
    "outlet_location_type", "outlet_type"
]
@app.route("/")
def index():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input values from form
        input_data = {
            "item_weight": float(request.form["item_weight"]),
            "item_fat_content": float(request.form["item_fat_content"]),
            "item_visibility": float(request.form["item_visibility"]),
            "item_type": float(request.form["item_type"]),
            "item_mrp": float(request.form["item_mrp"]),
            "outlet_establishment_year": float(request.form["outlet_establishment_year"]),
            "outlet_size": float(request.form["outlet_size"]),
            "outlet_location_type": float(request.form["outlet_location_type"]),
            "outlet_type": float(request.form["outlet_type"]),
        }

        # Convert input to DataFrame with correct feature names
        X_df = pd.DataFrame([input_data], columns=feature_names)

        # Transform input using the loaded scaler
        X_scaled = scaler.transform(X_df)

        # Predict sales using the trained model
        prediction = float(model.predict(X_scaled)[0])

        # Render the results page with prediction value
        return render_template("results.html", prediction=round(prediction, 2))

    except Exception as e:
        return render_template("results.html", prediction="Error: " + str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

