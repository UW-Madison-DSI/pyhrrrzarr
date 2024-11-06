import asyncio
from datetime import datetime

import pandas as pd
import nest_asyncio

from pyhrrrzarr.hrrr.schema import HRRRVariable
from pyhrrrzarr.schema import Location
from pyhrrrzarr.hrrrzarr.requests import create_requests
from pyhrrrzarr.hrrrzarr.fetch import get_all_request_values
from pyhrrrzarr.hrrrzarr.postprocess import requests_to_df


nest_asyncio.apply()


def fetch_hrrr_data(variables: list[HRRRVariable], locations: list[Location], start: datetime, end: datetime) -> pd.DataFrame:
    """
    Fetch HRRR data for the given variables, locations, and timeframe
    """
    requests = create_requests(
        locations=locations,
        variables=variables,
        start=start,
        end=end
    )

    # download the data``
    requests = asyncio.run(get_all_request_values(requests, batch_size=5500))

    # convert the requests to a pandas dataframe
    return requests_to_df([r for r in requests if r.value is not None])

