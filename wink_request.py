import requests
import json

winks = [8]

api_key = ""

# Create a dictionary for the header
headers = {"x-api-key": api_key}

for wink_n in winks:
    # Define the URL and API key
    url = f"https://server-s3.onrender.com/get-writings-by-wink/{wink_n}"  # Replace with the actual URL
    
    # Send the GET request
    response = requests.get(url, headers=headers)
    
    # Check for successful response
    if response.status_code == 200:
      # Process the response content
      data = response.json()  # Assuming JSON response, adjust parsing based on response format
      print(f"Successful request wink {wink_n}")
      with open(f"winks/wink_{wink_n}.json", "w") as f:
        json.dump(data, f)
    else:
      # Handle error codes
      print(f"Error: {response.status_code}")
