import pydantic


class Location(pydantic.BaseModel):
    """lat and lon are required and must be within the range of -90 to 90 and -180 to 180 respectively"""
    lat: float
    lon: float
    name: str | None = None

    @pydantic.field_validator("lat")
    @classmethod
    def lat_range(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError("latitude must be within the range of -90 to 90")
        return v
    
    @pydantic.field_validator("lon")
    @classmethod
    def lon_range(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError("longitude must be within the range of -180 to 180")
        return v
