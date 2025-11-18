
#  **README : MLflow Lab 1: Multi-Model Experiment Tracking**

##  **Objective**

The goal of this lab is to demonstrate how MLflow can be used for **experiment tracking**, **model comparison**, and **artifact logging** by training multiple regression models on the Diabetes dataset and recording their metrics, parameters, and models.

Multi_model)comparision .py has :

* Multiple ML algorithms
* Hyperparameter variations
* Preprocessing pipelines
* Rich metrics and model artifacts
* Visual comparisons

---

##  **Project Structure**

```
Mlflow_Labs/
└── Lab1/
    ├── multi_model_comparison.py    # Main Lab 1 script (enhanced)
    ├── README.md                    # This file
```

Your MLflow tracking server will store all logged runs under:

```
mlruns/
```

---

## ⚙️ **Prerequisites**

Activate your virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install mlflow scikit-learn matplotlib
```

Start MLflow UI:

```bash
mlflow ui --port 5000
```

Open browser:

👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

##  **Running the Lab**

Run the multi-model experiment:

```bash
python Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1/multi_model_comparision.py
```

MLflow will automatically log:

* Parameters
* Metrics
* Models
* Run metadata
* Artifacts

Each run prints its MLflow link in the terminal for easy navigation.

---

##  **Models Compared**

The following models were tracked:

| Model                     | Notes                                 |
| ------------------------- | ------------------------------------- |
| ElasticNet (3 versions)   | Linear regression with regularization |
| RandomForestRegressor     | Tree-based ensemble                   |
| GradientBoostingRegressor | Boosted tree ensemble                 |
| Scaled ElasticNet         | ElasticNet with StandardScaler        |

This allows comparison across architectures, preprocessing, and hyperparameters.

---

##  **Performance Summary**

### **RMSE Comparison**

Lower = better.

![RMSE Chart](attachment\:rmse_plot)

### **R² Comparison**

Higher = better.

![R2 Chart](attachment\:r2_plot)

---

## **Insights from Results**

### 1. **ElasticNet performs poorly without scaling**

* RMSE ~72
* R² ~0
  Linear models cannot capture nonlinear patterns in the Diabetes dataset.

---

### 2. **Tree-based models significantly outperform linear models**

* RandomForest RMSE ≈ 54.7
* GradientBoosting RMSE ≈ 53.8

They capture feature interactions and nonlinear relationships naturally.

---

### 3. **Scaling dramatically improves ElasticNet**

* Scaled ElasticNet RMSE drops to **53.38**, best overall
* Shows the importance of preprocessing steps
* MLflow tracks these transformations as part of the pipeline

---

### 4. **MLflow lets you compare everything at a glance**

The MLflow UI clearly displays:

* Metric trends
* Parameter effects
* Best model automatically
* Artifacts for each model
* Run-by-run comparison


---

## **Artifacts Logged Per Run**

Each run includes:

```
model/
 ├── MLmodel
 ├── model.pkl
 ├── conda.yaml
 ├── requirements.txt
```

These make each model portable, reproducible, and deployable.



