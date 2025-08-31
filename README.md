# 🌟 Cloud Demo - Machine Learning Deployment Showcase

A comprehensive demonstration of deploying a machine learning model (Iris Flower Predictor) using three different cloud deployment approaches.

## 🏗️ Project Overview

This project showcases how to deploy the same ML model using different cloud technologies:

- **Google Cloud Functions** - Serverless function deployment
- **Firebase Hosting + Functions** - Web app with serverless backend
- **Docker + Google Cloud Run** - Containerized deployment

## 📁 Project Structure

```
cloud demo/
├── deploy/                    # Google Cloud Functions (1st Gen)
│   ├── main.py               # Cloud Function code
│   └── requirements.txt      # Python dependencies
├── firebase-demo/            # Firebase Hosting + Functions
│   ├── functions/
│   │   ├── main.py          # Firebase Function code
│   │   └── requirements.txt # Python dependencies
│   ├── public/
│   │   └── index.html       # Web interface
│   └── firebase.json        # Firebase configuration
├── docker-demo/              # Docker + Cloud Run
│   ├── Dockerfile           # Container definition
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── templates/
│   │   └── index.html     # Beautiful web interface
│   └── docker-compose.yml  # Local development
├── iris_model.pkl          # Trained ML model
├── model_download.py       # Model training script
└── README.md              # This file
```

## 🚀 Deployment Approaches

### 1. 📦 **Google Cloud Functions** (`deploy/`)

**Best for:** Simple API endpoints, event-driven functions

**Features:**
- ✅ **Serverless** - No server management
- ✅ **Auto-scaling** - Scales to zero
- ✅ **Simple deployment** - Single function
- ✅ **Cost-effective** - Pay per request

**Deployment:**
```bash
cd deploy
gcloud functions deploy iris-predictor \
  --runtime=python311 \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars GCS_BUCKET=your-bucket-name
```

**API Endpoint:**
```
https://us-central1-PROJECT_ID.cloudfunctions.net/iris-predictor
```

### 2. 🌐 **Firebase Hosting + Functions** (`firebase-demo/`)

**Best for:** Web applications with backend APIs

**Features:**
- ✅ **Web interface** - Beautiful HTML/CSS/JS
- ✅ **Serverless backend** - Firebase Functions
- ✅ **Global CDN** - Fast worldwide access
- ✅ **Integrated hosting** - One deployment

**Deployment:**
```bash
cd firebase-demo
firebase deploy
```

**Web App:**
```
https://PROJECT_ID.web.app
```

### 3. 🐳 **Docker + Google Cloud Run** (`docker-demo/`)

**Best for:** Complex applications, microservices, production workloads

**Features:**
- ✅ **Containerized** - Portable and consistent
- ✅ **Production-ready** - Gunicorn WSGI server
- ✅ **Beautiful UI** - Modern web interface
- ✅ **Full control** - Custom runtime environment

**Deployment:**
```bash
cd docker-demo
docker build -t iris-predictor .
docker tag iris-predictor gcr.io/PROJECT_ID/iris-predictor:v1
docker push gcr.io/PROJECT_ID/iris-predictor:v1
gcloud run deploy iris-predictor --image gcr.io/PROJECT_ID/iris-predictor:v1
```

**Web App:**
```
https://iris-predictor-xxxxx-uc.a.run.app
```

## 🎯 **Comparison Table**

| **Approach** | **Complexity** | **Cost** | **Scalability** | **Best For** |
|--------------|----------------|----------|-----------------|--------------|
| **Cloud Functions** | ⭐⭐ | 💰💰 | ⭐⭐⭐⭐ | Simple APIs |
| **Firebase** | ⭐⭐⭐ | 💰💰💰 | ⭐⭐⭐ | Web apps |
| **Docker + Cloud Run** | ⭐⭐⭐⭐ | 💰💰💰💰 | ⭐⭐⭐⭐⭐ | Production apps |

## 🧪 **Testing Each Approach**

### **1. Cloud Functions:**
```bash
curl -X POST https://us-central1-PROJECT_ID.cloudfunctions.net/iris-predictor \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}'
```

### **2. Firebase:**
```bash
# Visit: https://PROJECT_ID.web.app
# Or test API:
curl -X POST https://us-central1-PROJECT_ID.cloudfunctions.net/iris_predictor \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}'
```

### **3. Docker + Cloud Run:**
```bash
# Visit: https://iris-predictor-xxxxx-uc.a.run.app
# Or test API:
curl -X POST https://iris-predictor-xxxxx-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}'
```

## 🔧 **Prerequisites**

### **Required Tools:**
- **Google Cloud CLI** (`gcloud`)
- **Firebase CLI** (`firebase`)
- **Docker Desktop**
- **Python 3.11+**

### **Required Services:**
- **Google Cloud Project** with billing enabled
- **Firebase Project** (for Firebase deployment)
- **Google Container Registry** (for Docker deployment)

## 📊 **Model Information**

### **Iris Flower Dataset:**
- **Features:** Sepal length, sepal width, petal length, petal width
- **Target:** Species (Setosa, Versicolor, Virginica)
- **Algorithm:** Logistic Regression
- **Accuracy:** ~96%

### **API Format:**
```json
{
  "data": [[sepal_length, sepal_width, petal_length, petal_width]]
}
```

### **Response Format:**
```json
{
  "prediction": [0],
  "species": ["Setosa"],
  "message": "Prediction successful"
}
```

## 🚀 **Quick Start**

### **Choose Your Approach:**

1. **For Simple API:** Use `deploy/` (Cloud Functions)
2. **For Web App:** Use `firebase-demo/` (Firebase)
3. **For Production:** Use `docker-demo/` (Docker + Cloud Run)

### **Each folder contains:**
- ✅ **Complete deployment instructions**
- ✅ **Local testing setup**
- ✅ **Production deployment guide**
- ✅ **Troubleshooting tips**

## 🎯 **Learning Objectives**

This project demonstrates:

- ✅ **Multiple deployment strategies**
- ✅ **Cloud-native development**
- ✅ **Containerization with Docker**
- ✅ **Serverless computing**
- ✅ **Web application development**
- ✅ **API design and testing**
- ✅ **Cloud platform integration**

## 🔗 **Useful Links**

- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Docker Documentation](https://docs.docker.com/)

## 📝 **Notes**

- **Environment Variables:** Each approach handles configuration differently
- **CORS:** Firebase and Docker versions include CORS headers
- **Error Handling:** All versions include comprehensive error handling
- **Monitoring:** Each deployment includes health check endpoints

## 🎉 **Success Criteria**

✅ **All three deployments working**
✅ **Web interfaces accessible**
✅ **API endpoints responding**
✅ **Predictions accurate**
✅ **Error handling implemented**

---

**Choose your preferred approach and start deploying!** 🚀
