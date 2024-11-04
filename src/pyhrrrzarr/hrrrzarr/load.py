import s3fs
import numpy as np
import xarray as xr

from fires.core import ZarrId
from fires.dataset.hrrr.zarr.projection import default_projection
from fires.dataset.hrrr.zarr.fs import default_fs
from fires.dataset.hrrr.zarr.url import create_s3_chunk_url
from fires.dataset.hrrr.zarr.chunk import (
    retrieve_object,
    decompress_chunk,
)


def load_dataset(urls: list[str]) -> xr.Dataset:
    projection = default_projection()
    fs = default_fs()
    ds = xr.open_mfdataset([s3fs.S3Map(url, s3=fs) for url in urls], engine='zarr')

    # add the projection data
    ds = ds.rename(projection_x_coordinate="x", projection_y_coordinate="y")
    ds = ds.metpy.assign_crs(projection.to_cf())
    ds = ds.metpy.assign_latitude_longitude()
    return ds


def get_value(zarr_id: ZarrId, chunk_id: str, nearest_point: xr.Dataset) -> np.ndarray | None:
    """
    fetch zarr_id @ chunk form s3, decompress, return nearest valye to your nearest point
    :param zarr_id: hrrr defining
    :param chunk_id:
    :param nearest_point:
    :return:
    """
    s3 = None
    compressed_data = retrieve_object(
        s3_url=create_s3_chunk_url(zarr_id, chunk_id),
        s3=s3
    )
    if compressed_data:
        chunk_data = decompress_chunk(zarr_id, compressed_data)
        if zarr_id.model_type == "fcst":
            return chunk_data[:, nearest_point.in_chunk_y.values, nearest_point.in_chunk_x.values]
        else:
            return chunk_data[nearest_point.in_chunk_y.values, nearest_point.in_chunk_x.values]
    else:
        return None