# PyHRRRZarr
Python wrapper for downloading met data from [HRRRZarr](https://mesowest.utah.edu/html/hrrr/).

# Install
```bash
# install pixi see https://pixi.sh/latest/#installation
curl -fsSL https://pixi.sh/install.sh | bash
# pull repo and install locally
git clone git@github.com:UW-Madison-DSI/pyhrrrzarr.git
cd pyhrrrzarr
pixi install
```

# Basic Usage
1. Configure local zarr caching by editing example.env and saving as .env
2. run the following script

```python
from datetime import datetime
from pyhrrrzarr.main import fetch_hrrr_data
from pyhrrrzarr.hrrr.schema import HRRRVariable, VariableName, Level
from pyhrrrzarr.schema import Location


variables = [
    HRRRVariable(name=VariableName.TMP, level=Level._2M_ABOVE_GROUND),
    HRRRVariable(name=VariableName.DPT, level=Level._2M_ABOVE_GROUND),
    HRRRVariable(name=VariableName.APCP_1hr_acc_fcst, level=Level._SURFACE, type_model="fcst"),
    HRRRVariable(name=VariableName.RH, level=Level._2M_ABOVE_GROUND),
    HRRRVariable(name=VariableName.UGRD, level=Level._10M_ABOVE_GROUND),
    HRRRVariable(name=VariableName.VGRD, level=Level._10M_ABOVE_GROUND),
]
locations = [
    Location(name="Madison", lat=43.0731, lon=-89.4012),
    Location(name="Seattle", lat=47.6062, lon=-122.3321),
]
start=datetime(2024, 10, 1, 0, 0)
end=datetime(2024, 10, 2, 0, 0)

df = fetch_hrrr_data(variables=variables, locations=locations, start=start, end=end)
```

for more detail see `notebooks/scratch.py`

