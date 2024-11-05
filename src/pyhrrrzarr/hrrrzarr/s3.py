import logging
import asyncio
import numpy as np
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import ClientError
import numcodecs as ncd

from pyhrrrzarr.hrrrzarr.fs import DEFAULT_FS
from pyhrrrzarr.hrrrzarr.schema import ZarrId 


def retrieve_object(s3_url: str, s3: boto3.resources.base.ServiceResource | None = None) -> bytes | None:
    if not s3:
        s3 = boto3.resource(service_name='s3', region_name='us-west-1', config=Config(signature_version=UNSIGNED))
    obj = s3.Object('hrrrzarr', s3_url)
    try:
        result = obj.get()['Body'].read()
    except ClientError as ex:
        if ex.response["Error"]["Code"] == 'NoSuchKey':
            logging.warning(f"NoSuchkKey for: {s3_url}")
            result = None
        else:
            raise
    return result


def decompress_chunk(zarr_id: ZarrId, compressed_data: bytes) -> np.ndarray | None:
    try:
        buffer = ncd.blosc.decompress(compressed_data)

        dtype = "<f2"
        if zarr_id.variable.level.name == "surface" and zarr_id.variable.name.value == "PRES":
            dtype = "<f4"

        chunk = np.frombuffer(buffer, dtype=dtype)

        if zarr_id.type_model == "anl":
            data_array = np.reshape(chunk, (150, 150))
        else:
            entry_size = 22500
            data_array = np.reshape(chunk, (len(chunk) // entry_size, 150, 150))
    except Exception as e:
        logging.error(f"Failed to decompress chunk {zarr_id}: {e}")
        data_array = None

    return data_array

