import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.title(" Classifier")


#  Upload CSV

uploaded_file = st.file_uploader("Upload Classification Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader(" Original Dataset Preview")
    st.dataframe(df)


    # 2) Check Zeros & Nulls

    st.subheader(" Data Quality Report")

    zero_counts = (df == 0).sum()
    null_counts = df.isnull().sum()

    st.write("**Zero Counts:**")
    st.write(zero_counts)

    st.write("**Null Counts:**")
    st.write(null_counts)

    # Drop null rows
    df = df.dropna()


    # 3) Outlier Detection (IQR)

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    outlier_count = 0

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count += mask.sum()

    st.write(f"**Outlier Count (IQR method): {outlier_count}**")

    # Remove outliers
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]


    # 4) Dataset Summary

    st.subheader(" Cleaned Dataset Summary")

    st.write(f"**Shape:** {df.shape}")
    st.write("**Columns:**", list(df.columns))


    # 5) Select Target Column

    st.subheader(" Select Target Column")
    target = st.selectbox("Target Column", df.columns)


    # 6) Train Classifier

    if st.button("Train Classifier"):
        X = df.drop(columns=[target])
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LogisticRegression(max_iter=500)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        st.success(f" Model trained! Accuracy: **{acc:.2f}**")

        st.session_state["model"] = model
        st.session_state["features"] = list(X.columns)


    # 7) Make Predictions

    if "model" in st.session_state:
        st.subheader(" Make a Prediction")

        input_values = {}
        for feature in st.session_state["features"]:
            val = st.number_input(f"{feature}", value=float(df[feature].mean()))
            input_values[feature] = val

        if st.button("Predict"):
            values = np.array(list(input_values.values())).reshape(1, -1)
            pred = st.session_state["model"].predict(values)[0]
            st.success(f" Prediction: **{pred}**")
