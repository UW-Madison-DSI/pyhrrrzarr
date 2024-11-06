from datetime import datetime

import pandas as pd

from pyhrrrzarr.main import fetch_hrrr_data
from pyhrrrzarr.hrrr.schema import HRRRVariable, VariableName, Level
from pyhrrrzarr.schema import Location


def test_pull_data_from_hrrr_zarr():
    variables = [
        HRRRVariable(name=VariableName.DPT, level=Level._2M_ABOVE_GROUND),
        HRRRVariable(name=VariableName.APCP_1hr_acc_fcst, level=Level._SURFACE, type_model="fcst"),
    ]
    locations = [
        Location(name="Madison", lat=43.0731, lon=-89.4012),
        Location(name="Seattle", lat=47.6062, lon=-122.3321),
    ]
    start=datetime(2024, 10, 1, 0, 0)
    end=datetime(2024, 10, 2, 0, 0)
    df = fetch_hrrr_data(variables=variables, locations=locations, start=start, end=end)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
