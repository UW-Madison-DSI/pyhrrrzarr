import pydantic
import numpy as np
import xarray as xr
from datetime import datetime
import cartopy.crs as ccrs

from pyhrrrzarr.schema import Location
from pyhrrrzarr.hrrr.schema import HRRRVariable, LevelType, ModelType
from pyhrrrzarr.hrrrzarr.chunk import get_nearest_point, get_chunk_index
from pyhrrrzarr.hrrrzarr.projection import DEFAULT_PROJECTION


class ZarrId(pydantic.BaseModel):
    """all identifiers necessary to describe and access relevant HRRRZarr Zarr array"""
    run_hour: datetime
    level_type: LevelType
    variable: HRRRVariable
    model_type: ModelType 

    def format_chunk_id(self, chunk_id):
        if self.model_type == "fcst":
            # Extra id part since forecasts have an additional (time) dimension
            return "0." + str(chunk_id)
        else:
            return chunk_id


class Request(pydantic.BaseModel):
    """Request schema"""
    zarr_id: ZarrId
    location: Location
    value: float | None = None

    def chunk_id(self) -> str:
        chunk_ds = get_nearest_point(self.location)
        chunk_id_str = f"{chunk_ds.chunk_y.item()}.{chunk_ds.chunk_x.item()}"
        return self.zarr_id.format_chunk_id(chunk_id_str)
    
    def https_url(self) -> str:
        url = "https://hrrrzarr.s3.amazonaws.com"
        url += self.zarr_id.run_hour.strftime(
        f"/{self.zarr_id.level_type}/%Y%m%d/%Y%m%d_%Hz_{self.zarr_id.model_type}.zarr/")
        url += f"{self.zarr_id.variable.name.value}/{self.zarr_id.variable.name.value}/{self.zarr_id.variable.level.value}/{self.zarr_id.variable.name.value}"
        url += f"/{self.chunk_id()}"
        return url
    
    def create_s3_group_url(self, prefix=True):
        url = "s3://hrrrzarr/" if prefix else "" # Skip when using boto3
        url += self.zarr_id.run_hour.strftime(
            f"{self.zarr_id.level_type}/%Y%m%d/%Y%m%d_%Hz_{self.zarr_id.model_type}.zarr/")
        url += f"{self.zarr_id.variable.level.value}/{self.zarr_id.variable.name.value}"
        return url
    
    def create_s3_subgroup_url(self, prefix=True):
        url = self.create_s3_group_url(prefix)
        url += f"/{self.zarr_id.variable.level.value}"
        return url
    
    def create_s3_chunk_url(self, prefix=False):
        url = self.create_s3_subgroup_url(prefix)
        url += f"/{self.zarr_id.variable.name.value}/{self.chunk_id()}"
        return url

    def get_nearest_point(
        self,
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
        x, y = projection.transform_point(self.location.lon, self.location.lat, ccrs.PlateCarree())
        return chunk_index.sel(x=x, y=y, method="nearest")


    def get_value(self, chunk_data: np.ndarray) -> np.ndarray | None:
        """
        fetch zarr_id @ chunk form s3, decompress, return nearest valye to your nearest point
        :param zarr_id: hrrr defining
        :param chunk_id:
        :param nearest_point:
        :return:
        """
        nearest_point = self.get_nearest_point()
        if self.zarr_id.model_type == "fcst":
            self.value = chunk_data[:, nearest_point.in_chunk_y.values, nearest_point.in_chunk_x.values]
        else:
            self.value =  chunk_data[nearest_point.in_chunk_y.values, nearest_point.in_chunk_x.values]
        return self.value