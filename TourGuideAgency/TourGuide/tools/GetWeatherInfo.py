from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
class GetWeatherInfo(BaseTool):
    """
    use this tool to get weather information for a given location
    """
    latitude: float = Field(..., description="The latitude of the location.")
    longitude: float = Field(..., description="The longitude of the location.")

    def run(self) -> str:
        """
        fetches weather data from open-meteo api using the given location.
        returns the call's result in a str.
        """
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&current_weather=true"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and 'current_weather' in data:
                weather = data['current_weather']['weathercode']
                temperature = data['current_weather']['temperature']
                wind_speed = data['current_weather']['windspeed']
                return (
                    f"The current weather at latitude {self.latitude} and longitude {self.longitude} is: "
                    f"Temperature: {temperature}°C, Weather Code: {weather}, Wind Speed: {wind_speed} m/s."
                )
            else:
                return f"Error fetching weather data: {data.get('reason', 'Unknown error')}"
        except Exception as e:
            return f"An error occurred: {str(e)}"