import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

from pyhrrrzarr.schema import Location
from pyhrrrzarr.hrrr.schema import HRRRVariable
from pyhrrrzarr.hrrrzarr.schema import ZarrId, Request, LevelType, ModelType


def create_requests(
        locations: list[Location], 
        variables: list[HRRRVariable], 
        level_type: LevelType,
        model_type: ModelType,
        start: datetime, 
        end: datetime
    ) -> list[Request]:
    """Fetch the data from the HRRR archive for the given variables at every location, during time range"""

    # get the time range by hour
    start_hour = start.replace(minute=0, second=0, microsecond=0)
    end_hour = end.replace(minute=0, second=0, microsecond=0)
    if start_hour > end_hour:
        start_hour, end_hour = end_hour, start_hour
    run_hours = [start_hour + timedelta(hours=i) for i in range((end_hour - start_hour).days * 24)]

    # generate ZarrIds for the given variables and time range
    zarr_ids = []
    for hour in run_hours:
        for variable in variables:
            zarr_ids.append(
                    ZarrId(
                        run_hour=hour,
                        level_type=level_type,
                        variable=variable,
                        model_type=model_type, 
                    )
            )

    # generate Requests for the given locations and ZarrIds
    requests = []
    for zarr_id in [x for x in zarr_ids if x]:
        for location in [x for x in locations if x]:
            requests.append(
                Request(
                    zarr_id=zarr_id,
                    location=location,
                )
            )
    
    return requests


def requests_to_df(requests: list[Request]) -> pd.DataFrame:
    data = []
    for r in requests:
        data.append({
            "location": r.location.name,
            "lat": r.location.lat,
            "lon": r.location.lon,
            "run_hour": r.zarr_id.run_hour,
            "var_name": r.zarr_id.variable.name.value,
            "var_level": r.zarr_id.variable.level.value,
            "value": r.value.item() if r.value else None,
            "units": r.zarr_id.variable.units,
        })
    return pd.DataFrame(data)


def csv_to_locations(file_path: Path, keys: dict[str, str] | None = None) -> list[Location]:
    """
    Read a CSV file and return a list of Location objects.

    :param file_path: Path to the CSV file.
    :param keys: Dictionary with keys for the columns in the CSV file. define: name, lat and lon.
    :return: List of Location objects
    """
    if not keys:
        keys = {
            "name": "Station ID",
            "lat": "Latitude",
            "lon": "Longitude",
        }
    df = pd.read_csv(file_path)
    locations = []
    for i, row in df.iterrows():
        locations.append(
            Location(
                name=row[keys["name"]],
                lat=row[keys["lat"]],
                lon=row[keys["lon"]],
            )
        )
    return locations


def add_wind_speed_and_direction(df: pd.DataFrame) -> pd.DataFrame:
    ugrd_df = df[df["var_name"] == "UGRD"]
    vgrd_df = df[df["var_name"] == "VGRD"]
    # join the two dataframes on the time and location
    uv_df = pd.merge(ugrd_df, vgrd_df, on=["run_hour", "location"], suffixes=("_u", "_v"))
    # calculate the wind speed
    uv_df["wind_speed"] = (uv_df["value_u"]**2 + uv_df["value_v"]**2)**0.5
    # calculate the wind direction
    uv_df["wind_dir"] = 180 + (180 / 3.14159) * np.arctan2(uv_df["value_u"], uv_df["value_v"])
    # match column name and count to the original dataframe
    uv_df = (
        uv_df
        .rename(columns={x: x[:-2] for x in uv_df.columns if x[-2:] == "_u"})
        .drop(columns=[x for x in uv_df.columns if x[-2:] == "_v"])
    )
    wind_speed_df = (
        uv_df
        .drop(columns=["value", "wind_dir"])
        .rename(columns={"wind_speed": "value"})
    )
    wind_speed_df["var_name"] = "WIND_SPEED"

    wind_dir_df = (
        uv_df
        .drop(columns=["value", "wind_speed"])
        .rename(columns={"wind_dir": "value"})
    )
    wind_dir_df["var_name"] = "WIND_DIR"
    wind_dir_df["units"] = "degrees"

    return pd.concat([df, wind_speed_df, wind_dir_df], ignore_index=True) 