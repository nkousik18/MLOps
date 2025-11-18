

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

# 1. Configure MLflow Tracking Server

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Lab1 - Multi-Model Comparison")

# 2. Load dataset: diabeties dataset

data = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# 3. Define models to compare

models = {
    "ElasticNet_default": ElasticNet(alpha=0.5, l1_ratio=0.5, random_state=42),
    "ElasticNet_alpha_0.1": ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
    "ElasticNet_alpha_1.0": ElasticNet(alpha=1.0, l1_ratio=0.5, random_state=42),

    "RandomForest": RandomForestRegressor(n_estimators=150, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),

    "Scaled_ElasticNet": Pipeline([
        ("scaler", StandardScaler()),
        ("model", ElasticNet(alpha=0.5, l1_ratio=0.5, random_state=42))
    ])
}


# 4. Train and log each model with MLflow

for model_name, model in models.items():

    with mlflow.start_run(run_name=model_name):

        # model training

        model.fit(X_train, y_train)

        # Prediction
        preds = model.predict(X_test)


        # Compute metrics
        mse = mean_squared_error(y_test, preds)
        rmse = mse ** 0.5
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)


        # Log parameters safely based on the model type
        mlflow.log_param("model_name", model_name)

        # If ElasticNet inside a pipeline
        if model_name == "Scaled_ElasticNet":
            mlflow.log_param("alpha", model.named_steps["model"].alpha)
            mlflow.log_param("l1_ratio", model.named_steps["model"].l1_ratio)

        # If standalone ElasticNet
        elif isinstance(model, ElasticNet):
            mlflow.log_param("alpha", model.alpha)
            mlflow.log_param("l1_ratio", model.l1_ratio)


        # Log metrics

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)


        # Log the model as an artifact

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
        )

        print(f"Logged: {model_name} | RMSE={rmse:.3f} | R2={r2:.3f}")

print("All models logged successfully!")
