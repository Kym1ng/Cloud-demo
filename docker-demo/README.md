# Docker Iris Predictor

A containerized ML service for iris flower species prediction using Docker and Google Cloud Run.

## 🏗️ Project Structure

```
docker-demo/
├── Dockerfile          # Container definition
├── app.py             # Flask application
├── requirements.txt   # Python dependencies
├── docker-compose.yml # Local development
├── .dockerignore      # Docker ignore rules
└── README.md         # This file
```

## 🚀 Quick Start

### Local Development

1. **Build and run with Docker Compose:**
```bash
cd docker-demo
docker-compose up --build
```

2. **Test the API:**
```bash
# Health check
curl http://localhost:8080/health

# Make prediction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[2, 3, 1, 4]]}'
```

### Manual Docker Commands

1. **Build the image:**
```bash
docker build -t iris-predictor .
```

2. **Run the container:**
```bash
docker run -p 8080:8080 iris-predictor
```

3. **Tag for Google Container Registry:**
```bash
docker tag iris-predictor gcr.io/YOUR_PROJECT_ID/iris-predictor:v1
```

## ☁️ Google Cloud Deployment

### 1. Build and Push to Google Container Registry

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build the image
docker build -t gcr.io/$PROJECT_ID/iris-predictor:v1 .

# Push to Google Container Registry
docker push gcr.io/$PROJECT_ID/iris-predictor:v1
```

### 2. Deploy to Google Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy iris-predictor \
  --image gcr.io/$PROJECT_ID/iris-predictor:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### 3. Alternative: Deploy to Google Cloud Functions (2nd Gen)

```bash
# Deploy as Cloud Function
gcloud functions deploy iris-predictor \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=predict \
  --trigger-http \
  --allow-unauthenticated
```

## 📡 API Endpoints

### Health Check
```bash
GET /health
```
Returns service status and model loading status.

### Prediction
```bash
POST /predict
Content-Type: application/json

{
  "data": [[sepal_length, sepal_width, petal_length, petal_width]]
}
```

### Example Response
```json
{
  "prediction": [0],
  "species": ["Setosa"],
  "message": "Prediction successful"
}
```

## 🔧 Environment Variables

- `PORT`: Server port (default: 8080)
- `HOST`: Server host (default: 0.0.0.0)

## 🐳 Docker Commands Reference

### Build
```bash
docker build -t iris-predictor .
```

### Run
```bash
docker run -p 8080:8080 iris-predictor
```

### Tag
```bash
docker tag iris-predictor gcr.io/PROJECT_ID/iris-predictor:v1
```

### Push
```bash
docker push gcr.io/PROJECT_ID/iris-predictor:v1
```

### Pull
```bash
docker pull gcr.io/PROJECT_ID/iris-predictor:v1
```

## 🧪 Testing

### Local Testing
```bash
# Health check
curl http://localhost:8080/health

# Prediction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}'
```

### Production Testing
```bash
# Replace with your Cloud Run URL
curl -X POST https://iris-predictor-xxxxx-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}'
```

## 📊 Performance

- **Model Loading:** ~100ms (cold start)
- **Prediction:** ~10ms
- **Container Size:** ~200MB
- **Memory Usage:** ~150MB

## 🔒 Security

- CORS enabled for web applications
- No authentication required (public API)
- Input validation on all endpoints
- Error handling with proper HTTP status codes

## 🚀 Next Steps

1. Add authentication
2. Implement rate limiting
3. Add monitoring and logging
4. Set up CI/CD pipeline
5. Add model versioning
