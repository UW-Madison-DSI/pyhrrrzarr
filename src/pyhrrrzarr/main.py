import xarray as xr
from pathlib import Path
from datetime import datetime


from pyhrrrzarr.schema import Location
from pyhrrrzarr.hrrr.schema import HRRRVariable
from pyhrrrzarr.hrrrzarr.chunk import get_chunk_index, get_nearest_point


def create_hrrr_zarr_explorer_url(level_type, model_type, run_hour):
    url = "https://hrrrzarr.s3.amazonaws.com/index.html"
    url += run_hour.strftime(
        f"#{level_type}/%Y%m%d/%Y%m%d_%Hz_{model_type}.zarr/"
    )
    return url


def create_https_chunk_url(zarr_id, chunk_id):
    url = "https://hrrrzarr.s3.amazonaws.com"
    url += zarr_id.run_hour.strftime(
        f"/{zarr_id.level_type}/%Y%m%d/%Y%m%d_%Hz_{zarr_id.model_type}.zarr/")
    url += f"{zarr_id.var_level}/{zarr_id.var_name}/{zarr_id.var_level}/{zarr_id.var_name}"
    url += f"/{zarr_id.format_chunk_id(chunk_id)}"
    return url


def fetch(locations: list[Location], variables: list[HRRRVariable], start: datetime, end: datetime) -> list[Path]:
    """Fetch the data from the HRRR archive for the given variables at every location, during time range"""
    # Create a list of paths to the fetched data
    paths = []



    level_type = "sfc"
    model_type = "fcst"
    run_hour = datetime.datetime(2021, 1, 1, 7)
    url = create_hrrr_zarr_explorer_url(level_type, model_type, run_hour)


    # get a zarr ids

    # convert locations to chunks
    chunk_ds_lst = [get_nearest_point(location, chunk_index=get_chunk_index()) for location in locations]
    



    # generate url

    
    
        
    return paths

    