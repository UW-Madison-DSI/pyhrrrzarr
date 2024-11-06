import logging
import numpy as np
import pandas as pd

from pyhrrrzarr.hrrrzarr.schema import Request


logger = logging.getLogger(__name__)


def requests_to_df(requests: list[Request]) -> pd.DataFrame:
    """
    Convert a list of Request objects to a pandas DataFrame
    NB: use pyhrrrzarr.hrrrzarr.fetch.get_all_request_values to get the *values* for the requests
    """

    data = []
    for r in requests:
        request_value = None
        if r.value is not None:
            try: 
                request_value = r.value[0].item()  # always take first hour of forecast
            except IndexError:
                request_value = r.value.item()
        
        data.append({
            "location": r.location.name,
            "lat": r.location.lat,
            "lon": r.location.lon,
            "run_hour": r.zarr_id.run_hour,
            "var_name": r.zarr_id.variable.name.value,
            "var_level": r.zarr_id.variable.level.value,
            "value": request_value,
            "units": r.zarr_id.variable.units,
        })
    logger.info(f"Converted {len(data)} requests to DataFrame rows")
    return pd.DataFrame(data)


def add_wind_speed_and_direction(df: pd.DataFrame) -> pd.DataFrame:
    ugrd_df = df[df["var_name"] == "UGRD"]
    vgrd_df = df[df["var_name"] == "VGRD"]
    uv_df = pd.merge(ugrd_df, vgrd_df, on=["run_hour", "location"], suffixes=("_u", "_v"))
    uv_df["wind_speed"] = (uv_df["value_u"]**2 + uv_df["value_v"]**2)**0.5
    uv_df["wind_dir"] = 180 + (180 / 3.14159) * np.arctan2(uv_df["value_u"], uv_df["value_v"])
    # format wind speed and dir into original df
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
    logger.info(f"Added {len(wind_speed_df)} wind speed and {len(wind_dir_df)} wind direction rows")
    return pd.concat([df, wind_speed_df, wind_dir_df], ignore_index=True)
