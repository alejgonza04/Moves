import pandas as pd
import numpy as np
import random
import joblib
import lightgbm as lgb
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity
from math import radians, cos, sin, asin, sqrt

shopping_types = [
  "clothing_store", "shoe_store", "electronics_store",
  "jewelry_store", "book_store", "convenience_store", "department_store",
  "home_goods_store", "pet_store", "shopping_mall", "store"
]


mood_type_map = {
    "shopping": shopping_types,
    "coffee" : ["cafe", "bakery"],
    "party" : ["night_club", "bar", "liquor_store"],
    "food": ["restaurant", "meal_takeaway", "meal_delivery"],
    "workout" : ["gym", "health", "spa"],
    "adventurous": ["amusement_park", "aquarium", "zoo", "park", "tourist_attraction", "campground"],
    "artsy": ["art_gallery", "museum", "movie_theater"],
    "academic": ["library", "university", "book_store"]
}

#businesses, cv, similarity = joblib.load("recommender_model.joblib")
#cv = cv.transform(businesses["tags"]).toarray()
_, cv, _ = joblib.load("recommender_model.joblib")

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
        "query": f"{name} {city}",
        "key": GOOGLE_PLACES_API_KEY,
    }

    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    return results[0] if results else None

def fetch_similar_google_places(city: str, category_keywords: str):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": f"{category_keywords} in {city}", "key": GOOGLE_PLACES_API_KEY}
    response = requests.get(url, params=params)
    return response.json().get("results", [])

def build_google_tag(business: dict) -> str:
    name = business.get("name", "")
    city = business.get("formatted_address", "").split(",")[-3].strip() if ","  in business.get("formatted_address", "") else ""
    categories = " ".join(business.get("types", []))
    return f"{name} {categories} {city}"

# calculate longitude and lattitude
def haversine_distance(lat1, lon1, lat2, lon2):
  R = 6371  # Radius of the Earth in kilometer
  lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
  dlat = lat2 - lat1
  dlon = lon2 - lon1
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  return R * 2 * asin(sqrt(a))

def get_city_from_coordinates(lattitude: float, longitude: float) -> str:
  url = "https://maps.googleapis.com/maps/api/geocode/json"
  params = {
      "latlng": f"{lattitude},{longitude}",
      "key": GOOGLE_PLACES_API_KEY,
  }
  response = requests.get(url, params=params)
  results = response.json().get("results", [])
  if not results:
    return ""

  for component in results[0].get("address_components", []):
    if "locality" in component.get("types", []):
        return component.get("long_name")
  return ""
 
def fetch_location_and_mood_from_flask():
  url = "http://localhost:5555/locationmood"
  try:
    response = requests.post(url, json={})
    if response.status_code == 200:
      data = response.json()
      print(data)
      return data
    else:
      print("Error contacting Flask service:", response.text)
      return None
  except Exception as e:
    print("Exception fetching location/mood:", e)
    return None
  
@app.get("/recommend/")
def get_recommendations(user_mood: str = None, latitude: float = None, longitude: float = None, rating_threshold: float = 3.0):
   # get base business from user
    if latitude is None or longitude is None:
      location_data = fetch_location_and_mood_from_flask()
      if location_data:
        latitude = location_data.get("latitude")
        longitude = location_data.get("longitude")
        user_mood = user_mood or location_data.get("mood")
    
    print(f"User location: ({latitude}, {longitude}), mood: {user_mood}")

    city = get_city_from_coordinates(latitude, longitude)
    mood_types = mood_type_map.get(user_mood.lower())

    all_businesses = []
    for place_type in mood_types:
       all_businesses += fetch_similar_google_places(city, place_type)  
    
    
    '''if not base:
        return JSONResponse(status_code=404, content={"error": "Business not found"})

    base_tag = build_google_tag(base)
    base_vector = cv.transform([base_tag]).toarray()

    # find other businesses with similar tags
    category_keywords = " ".join(base.get("types", []))
    nearby = fetch_similar_google_places(city, category_keywords)
    if not nearby:
        return JSONResponse(status_code=404, content={"error": "No similar businesses found"})

    # tag and vectorize the nearby businesses'''
    tagged = []
    for business in all_businesses:
        rating = business.get("rating", 0)
        if rating >= rating_threshold:
            tag = build_google_tag(business)
            tagged.append((business, tag))

    if not tagged:
        return JSONResponse(status_code=200, content={"recommendations": []})

    tags = [tag for _, tag in tagged]
    tag_vectors = cv.transform(tags).toarray()

    # calculate similarity
    #scores = cosine_similarity(base_vector, tag_vectors)[0]
    #ranked = sorted(zip(tagged, scores), key=lambda x: x[1], reverse=True)

    # generate fake base vvector for similarity since we won't sort by it primarily
    dummy_vector = np.zeros_like(tag_vectors[0])
    scores = cosine_similarity([dummy_vector], tag_vectors)[0]

    combined = []
    for((business, tag), sim_score) in zip(tagged, scores):
      business_lat = business.get("geometry", {}).get("location", {}).get("lat")
      business_lon = business.get("geometry", {}).get("location", {}).get("lng")
      if latitude is not None and longitude is not None and business_lat is not None and business_lon:
        distance_miles = haversine_distance(latitude, longitude, business_lat, business_lon) * 0.621371
      else:
        distance_miles = float('inf')  # deprioritize if no location data

      combined.append((business, sim_score, distance_miles))
    
    # within 30 mile filter
    close_options = [item for item in combined if item[2] <= 30]

    # return the results
    #ranked = sorted(combined, key=lambda x: (x[2], -x[1]))
    #close_options = [b for b in combined if b[2] <= 30]

    # choose one randomly from the top N cloesest, for ex top 5
    close_options.sort(key=lambda x: x[2])
    
    top_nearby = close_options[:5]

    recommendations = []
    for (business, sim_score, distance_miles) in top_nearby:
      # set photo_url to none
      photo_url = None

      if "photos" in business and business["photos"]:
        photo_reference = business["photos"][0].get("photo_reference")
        if photo_reference:
          photo_url = (
              f"https://maps.googleapis.com/maps/api/place/photo"
                f"?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
          )

        recommendations.append({
            "name": business.get("name"),
            "rating": business.get("rating"),
            "address": business.get("formatted_address"),
            "categories": ", ".join(business.get("types", [])),
            "distance_miles": round(distance_miles, 2),
            "image": photo_url
            #"score": round(score, 3)
        })

    #print(f"User: ({latitude}, {longitude}), Business: ({business_lat}, {business_lon})")
    return JSONResponse(content={"recommendations": recommendations})
