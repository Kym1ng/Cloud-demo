import joblib
from google.cloud import storage

# Initialize the GCS client
storage_client = storage.Client()
model = None

def download_model_from_gcs():
    """Downloads the model from GCS and loads it."""
    # --- ACTION FOR YOU ---
    # Replace with your actual bucket name
    bucket_name = "cloud-ai-platform-0008304c-88fc-442a-91bc-467e3d6a002d"
    model_path = "models/iris_model.pkl" # The path to your model in the bucket
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(model_path)
    
    # Download to a temporary directory
    blob.download_to_filename("/tmp/iris_model.pkl")
    
    return joblib.load("/tmp/iris_model.pkl")

def handle_request(request):
    """
    The main entry point for the Cloud Function.
    Handles incoming HTTP POST requests.
    """
    global model

    # Load the model if it's not already in memory
    if model is None:
        model = download_model_from_gcs()

    # Get the JSON data from the request
    request_json = request.get_json(silent=True)
    if not request_json or 'data' not in request_json:
        return ("Bad request: JSON payload with 'data' key is required.", 400)

    # Make a prediction
    try:
        data = request_json['data']
        prediction = model.predict(data)
        # Return the prediction as JSON
        return {"prediction": prediction.tolist()}
    except Exception as e:
        return (f"Error during prediction: {e}", 500)