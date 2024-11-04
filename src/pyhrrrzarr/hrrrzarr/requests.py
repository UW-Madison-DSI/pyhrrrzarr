import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

from pyhrrrzarr.schema import Location
from pyhrrrzarr.hrrr.schema import HRRRVariable
from pyhrrrzarr.hrrrzarr.schema import ZarrId, Request


def create_requests(
        locations: list[Location], 
        variables: list[HRRRVariable], 
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
                        level_type=variable.level_type,
                        variable=variable,
                        model_type=variable.model_type, 
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
