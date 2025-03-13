# California Housing Price Prediction

## Objective
The goal of this project is to preprocess data, train and evaluate machine learning models, deploy a simple model as an API, and follow basic MLOps practices.

## Task
### Build and Deploy a Machine Learning Model for Predicting House Prices
- **Dataset:** The California Housing Dataset from Scikit-learn was used for this.

## Data Preprocessing and Feature Engineering
To build an accurate predictive model for California housing prices, the following steps were taken in data preprocessing and feature engineering:

### Data Cleaning
- No missing values were found in the dataset.
- All features were numerical, so no categorical encoding was needed.

### Feature Selection
- **Median income** was identified as a key feature, though it appears to be pre-processed.
- **Housing median age and median house value** were capped. Districts with capped values were removed to ensure the model learns beyond the $500,000 limit.

### Feature Engineering
- Created `bedrooms_per_room`, which showed a stronger correlation with house prices than raw bedroom or room counts.
- Used `rooms_per_household` to provide more valuable insights.

### Scaling and Normalization
- Standardized numerical features using `StandardScaler` to improve model performance.

### Data Splitting
- Used **stratified train-test splitting** based on median income to ensure fair representation of income groups.

## Model Selection and Optimization
The model selection and optimization process involved multiple machine learning models:

### Linear Regression
- **Final Performance Metrics:**
  - RMSE: 0.5805
  - MAE: 0.4269
  - R² Score: 0.6322
- The model struggled with non-linear relationships in the data.

### Random Forest Regressor
- **Grid Search Hyperparameter Tuning:** Tuned `n_estimators`, `max_features`, and `bootstrap`.
- **Final Performance Metrics:**
  - RMSE: 0.4394
  - MAE: 0.2964
  - R² Score: 0.7893
- Showed significant improvement over linear regression, capturing non-linear relationships better.

### XGBoost Regressor
- **Hyperparameter Tuning:** Tuned `n_estimators`, `max_depth`, `learning_rate`, `subsample`, `colsample_bytree`, `reg_lambda`, and `reg_alpha`.
- **Final Performance Metrics:**
  - RMSE: 0.4062
  - MAE: 0.2750
  - R² Score: 0.8199
- Outperformed both Linear Regression and Random Forest, effectively handling complex relationships in the data.

## Deployment Strategy and API Usage Guide
The trained model was deployed as a **REST API** using **FastAPI, Docker, and Render.com**.

### Deployment Steps:
1. **Model Serialization:** Saved the trained model as a pickle file.
2. **FastAPI Setup:** Created an API endpoint for predictions.
3. **Dockerization:** Packaged the API in a Docker container for consistency across environments.
4. **Hosting on Render.com:** Deployed the containerized API on Render.com for public access.
5. **Testing:** Used Postman and cURL to test API endpoints before production release.

### API Endpoint
- **Backend API:** [https://california-housing-price-prediction-04in.onrender.com/predict](https://california-housing-price-prediction-04in.onrender.com/predict)

## Frontend Integration
A sample frontend was built using **Next.js, Docker, and Render.com** to provide a user-friendly interface for interacting with the API.

### Frontend Features
- Users input housing attributes.
- Sends a request to the FastAPI backend for predictions.
- Displays predicted housing prices dynamically.

### Hosting
The frontend is deployed on Render.com alongside the backend for a seamless experience.

- **Frontend URL:** [https://california-housing-price-prediction-u4rm.onrender.com/](https://california-housing-price-prediction-u4rm.onrender.com/)
