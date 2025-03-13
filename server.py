from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator, model_validator, ValidationError
from xgboost import XGBRegressor
import numpy as np
import pickle
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load your pre-trained model
try:
    with open('./xgb_model.pkl', 'rb') as f:
        model = pickle.load(f)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise HTTPException(status_code=500, detail="Model loading failed.")

class PredictionRequest(BaseModel):
    """
    PredictionRequest is a Pydantic model that defines the structure of the input data for a prediction request.
    
    Attributes:
        MedInc (float): Median income in the block group. Default is 3.5348.
        HouseAge (float): Median age of the houses in the block group. Default is 29.0.
        AveRooms (float): Average number of rooms per household. Default is 5.229.
        AveBedrms (float): Average number of bedrooms per household. Default is 1.1.
        Population (float): Total population in the block group. Default is 1166.0.
        AveOccup (float): Average number of occupants per household. Default is 2.8181.
        Latitude (float): Latitude of the block group. Default is 34.26.
        Longitude (float): Longitude of the block group. Default is -118.49.

    Methods:
        model_validate(cls, values):
            Ensures at least one feature is provided.
            Sets default values for missing fields.
    """
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values):
        """
        Validates the input fields for the model.
        This method is a class method and is used as a model validator with the "before" mode.
        It ensures that the input data is a valid dictionary and that at least one feature is provided.
        If any required field is missing, it sets the default value from the predefined dataset medians.
        Args:
            cls (type): The class that this method is called on.
            values (dict): The input data to be validated.
        Returns:
            dict: The validated input data with missing fields set to their default values.
        Raises:
            HTTPException: If the input data is not a dictionary or if no features are provided.
        """
        if not isinstance(values, dict):
            raise HTTPException(status_code=400, detail="The input data must be a valid dictionary.")
        
        extra_fields = set(values.keys()).difference(set(cls.model_fields.keys()))
        if extra_fields:
            raise HTTPException(status_code=400, detail=f"Invalid fields provided: {extra_fields}. Allowed fields are: {set(cls.model_fields.keys())}")

        # Check if at least one field is provided
        if not any(values.values()):
            logger.warning("Validation failed: No features provided.")
            raise HTTPException(status_code=400, detail="At least one feature must be provided.")

        # Set median from the dataset as the default for missing fields
        defaults = {
            "MedInc": 3.5348,
            "HouseAge": 29.0,
            "AveRooms": 5.229,
            "AveBedrms": 1.1,
            "Population": 1166.0,
            "AveOccup": 2.8181,
            "Latitude": 34.26,
            "Longitude": -118.49,
        }

        for key, default in defaults.items():
            if key not in values or values[key] is None:
                values[key] = default
        
        logger.info("Validation successful. Missing values set to defaults.")
        return values

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        request = request.model_dump()
        logger.info(f"Received request: {request}")
        
        features = np.array([[request["MedInc"], 
                              request["HouseAge"], 
                              request["AveRooms"], 
                              request["AveBedrms"], 
                              request["Population"], 
                              request["AveOccup"], 
                              request["Latitude"], 
                              request["Longitude"]]])
        
        logger.info(f"Features array: {features}")
        
        prediction = model.predict(features)
        logger.info(f"Prediction: {prediction}.")
        
        return {"predicted_price": prediction.item()*10**5}
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=5500)
        logger.info("Server started successfully.")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        raise