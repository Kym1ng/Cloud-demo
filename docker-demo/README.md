# 🐳 Docker Iris Predictor

A containerized ML service for iris flower species prediction using Docker and Google Cloud Run.

## 🏗️ Project Structure

```
docker-demo/
├── Dockerfile              # Container definition
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Local development setup
├── .dockerignore          # Docker ignore rules
├── iris_model.pkl         # ML model file
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Docker Desktop** installed and running
2. **Google Cloud CLI** configured
3. **Google Cloud Project** with billing enabled

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

### Step 1: Start Docker Desktop
```bash
# Make sure Docker Desktop is running
# Check Docker status
docker --version
docker ps
```

### Step 2: Build the Docker Image
```bash
cd docker-demo
docker build -t iris-predictor .
```

**Expected Output:**
```
Sending build context to Docker daemon...
Step 1/8 : FROM python:3.11-slim
...
Successfully built abc123def456
Successfully tagged iris-predictor:latest
```

### Step 3: Test Locally
```bash
# Run the container locally
docker run -p 8080:8080 iris-predictor

# In another terminal, test the API
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[2, 3, 1, 4]]}'
```

### Step 4: Configure Google Cloud
```bash
# Set your project ID
export PROJECT_ID=dev-solstice-460607-q5

# Configure Docker for Google Container Registry
gcloud auth configure-docker
```

### Step 5: Tag for Google Container Registry
```bash
# Tag the image for GCR
docker tag iris-predictor gcr.io/$PROJECT_ID/iris-predictor:v1
```

### Step 6: Push to Google Container Registry
```bash
# Push the image
docker push gcr.io/$PROJECT_ID/iris-predictor:v1
```

**Expected Output:**
```
The push refers to repository [gcr.io/dev-solstice-460607-q5/iris-predictor]
abc123def456: Pushed
v1: digest: sha256:... size: 1234
```

### Step 7: Deploy to Google Cloud Run
```bash
# Deploy to Cloud Run
gcloud run deploy iris-predictor \
  --image gcr.io/$PROJECT_ID/iris-predictor:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

**Expected Output:**
```
Deploying container to Cloud Run service [iris-predictor] in project [dev-solstice-460607-q5] region [us-central1]
✓ Deploying... Done.
✓ Creating Revision...
✓ Routing traffic...
Done.
Service URL: https://iris-predictor-xxxxx-uc.a.run.app
```

### Step 8: Test the Deployed Service
```bash
# Test health endpoint
curl https://iris-predictor-xxxxx-uc.a.run.app/health

# Test prediction endpoint
curl -X POST https://iris-predictor-xxxxx-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}'
```

## 🔄 Alternative: Deploy to Cloud Functions (2nd Gen)

If you prefer Cloud Functions over Cloud Run:

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

## 📊 Monitoring and Logs

### View Cloud Run Logs
```bash
gcloud logs read --service=iris-predictor --limit=50
```

### View Cloud Function Logs
```bash
gcloud functions logs read iris-predictor --limit=50
```

## 🔧 Troubleshooting

### Common Issues:

1. **Docker daemon not running:**
   ```bash
   # Start Docker Desktop
   open -a Docker
   ```

2. **Authentication issues:**
   ```bash
   gcloud auth login
   gcloud auth configure-docker
   ```

3. **Permission denied:**
   ```bash
   # Make sure you have the right permissions
   gcloud projects describe $PROJECT_ID
   ```

4. **Image not found:**
   ```bash
   # List your images
   docker images
   # Check GCR
   gcloud container images list --repository=gcr.io/$PROJECT_ID
   ```

## 🎯 Success Criteria

✅ **Local Docker container runs**
✅ **Health endpoint responds**
✅ **Prediction endpoint works**
✅ **Image pushed to GCR**
✅ **Service deployed to Cloud Run**
✅ **Public URL accessible**
✅ **API responds correctly**

## 🚀 Next Steps

1. **Set up CI/CD pipeline**
2. **Add monitoring and alerting**
3. **Implement versioning strategy**
4. **Add authentication**
5. **Set up custom domain**

## 🔗 Useful Commands

```bash
# List running containers
docker ps

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# Remove image
docker rmi iris-predictor

# View container logs
docker logs <container_id>

# Shell into container
docker exec -it <container_id> /bin/bash
```
