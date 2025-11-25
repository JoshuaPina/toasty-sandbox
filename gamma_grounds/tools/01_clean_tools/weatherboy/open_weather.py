# Script from Open-Meteo's website. Coordinates are for the city of Atlanta. Consider getting coords of each NPU for more focused results


import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 33.749,
	"longitude": 84.388,
	"start_date": "2021-01-01",
	"end_date": "2024-12-31",
	"daily": ["sunrise", "daylight_duration", "sunshine_duration", "precipitation_hours", "rain_sum", "temperature_2m_mean", "weather_code"],
	"hourly": ["temperature_2m", "precipitation", "rain", "apparent_temperature", "weather_code", "is_day"],
	"timezone": "America/New_York",
	"temperature_unit": "fahrenheit",
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
hourly_rain = hourly.Variables(2).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(4).ValuesAsNumpy()
hourly_is_day = hourly.Variables(5).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["precipitation"] = hourly_precipitation
hourly_data["rain"] = hourly_rain
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["weather_code"] = hourly_weather_code
hourly_data["is_day"] = hourly_is_day

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("\nHourly data\n", hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_sunrise = daily.Variables(0).ValuesInt64AsNumpy()
daily_daylight_duration = daily.Variables(1).ValuesAsNumpy()
daily_sunshine_duration = daily.Variables(2).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(3).ValuesAsNumpy()
daily_rain_sum = daily.Variables(4).ValuesAsNumpy()
daily_temperature_2m_mean = daily.Variables(5).ValuesAsNumpy()
daily_weather_code = daily.Variables(6).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["sunrise"] = daily_sunrise
daily_data["daylight_duration"] = daily_daylight_duration
daily_data["sunshine_duration"] = daily_sunshine_duration
daily_data["precipitation_hours"] = daily_precipitation_hours
daily_data["rain_sum"] = daily_rain_sum
daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
daily_data["weather_code"] = daily_weather_code

daily_dataframe = pd.DataFrame(data = daily_data)
print("\nDaily data\n", daily_dataframe)

hourly_dataframe.to_csv('atlanta_hourly_weather.csv', index=False)
daily_dataframe.to_csv('atlanta_daily_weather.csv', index=False)

print("\nData saved to CSV files:")
print("- atlanta_hourly_weather.csv")
print("- atlanta_daily_weather.csv")