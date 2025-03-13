"use client";

import { useState } from "react";
import Image from "next/image";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function PricePrediction() {
  const [features, setFeatures] = useState({
    MedInc: 3.5348,
    HouseAge: 29.0,
    AveRooms: 5,
    AveBedrms: 1,
    Population: 1425.0,
    AveOccup: 3,
    Latitude: 35.63,
    Longitude: -119.57,
  });
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  interface Features {
    MedInc: number;
    HouseAge: number;
    AveRooms: number;
    AveBedrms: number;
    Population: number;
    AveOccup: number;
    Latitude: number;
    Longitude: number;
  }

  const featureLabels: { [key in keyof Features]: string } = {
    MedInc: "Median Income (in multiples of $100K)",
    HouseAge: "House Age (in years)",
    AveRooms: "Number of Rooms",
    AveBedrms: "Number of Bedrooms",
    Population: "Population",
    AveOccup: "Size of Household",
    Latitude: "Latitude",
    Longitude: "Longitude",
  };

  interface PredictionResponse {
    predicted_price: number;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(`Changing ${e.target.name} to ${e.target.value}`);
    setFeatures({ ...features, [e.target.name]: parseFloat(e.target.value) });
  };

  const handleSubmit = async () => {
    console.log("Submitting features:", features);
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("https://california-housing-price-prediction-04in.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(features),
      });
      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }
      const data: PredictionResponse = await response.json();
      console.log("Received prediction:", data.predicted_price);
      setPrediction(data.predicted_price);
    } catch (err) {
      console.error("Error fetching prediction:", err);
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
        {/* Page Title */}
        <title>California Housing Price Prediction</title>

        <div className="flex justify-center items-center h-screen bg-gray-100">
          {/* Write-up Section */}
        <div className="max-w-2xl text-left mb-6 px-4">
          <p className="text-lg font-semibold">
            The <span className="text-blue-600">California Housing Price Prediction</span> tool helps estimate property values based on key factors like 
            <strong> median income, house age, average rooms, population density, and location coordinates.</strong>
          </p>
          <p className="mt-2 text-gray-700">
            Using advanced machine learning models, this tool analyzes patterns in <strong>housing data</strong> to provide accurate price predictions. Whether you're a 
            <span className="text-blue-600"> homebuyer, investor, or real estate analyst</span>, this tool offers valuable insights into property valuation trends in California.
          </p>
          <p className="mt-2 font-medium mb-4">
            Simply enter the required details, and get an <span className="text-green-600">instant price prediction</span> for any home in California! 🏡
          </p>

          {/* Image below the writeup */}
          <Image src="/california-house-price-trends.png" alt="Housing Image" width={600} height={800} className="rounded-xl shadow-lg" />
        </div>
        
        {/* Prediction Card */}
        <Card className="p-6 w-[600px] bg-white shadow-lg rounded-xl mt-[-85px]">
          <CardContent>
            {Object.keys(features).map((key) => (
              <div key={key} className="mb-2">
              <label className="block text-sm font-medium">{featureLabels[key as keyof Features]}</label>
              <Input
                type="number"
                name={key}
                value={features[key as keyof Features]}
                onChange={handleChange}
                className="w-full border rounded p-2"
              />
              </div>
            ))}
            <Button onClick={handleSubmit} className="w-full mt-4" disabled={loading}>
              {loading ? "Predicting..." : "Predict"}
            </Button>
            {error && <p className="mt-4 text-red-500">{error}</p>}
            {prediction !== null && (
              <p className="mt-4 text-lg font-semibold">Prediction: $ {prediction.toFixed(2)}</p>
            )}
          </CardContent>
        </Card>
      </div>
    </>
  );
}
