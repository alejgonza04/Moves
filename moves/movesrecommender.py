import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

business = pd.read_json('moves\yelp_academic_dataset_business.json', lines=True)

# filter dataset and only keep open businesses with a 3.0 or higher rating
# only have category information  that is not null
businesses = business[
    (business['is_open'] == 1) &
    (business['stars'] >= 3.0) &
    (business['categories'].notna())
]

# limit to first 5,000 entries since original dataset is HUGE
businesses = businesses.head(5000).reset_index(drop=True)

# filtered = filtered[['name', 'stars', 'categories', 'city', 'latitude', 'longitude']]

businesses = businesses[['name', 'stars', 'categories', 'city']]

# print(businesses.head())

# print(businesses['name'].sample(10).tolist())

# creates tags that combines cols into a single string for comparing similarity
businesses['tags'] = businesses['name'] + " " + businesses['categories'] + " " + businesses['city']

# convert tags into numerical vectors and remove stopwords
cv = CountVectorizer(max_features=10000, stop_words='english')

vector = cv.fit_transform(businesses['tags'].values.astype('U')).toarray()

# calculate similarity using tag vectors
similarity = cosine_similarity(vector)

def recommend(business_name, city=None, rating_threshold = 3.0):
  index = businesses[businesses['name'] == business_name].index[0]
  
  # calculate similarity
  distance = list(enumerate(similarity[index]))
 
  # sort similarity from highest to lowest
  distance = sorted(distance, reverse=True, key=lambda x: x[1])
  print(f"Top recommendations similar to {business_name}")

  # count = 0
  seen = set()
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

    # matching mechanic
    print(f"How is this place?")
    print(f"{business['name']} (Rating: {business['stars']}), (Category: {business['categories']}), (City: {business['city']})\n")
    swipe = input("Enter 1 for Right, 0 for Left: ")

    if swipe == "1":
      print("Matched!")
      return
    seen.add(business_id)

recommend('Biscuits Cafe', city='Tampa')

joblib.dump((businesses, cv, similarity), 'recommender_model.joblib', compress=3)

with open("movierecommender.pkl", "wb") as f:
    pickle.dump((businesses, cv, similarity), f)
