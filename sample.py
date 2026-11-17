import groq
import os
import httpx
import json





# export XWEATHER_CLIENT_ID="your_client_id"
# export XWEATHER_CLIENT_SECRET="your_client_secret"



class agentic_weather:

    def get_weather(self,city:str) -> int:

        api_key = os.getenv("ACCUWEATHER_API_KEY")
        

        if not api_key:
            raise ValueError("AccuWeather API key not found")

        headers = {
            "Authorization": f"Bearer {api_key}"
        }


          # Find city Location Key
        location_url = (
            "https://dataservice.accuweather.com/"
            "locations/v1/cities/search"
        )
        
        params = {
        "q": city,
        "appid": api_key  # Parameter name varies by API (e.g., api_key, key, token)
        }

        response = httpx.get(
        location_url,
        headers=headers,
        params={"q":city},  # URL query parameters
        timeout=60.0,
        )

        response.raise_for_status()

        data = response.json()

        location_key = data[0]["Key"]

        weather_url = (
            f"https://dataservice.accuweather.com/"
            f"currentconditions/v1/{location_key}"
        )

        weather_response = httpx.get(
        weather_url,
        headers=headers,
        params={"q":city},  # URL query parameters
        timeout=60.0,
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

       
        return float(weather_data[0]["Temperature"]["Metric"]["Value"])


    def suggest_activity(self, temperature:int) -> str:

        if temperature < 10 and temperature >0:
            return print("Time to have a good Workout")

        elif temperature <0:
           return print("Stay at home")

        else:
           return print("Time for walk")

       
        

   
            

       






