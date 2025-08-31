import os
import joblib
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model at startup
model = None

def load_model():
    """Load the ML model."""
    global model
    try:
        print("Loading model...")
        model = joblib.load('iris_model.pkl')
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in directory: {os.listdir('.')}")
        return False

# Load model when app starts (works with Gunicorn)
print("Starting Iris Predictor application...")
if not load_model():
    print("Failed to load model. Application may not work correctly.")

@app.route('/')
def home():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/_ah/health', methods=['GET'])
def google_health_check():
    """Google Cloud health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/startup', methods=['GET'])
def startup_check():
    """Startup check endpoint."""
    if model is not None:
        return jsonify({"status": "ready", "model_loaded": True}), 200
    else:
        return jsonify({"status": "not_ready", "model_loaded": False}), 503

@app.route('/predict', methods=['POST'])
def predict():
    """Predict iris species endpoint."""
    try:
        # Check if model is loaded
        if model is None:
            # Try to load model again
            if not load_model():
                return jsonify({"error": "Model not available"}), 503
        
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

@app.route('/api', methods=['GET'])
def api_docs():
    """API documentation endpoint."""
    return jsonify({
        "message": "Iris Predictor API",
        "endpoints": {
            "web_interface": "/",
            "health": "/health",
            "startup": "/startup",
            "predict": "/predict (POST)",
            "usage": "Send POST request to /predict with JSON: {\"data\": [[sepal_length, sepal_width, petal_length, petal_width]]}"
        }
    })

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Starting server on {host}:{port}")
    print(f"🌐 Web interface: http://{host}:{port}")
    print(f"📡 API endpoints: http://{host}:{port}/api")
    app.run(host=host, port=port, debug=False)
