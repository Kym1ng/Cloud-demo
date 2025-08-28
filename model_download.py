import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

# Load the dataset
X, y = load_iris(return_X_y=True)

# Train a simple model
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save the trained model to a file
joblib.dump(model, 'iris_model.pkl')

print("Model saved as iris_model.pkl!")