import pytest
from pyhrrrzarr.hrrr.schema import VariableName, Level, HRRRVariable


def test_create_hrrr_variable():
    hv = HRRRVariable(
        name=VariableName.TMP,
        level=Level._2M_ABOVE_GROUND,
        type_level='sfc',
        type_model='anl'
    )
    assert str(hv) == "TMP_2m_above_ground_sfc_anl"


def test_create_hrrr_variable_has_correct_units():
    hv = HRRRVariable(
        name=VariableName.TMP,
        level=Level._2M_ABOVE_GROUND
    )
    assert hv.units == "K"


def test_create_hrrr_variable_with_invalid_level_raises_value_error():
    with pytest.raises(ValueError):
        hv = HRRRVariable(
            name=VariableName.RH,
            level=Level._10M_ABOVE_GROUND,
            type_level='sfc',
            type_model='anl'
        )
