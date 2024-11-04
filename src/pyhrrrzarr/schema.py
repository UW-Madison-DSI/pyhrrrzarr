import pydantic
import pandas as pd
from pathlib import Path


class Location(pydantic.BaseModel):
    """lat and lon are required and must be within the range of -90 to 90 and -180 to 180 respectively"""
    lat: float
    lon: float
    name: str | None = None

    @pydantic.field_validator("lat")
    @classmethod
    def lat_range(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError("latitude must be within the range of -90 to 90")
        return v
    
    @pydantic.field_validator("lon")
    @classmethod
    def lon_range(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError("longitude must be within the range of -180 to 180")
        return v



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