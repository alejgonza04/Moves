import pandas as pd
import numpy as np
import joblib
import lightgbm as lgb
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity

businesses, cv, similarity = joblib.load("recommender_model.joblib")
vector = cv.transform(businesses["tags"]).toarray()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_PLACES_API_KEY = "AIzaSyBUMS7_7cs7rjijPp4LMcP6eXj8VwPi7CQ"
def fetch_google_business(name: str, city: str) -> dict:
    query = f"{name} {city}"

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": query,
        "key": GOOGLE_PLACES_API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Google Places API error")
    
    results = response.json().get("results", [])
    
    if not results:
        raise Exception("Business not found on Google")
    
    return results[0]  # Take top match

def build_google_tag(business: dict) -> str:
    name = business.get("name", "")
    city = business.get("formatted_address", "").split(",")[-3].strip() if ","  in business.get("formatted_address", "") else ""
    categories = " ".join(business.get("types", []))

    tag = f"{name} {categories} {city}"

    return tag

@app.get("/recommend/")
def get_recommendations(business_name: str, city: str = None, rating_threshold: float = 3.0):
  use_custom_vector = False
  try:
    index = businesses[businesses['name'] == business_name].index[0]
    tag_vector = vector[index].reshape(1, -1)
  except IndexError:
      try:
          google_business = fetch_google_business(business_name, city)
          tag = build_google_tag(google_business)
          tag_vector = cv.transform([tag]).toarray()
          use_custom_vector = True
      except Exception as e: 
        return JSONResponse(content={"error": str(e)}, status_code=400)      
      
  if use_custom_vector:
      similarity_scores = cosine_similarity(tag_vector, vector)[0]
      distance = list(enumerate(similarity_scores))
  else:
      distance = list(enumerate(similarity[index]))   

  
  # calculate similarity
 
  # sort similarity from highest to lowest
  distance = sorted(distance, reverse=True, key=lambda x: x[1])
  # count = 0
  seen = set()
  recommendations = []
  for i in distance:
    business = businesses.iloc[i[0]]
    business_id = i[0]

    if business['name'] == business_name:
      continue

    if city and business['city'].lower() != city.lower():
            continue

    # if it does not meet threshold, skip
    if business['stars'] < rating_threshold:
      # print(f"{business['name']} (Rating: {business['stars']}), (Category: {business['categories']}), (City: {business['city']})\n")
      # count += 1
      continue

    # if business was already swiped on, skip it
    if business_id in seen:
            continue

    #if count == 5:
      #break

    seen.add(business_id )

    recommendations.append({ 
        "name": business['name'],
        "rating": business['stars'],
        "category": business['categories'],
        "city": business['city']
    })

    if len(recommendations) >= 5:
        break

  return JSONResponse(content={"recommendations": recommendations})