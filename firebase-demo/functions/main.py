# main.py

import joblib
from google.cloud import storage
import os
from firebase_functions import https_fn

# Don't initialize storage client at module level
model = None

def download_model_from_gcs():
    """Downloads the model from GCS and loads it."""
    try:
        # Initialize storage client inside function
        storage_client = storage.Client()
        
        # Get bucket name from environment variable
        bucket_name = os.environ.get("GCS_BUCKET")
        
        if not bucket_name:
            raise Exception("GCS_BUCKET environment variable not set. Please set it in Firebase console or use environment variables.")

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob("models/iris_model.pkl")
        
        download_path = "/tmp/iris_model.pkl"
        blob.download_to_filename(download_path)
        
        return joblib.load(download_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

# This decorator tells Firebase this is an HTTP-triggered function
@https_fn.on_request(max_instances=10)
def iris_predictor(req: https_fn.Request) -> https_fn.Response:
    """The main entry point for the Cloud Function."""
    global model

    # Handle CORS preflight requests
    if req.method == 'OPTIONS':
        return https_fn.Response(
            '',
            status=200,
            headers={
                'Access-Control-Allow-Origin': 'https://cloud-demo-6a36f.web.app',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
        )

    try:
        # Load the model if it's not already in memory
        if model is None:
            model = download_model_from_gcs()

        # Get the JSON data from the request
        request_json = req.get_json(silent=True)
        if not request_json or 'data' not in request_json:
            return https_fn.Response(
                "Bad request: JSON payload with 'data' key is required.", 
                status=400,
                headers={
                    'Access-Control-Allow-Origin': 'https://cloud-demo-6a36f.web.app',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            )

        # Make a prediction
        data = request_json['data']
        prediction = model.predict(data)
        # Return the prediction as JSON
        return https_fn.Response(
            f'{{"prediction":{prediction.tolist()}}}', 
            status=200, 
            headers={
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': 'https://cloud-demo-6a36f.web.app',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        )
    except Exception as e:
        print(f"Error in iris_predictor: {e}")
        return https_fn.Response(
            f"Error during prediction: {e}", 
            status=500,
            headers={
                'Access-Control-Allow-Origin': 'https://cloud-demo-6a36f.web.app',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        )