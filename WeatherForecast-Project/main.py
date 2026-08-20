import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ==================== HELPER FUNCTION ====================

def ask_again(prompt):
    while True:
        answer = input(prompt).lower().strip()

        if answer in ("yes", "no"):
            return answer

        print("Please enter yes or no.")


# ==================== COORDINATES ====================

def coordinates_finder():
    while True:
        city_name = input("Enter city name: ").strip()

        while not city_name or not all(
            char.isalpha() or char.isspace()
            for char in city_name
        ):
            print("Please enter a valid city name.")
            city_name = input("Enter city name: ").strip()

        country_code = input(
            "Enter country code (e.g. PK, US, GB): "
        ).strip().upper()

        while len(country_code) != 2 or not country_code.isalpha():
            print("Please enter a valid 2-letter country code.")
            country_code = input(
                "Enter country code (e.g. PK, US, GB): "
            ).strip().upper()

        coordinates = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={city_name},{country_code}&appid={API_KEY}"
        )

        try:
            response = requests.get(coordinates, timeout=10)

        except requests.exceptions.RequestException:
            print("There was a problem connecting to the server.")
            continue

        if response.status_code != 200:
            print("The server returned an error.")
            continue

        data = response.json()

        if not data:
            print("Sorry, we couldn't find that city.")
            continue

        lat = data[0]["lat"]
        lon = data[0]["lon"]

        return lat, lon


# ==================== WEATHER FORECAST ====================

def weather_forecast():
    while True:
        lat, lon = coordinates_finder()

        weather = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        try:
            response = requests.get(weather, timeout=10)

        except requests.exceptions.RequestException:
            print("There was a problem connecting to the server.")
            continue

        if response.status_code != 200:
            print("The server returned an error.")
            continue

        data = response.json()

        weather_details = {
            "City": data["name"],
            "Country": data["sys"]["country"],
            "Temp": data["main"]["temp"],
            "Feels_Like": data["main"]["feels_like"],
            "Min_Temp": data["main"]["temp_min"],
            "Max_Temp": data["main"]["temp_max"],
            "Condition": data["weather"][0]["main"],
            "Description": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Wind_Speed": data["wind"]["speed"],
            "Pressure": data["main"]["pressure"]
        }

        show_weather(weather_details)

        print("\n")

        if ask_again(
            "Do you want to see another weather forecast?: "
        ) != "yes":
            print("Thank you for using Weather Forecast")
            break


# ==================== DISPLAY WEATHER ====================

def show_weather(weather_details):
    print("=" * 50)
    print("Weather Information".center(50))
    print("=" * 50)

    print("\n" + "Location".center(50))
    print("-" * 50)
    print(f"City: {weather_details['City']}")
    print(f"Country: {weather_details['Country']}")

    print("\n" + "Weather".center(50))
    print("-" * 50)
    print(f"Temperature: {weather_details['Temp']}°C")
    print(f"Feels Like: {weather_details['Feels_Like']}°C")
    print(f"Minimum Temperature: {weather_details['Min_Temp']}°C")
    print(f"Maximum Temperature: {weather_details['Max_Temp']}°C")

    print("\n" + "Conditions".center(50))
    print("-" * 50)
    print(f"Condition: {weather_details['Condition']}")
    print(f"Description: {weather_details['Description']}")
    print(f"Humidity: {weather_details['Humidity']}%")
    print(f"Wind Speed: {weather_details['Wind_Speed']} m/s")
    print(f"Pressure: {weather_details['Pressure']} hPa")

    print("=" * 50)


# ==================== MAIN PROGRAM ====================

def main():
    print("=" * 50)
    print("Welcome to Weather Forecast".center(50))
    print("=" * 50)

    weather_forecast()


if __name__ == "__main__":
    main()