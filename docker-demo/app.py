import os
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model at startup
model = None

def load_model():
    """Load the ML model."""
    global model
    try:
        model = joblib.load('iris_model.pkl')
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    """Predict iris species endpoint."""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({"error": "Bad request: JSON payload with 'data' key is required."}), 400
        
        # Make prediction
        prediction = model.predict(data['data'])
        
        # Map prediction to species names
        species = ['Setosa', 'Versicolor', 'Virginica']
        predicted_species = [species[pred] for pred in prediction]
        
        return jsonify({
            "prediction": prediction.tolist(),
            "species": predicted_species,
            "message": "Prediction successful"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with usage instructions."""
    return jsonify({
        "message": "Iris Predictor API",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "usage": "Send POST request to /predict with JSON: {\"data\": [[sepal_length, sepal_width, petal_length, petal_width]]}"
        }
    })

if __name__ == '__main__':
    # Load model before starting the server
    load_model()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
