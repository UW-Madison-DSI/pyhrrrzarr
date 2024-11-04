from pyhrrrzarr.hrrr.schema import VariableName, Level, HRRRVariable


def test_create_hrrr_variable():
    hv = HRRRVariable(
        variable=VariableName.TMP,
        level=Level._2M_ABOVE_GROUND,
        forecast_hour=0
    )
    assert str(hv) == "TMP_2m_above_ground"
