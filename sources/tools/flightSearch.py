import os
import requests
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    from tools import Tools
else:
    from sources.tools.tools import Tools

class FlightSearch(Tools):
    def __init__(self, api_key: str = None):
        """
        A tool to search for flight information using a flight number via AviationStack API.
        """
        super().__init__()
        self.tag = "flight_search"
        self.api_key = None
        self.api_key = api_key or os.getenv("AVIATIONSTACK_API_KEY")

    def execute(self, blocks: str, safety: bool = True) -> str:
        if self.api_key is None:
            return "Error: No AviationStack API key provided."
        
        for block in blocks:
            flight_number = block.strip()
            if not flight_number:
                return "Error: No flight number provided."

            try:
                url = "http://api.aviationstack.com/v1/flights"
                params = {
                    "access_key": self.api_key,
                    "flight_iata": flight_number,
                    "limit": 1
                }
                response = requests.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    flight = data["data"][0]
                    # Extract key flight information
                    flight_status = flight.get("flight_status", "Unknown")
                    departure = flight.get("departure", {})
                    arrival = flight.get("arrival", {})
                    airline = flight.get("airline", {}).get("name", "Unknown")
                    
                    departure_airport = departure.get("airport", "Unknown")
                    departure_time = departure.get("scheduled", "Unknown")
                    arrival_airport = arrival.get("airport", "Unknown")
                    arrival_time = arrival.get("scheduled", "Unknown")

                    return (
                        f"Flight: {flight_number}\n"
                        f"Airline: {airline}\n"
                        f"Status: {flight_status}\n"
                        f"Departure: {departure_airport} at {departure_time}\n"
                        f"Arrival: {arrival_airport} at {arrival_time}"
                    )
                else:
                    return f"No flight information found for {flight_number}"
            except requests.RequestException as e:
                return f"Error during flight search: {str(e)}"
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        return "No flight search performed"

    def execution_failure_check(self, output: str) -> bool:
        return output.startswith("Error") or "No flight information found" in output

    def interpreter_feedback(self, output: str) -> str:
        if self.execution_failure_check(output):
            return f"Flight search failed: {output}"
        return f"Flight information:\n{output}"


if __name__ == "__main__":
    flight_tool = FlightSearch()
    flight_number = "AA123"
    result = flight_tool.execute([flight_number], safety=True)
    feedback = flight_tool.interpreter_feedback(result)
    print(feedback)