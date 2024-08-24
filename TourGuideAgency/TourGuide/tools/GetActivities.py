import os

from agency_swarm.tools import BaseTool
from pydantic import Field
import requests


class GetActivities(BaseTool):
    """
    Use this tool to get activities. the supported arguments are used to refine and make the search more accurate.
    """
    latitude: float = Field(..., description="The latitude of the location.")
    longitude: float = Field(..., description="The longitude of the location.")
    query: str = Field(..., description="Search term to match places to specific activities or categories.")
    radius: int = Field(1000, description="The radius (in meters) within which to search for activities.")
    categories: str = Field(..., description="Comma-separated list of category IDs that match the user query context,"
                                             " based on the fsq-categories file. You can enter multiple categories if needed.")
    limit: int = Field(10, description="The maximum number of results to return.")
    sort: str = Field("distance",
                      description="Sort order of results. Possible values: 'distance', 'relevance', 'popularity'.")
    open_now: bool = Field(True, description="Filter for places that are currently open.")
    min_price: int = Field(None,
                           description="Minimum price level to filter results (1 = inexpensive, 4 = very expensive).")
    max_price: int = Field(None,
                           description="Maximum price level to filter results (1 = inexpensive, 4 = very expensive).")
    def run(self) -> dict:
        """
        fetches activities from the foursqaure api using the given parameters.
        returns the call's result in a dict.
        """
        try:
            url = "https://api.foursquare.com/v3/places/search"
            params = {
                "ll": f"{self.latitude},{self.longitude}",
                "query": self.query,
                "radius": self.radius,
                "categories": self.categories,
                "limit": self.limit,
                "sort": self.sort,
                "open_now": str(self.open_now).lower(),
                "min_price": self.min_price,
                "max_price": self.max_price,
                "fields": "name,location,distance,categories,rating,price,popularity,description,website,hours"
            }
            headers = {
                "Accept": "application/json",
                "Authorization": os.getenv('FOURSQAURE_API_KEY'),
            }
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            if response.status_code == 200 and 'results' in data:
                activities = []
                for place in data['results']:
                    print(place)
                    name = place.get('name', 'Unknown Place')
                    location = place.get('location', {})
                    address = location.get('address', 'Address not available')
                    distance = place.get('distance', 'Distance not available')
                    categories = ', '.join([cat['name'] for cat in place.get('categories', [])])
                    rating = place.get('rating', 'No rating')
                    price = place.get('price', 'No price info')
                    popularity = place.get('popularity', 'No popularity info')
                    description = place.get('description', 'No description available')
                    website = place.get('website', 'No website available')
                    hours = place.get('hours', 'Hours not available')
                    verified = place.get('verified', False)

                    activities.append({
                        "name": name,
                        "address": address,
                        "distance": distance,
                        "categories": categories,
                        "rating": rating,
                        "price": price,
                        "popularity": popularity,
                        "description": description,
                        "url": url,
                        "website": website,
                        "hours": hours,
                        "verified": verified,
                    })

                return {'activities': activities}
            else:
                return {"error": data.get('reason', 'Unknown error')}
        except Exception as e:
            return {"error": str(e)}
