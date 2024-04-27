import requests

# Replace with your Tanzania city (e.g., Dar es Salaam)
city_name = "London"
api_key = "52afd2a44f544e4e9ed200555242604"
base_url = "https://api.openweathermap.com/v1/current.json"

# Build the API request URL with city name and API key
url = "http://api.weatherapi.com/v1/current.json?key=52afd2a44f544e4e9ed200555242604&q=London&aqi=no"


try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    # Handle JSON response (assuming OpenWeatherMap)
    data = response.json()

    print(data)
except requests.exceptions.RequestException as e:
    print("Error:", e)