# Census Geocoder API Wrapper

A simple Python library that integrates with the Census Geocoder API and Google Maps Geocoding API. This library provides functions for fetching geocode data from an address and coordinates, estimating an address from coordinates, and other useful utilities.

## Getting Started

### Dependencies

Ensure the following module is installed:
* `censusgeocode`
* `requests`

You will also require a Google Maps Geocoding API key

### Functions

Below are the provided functions in the library:

1. `fetch_geocode_address(full_address=None, street=None, city=None, state=None)`
Fetches the geocode data from the Census Geocoder for a given address.

2. `fetch_geocode_coordinates(lat, lng)`
Fetches the geocode data for given coordinates from the Census Geocoder.

3. `extract_data(data, main_key, sub_keys)`
Extracts specific keys from the provided data.

4. `build_geographical_dict(data)`
Builds a dictionary containing geographical data from the Census Geocoder response.

5. `build_address_dict(cdata)`
Builds a dictionary containing address components from the Census Geocoder response.

6. `fetch_google_api_data(lat, lng, api_key)`
Fetches data from the Google Maps Geocoding API for a given set of coordinates.

7. `estimate_address_from_coordinates(lat, lng, GOOGLE_MAPS_API_KEY)`
Estimates an address based on given coordinates using the Google Maps Geocoding API.


## Examples

```python
import CensusAPI_Wrapper

address_result = CensusAPI_Wrapper.fetch_geocode_address("1600 Pennsylvania Ave NW, Washington, DC")
coordinates_result = CensusAPI_Wrapper.fetch_geocode_coordinates(38.89511, -77.03637)
estimated_address = CensusAPI_Wrapper.estimate_address_from_coordinates(38.89511, -77.03637, "YOUR_GOOGLE_MAPS_API_KEY")
