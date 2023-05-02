#%%
import censusgeocode as cg
import requests
import pandas as pd


def geocode_multi_batch(df, address_col: str, city_col: str, state_col: str, zip_col: str, batch_size: int = 500):
    """
    This function geocodes a list of addresses provided in a DataFrame, in chunks based on the batch_size.

    :param df: DataFrame containing addresses to geocode.
    :param address_col: Name of the column in the input DataFrame containing the street address.
    :param city_col: Name of the column in the input DataFrame containing the city.
    :param state_col: Name of the column in the input DataFrame containing the state.
    :param zip_col: Name of the column in the input DataFrame containing the zip code.
    :param batch_size: The size of each batch for geocoding. Default is 500.
    :return: List of DataFrames containing the original input data and the geocoded results.
    """

    def create_batch(chunk):
        """
        Creates a batch for geocoding by subsetting the relevant columns.

        :param chunk: DataFrame containing a chunk of addresses.
        :return: DataFrame with columns needed for geocoding.
        """
        chunk['id'] = chunk.index
        columns = [address_col, city_col, state_col, zip_col]
        batch_input_df = chunk[columns].reset_index(drop=True)
        batch_input_df.columns = ['street', 'city', 'state', 'zip']
        return batch_input_df

    def process_batch(batch, current_chunk_index):
        """
        Processes the batch by geocoding the addresses and returning the results.

        :param batch: DataFrame containing a batch of addresses.
        :param current_chunk_index: Index of the current chunk being processed.
        :return: DataFrame with the geocoding results.
        """
        batch_filename = f'current_chunk_{current_chunk_index}.csv'
        batch.to_csv(batch_filename, index=True, header=False)
        return pd.DataFrame.from_dict(cg.addressbatch(batch_filename))

    chunks = [df[i:i + batch_size] for i in range(0, len(df), batch_size)]
    output_dfs = []

    for index, chunk in enumerate(chunks):
        batch_input_df = create_batch(chunk)
        batch_output_df = process_batch(batch_input_df, index)
        batch_output_df['id'] = batch_output_df['id'].astype(int)
        output_df = chunk.merge(batch_output_df, on='id')
        output_dfs.append(output_df)

    return pd.concat(output_dfs, axis=0, ignore_index=True)

def fetch_geocode_address(full_address=None, street=None, city=None, state=None):
    if street and city and state:
        full_address = f'{street}, {city}, {state}'
    try:
        return cg.onelineaddress(full_address)[0]
    except IndexError:
        return None

def fetch_geocode_coordinates(lat, lng):
    return cg.coordinates(lng, lat)

def extract_data(data, main_key, sub_keys):
    return {key: data[main_key][0][key] for key in sub_keys}

def build_geographical_dict(data):
    data_dict = extract_data(data, "States", ["STATE", "BASENAME"])
    data_dict.update(extract_data(data, "Incorporated Places", ["NAME"]))
    data_dict.update(extract_data(data, "2020 Census Blocks", ["BLOCK", "CENTLAT", "CENTLON", "AREALAND"]))
    data_dict.update(extract_data(data, "Census Tracts", ["BASENAME"]))
    data_dict["BLOCK_CENTER"] = (float(data_dict["CENTLAT"][1:]), float(data_dict["CENTLON"]))
    return data_dict

def build_address_dict(cdata):
    if not cdata:
        return {'error': 'data parameter is empty'}
    
    address_components_raw = cdata['addressComponents']
    address_components = {'fullAddress': cdata['matchedAddress']}
    cdata_keys = [ "fromAddress", "toAddress", "preType", "preDirection", "streetName", "suffixType", "suffixDirection", "suffixQualifier", "city", "state", "zip"]
    address_components.update({key: address_components_raw[key] for key in cdata_keys})
    return address_components

def fetch_google_api_data(lat, lng, api_key):
    API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    coordinates = f"{lat},{lng}"
    params = {
        "latlng": coordinates,
        "key": api_key
    }
    response = requests.get(API_URL, params=params)
    return response.json()


def estimate_address_from_coordinates(lat, lng, GOOGLE_MAPS_API_KEY):
    api_data = fetch_google_api_data(lat, lng, GOOGLE_MAPS_API_KEY)
    return api_data['results'][0]['formatted_address'] if api_data["status"] == "OK" else {'error': 'Failed to find an address for the given coordinates'}
    



'''
def address_geocoder(full_address=None, street=None, city=None, state=None):
    if street and city and state:
        full_address = f'{street}, {city}, {state}'
    try:
        return cg.onelineaddress(full_address)[0]
    except IndexError:
        return None

def coordinates_geocoder(lat, lng):
    result = cg.coordinates(lng, lat)
    return result

def parse_geographical_component(data):
    if not data:
        return {'error': 'data parameter is empty'}
    states = data['States'][0]
    state, basename = states['STATE'], states['BASENAME']
    name = data['Incorporated Places'][0]['NAME']
    census_blocks = data['2020 Census Blocks'][0]
    blocks, cent_lat, cent_lng, arealand = census_blocks['BLOCK'], census_blocks['CENTLAT'], census_blocks['CENTLON'], census_blocks['AREALAND']
    tract = data['Census Tracts'][0]['BASENAME']

    return {
        'NAME': name,
        'PARENT': basename,
        'STATEID': state,
        'BLOCK': blocks,
        'BLOCK_CENTER': (float(cent_lat[1:]), float(cent_lng)),
        'BLOCK_AREALAND': arealand,
        'TRACT': tract, 
    }

def parse_address_component(cdata):
    if not cdata:
        return {'error': 'data parameter is empty'}
    
    address_components_raw = cdata['addressComponents']

    return {
        'fullAddress': cdata['matchedAddress'],
        'streetStartAddress': address_components_raw['fromAddress'],
        'streetEndAddress': address_components_raw['toAddress'],
        'preType': address_components_raw['preType'],
        'preDirection': address_components_raw['preDirection'],
        'streetName': address_components_raw['streetName'],
        'suffixType': address_components_raw['suffixType'],
        'suffixDirection': address_components_raw['suffixDirection'],
        'suffixQualifier': address_components_raw['suffixQualifier'],
        'city': address_components_raw['city'],
        'state': address_components_raw['state'],
        'zipcode': address_components_raw['zip'],
    }
    
def get_address_from_coordinates(lat, lng, GOOGLE_MAPS_API_KEY):
    API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    coordinates = f"{lat},{lng}"
    params = {
        "latlng": coordinates,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    if data["status"] == "OK":
        return data['results'][0]['formatted_address']
    else:
        return {'error': 'Failed to find an address for the given coordinates'}



'''

#%%
'''
# Example usage
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
lat, lon = 40.73659, -73.99563
lat2, lon2 = 39.12518, -77.76760
address = get_address_from_coordinates(lat, lon, GOOGLE_MAPS_API_KEY)
address2 = get_address_from_coordinates(lat2, lon2, GOOGLE_MAPS_API_KEY)
print(address)


'''

# %%
