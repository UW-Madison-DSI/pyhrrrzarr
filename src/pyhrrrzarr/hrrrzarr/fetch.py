import os
import asyncio
import concurrent.futures
from tqdm.auto import tqdm
import aiofiles as aiof
from pathlib import Path
import logging

from pyhrrrzarr.hrrrzarr.s3 import retrieve_object, decompress_chunk
from pyhrrrzarr.hrrrzarr.requests import Request


logger = logging.getLogger(__name__)
CACHE_ROOT = Path(os.environ.get("LOCAL_HRRRZARR_CACHE_PATH"))


async def read_from_hrrrzarr_cache(s3url) -> bytes | None:
    file_path = CACHE_ROOT / s3url / "arr.dat"
    try:
        async with aiof.open(file_path, "rb") as f:
            return await f.read()
    except FileNotFoundError:
        return None


async def write_to_hrrrzarr_cache(s3url, result) -> None:
    file_path = CACHE_ROOT / s3url / "arr.dat"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        async with aiof.open(file_path, "wb") as f:
            await f.write(result)
    except Exception as e:
        logger.error(f"Error writing to cache: {file_path}; {e}")


async def hrrr_fetch(r: Request) -> tuple[Request, bytes | None]:
    """
    get value for request from cache or s3
    return request, and chunk as compressed bytes 
    """
    s3url = r.create_s3_chunk_url()
    result = await read_from_hrrrzarr_cache(s3url=s3url)
    if not result:
        result = await asyncio.to_thread(retrieve_object, s3url)
        if not result:
            return r, result
        await write_to_hrrrzarr_cache(s3url, result)
    return r, result



def decompress_one_chunk(request_compressed_bytes_tuple: tuple[Request, bytes]) -> None:
    """
    decompress one chunk
    """

    request, compressed_bytes = request_compressed_bytes_tuple
    try:
        arr = decompress_chunk(request.zarr_id, compressed_bytes)
        request.get_value(arr)
    except Exception as e:
        logger.error(f"Failed to decompress chunk {request}: {e}")
    
    return request


async def get_all_request_values(requests: list[Request], batch_size: int = 500) -> None:
    """
    get all values for all requests

    requests: list[Request]
    batch_size: int, default 500, number of requests to fetch concurrently
    """
    # group all requests into batches of batch_size
    request_batches = []
    for i in range(0, len(requests), batch_size):
        try:
            request_batches.append(requests[i : i + batch_size])
        except IndexError:
            request_batches.append(requests[i:])
    
    requests_and_compressed_bytes = []
    pbar = tqdm(request_batches, desc="Fetching HRRR data", total=len(requests))
    for request_batch in request_batches:
        batch_requests_and_compressed_bytes = await asyncio.gather(
            *[hrrr_fetch(r) for r in request_batch]
        )
        requests_and_compressed_bytes.extend(batch_requests_and_compressed_bytes)    
        pbar.update(len(request_batch))
    
    l = len(requests_and_compressed_bytes)
    updated_requests = []
    with tqdm(total=l, desc="decompressing") as pbar:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(decompress_one_chunk, arg) for arg in requests_and_compressed_bytes]
            for future in concurrent.futures.as_completed(futures):
                updated_requests.append(future.result())
                pbar.update(1)
    return updated_requests
