import os
import functools

import s3fs
import xarray as xr
from pathlib import Path
import cartopy.crs as ccrs
from dotenv import load_dotenv

from pyhrrrzarr.schema import Location
from pyhrrrzarr.hrrrzarr.fs import DEFAULT_FS
from pyhrrrzarr.hrrrzarr.projection import DEFAULT_PROJECTION


load_dotenv()


@functools.lru_cache(maxsize=1, typed=False)
def get_chunk_index(
        fs: s3fs.S3FileSystem | None = None,
        local_chunk_index_path: Path | None = None,
        clobber: bool = False
) -> xr.Dataset:
    """load from disk or fetch from AWS and return lat lon -> chunk_id lookup xr.dataset"""
    default_chunk_index_path = Path(os.environ.get("LOCAL_ZARR_CHUNK_INDEX_PATH","")).expanduser() / "local_chunk_index.zarr"
    if not local_chunk_index_path:
        local_chunk_index_path = default_chunk_index_path
    if not fs:
        fs = DEFAULT_FS
    if not local_chunk_index_path.exists() or clobber:
        chunk_index = xr.open_zarr(s3fs.S3Map("s3://hrrrzarr/grid/HRRR_chunk_index.zarr", s3=fs))
        chunk_index['chunk_id'] = chunk_index.chunk_id.astype(str)
        _ = chunk_index.to_zarr(local_chunk_index_path, mode='w')
        if not local_chunk_index_path.exists():
            raise FileNotFoundError("No existing chunk index and unable to download it")
    return xr.open_zarr(local_chunk_index_path)


def get_nearest_point(
        location: Location,
        projection: ccrs.LambertConformal | None = None,
        chunk_index: xr.Dataset | None = None,
) -> xr.Dataset:
    """
    return nearest point in chunk index to give Location
    :param point:
    :param projection:
    :param chunk_index:
    :return: xr.Dataset containing
    """
    if not projection:
        projection = DEFAULT_PROJECTION
    if not chunk_index:
        chunk_index = get_chunk_index()
    x, y = projection.transform_point(location.lon, location.lat, ccrs.PlateCarree())
    return chunk_index.sel(x=x, y=y, method="nearest")
