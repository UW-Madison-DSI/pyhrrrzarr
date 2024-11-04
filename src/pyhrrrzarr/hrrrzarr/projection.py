import cartopy.crs as ccrs


DEFAULT_PROJECTION = ccrs.LambertConformal(
    central_longitude=262.5,
    central_latitude=38.5,
    standard_parallels=(38.5, 38.5),
    globe=ccrs.Globe(
        semimajor_axis=6371229,
        semiminor_axis=6371229
    )
)
