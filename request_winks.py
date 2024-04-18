import requests
import json
import yaml


winks = list(range(9,20))
filename = "config.yaml"
try:
  with open(filename, "r") as file:
    config_data = yaml.safe_load(file)
except FileNotFoundError:
  raise FileNotFoundError(f"Error: YAML file not found: {filename}")

for wink_n in winks:
    # Define the URL and API key
    url = f"https://api.anky.lat/book-data/{wink_n}"  # Replace with the actual URL
    
    # Send the GET request
    response = requests.get(url, headers={"x-api-key": config_data["WINK_API_KEY"]})
    
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
