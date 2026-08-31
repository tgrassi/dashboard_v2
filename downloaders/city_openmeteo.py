import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from downloaders.commons import DATA_FOLDER
import time

def download():

    end_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    start_date = "1940-08-15"

    cities = {
        "Milano": {
            "latitude": 45.4643,
            "longitude": 9.1895,
        },
        "Roma": {
            "latitude": 41.8919,
            "longitude": 12.5113,
        },
        "Napoli": {
            "latitude": 40.8522,
            "longitude": 14.2681,
        },
        "Palermo": {
            "latitude": 38.1166,
            "longitude": 13.3636,
        },
        "Cagliari": {
            "latitude": 39.2305,
            "longitude": 9.1192,
        },
        "Bologna": {
            "latitude": 44.4938,
            "longitude": 11.3387,
        },
        "Torino": {
            "latitude": 45.0705,
            "longitude": 7.6868,
        },
        "Venezia": {
            "latitude": 45.4371,
            "longitude": 12.3326,
        },
        "Firenze": {
            "latitude": 43.7792,
            "longitude": 11.2463,
        },
        "Genova": {
            "latitude": 44.4048,
            "longitude": 8.9444,
        }
    }


    for city, coords in cities.items():
        df = download_openmeteo(
            latitude=coords["latitude"],
            longitude=coords["longitude"],
            start_date=start_date,
            end_date=end_date
        )

        time_sleep = 20
        df.to_csv(f"{DATA_FOLDER}/city_openmeteo_{city.lower()}.csv", index=False)
        print(f"Open-Meteo data saved to {DATA_FOLDER}/city_openmeteo_{city.lower()}.csv (sleep {time_sleep} seconds)")
        time.sleep(time_sleep)  # Sleep to avoid hitting the API too quickly


def download_openmeteo(latitude, longitude, start_date, end_date):

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "Europe/Berlin",
    }
    responses = openmeteo.weather_api(url, params = params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        ).tz_convert(response.Timezone().decode())
    }

    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min

    daily_dataframe = pd.DataFrame(data = daily_data)

    return daily_dataframe