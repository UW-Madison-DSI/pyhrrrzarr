from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field, computed_field


class VariableName(Enum):
    """all HRRR variable names"""

    # CIN = 'CIN' # Convective Inhibition 255_0mb_above_ground
    # CIN = 'CIN' # Convective Inhibition 90_0mb_above_ground
    # CIN = 'CIN' # Convective Inhibition surface
    # HAIL_1hr_max_fcst = 'HAIL_1hr_max_fcst' # Hail 0.1_sigma_layer
    # HAIL_1hr_max_fcst = 'HAIL_1hr_max_fcst' # Hail surface
    # HAIL_max_fcst = 'HAIL_max_fcst' # Hail 0.1_sigma_layer
    # HAIL_max_fcst = 'HAIL_max_fcst' # Hail surface
    # HGT = 'HGT' # Geopotential Height 1000mb
    # HGT = 'HGT' # Geopotential Height 500mb
    # HGT = 'HGT' # Geopotential Height 700mb
    # HGT = 'HGT' # Geopotential Height 850mb
    # HGT = 'HGT' # Geopotential Height cloud_base
    # HGT = 'HGT' # Geopotential Height cloud_ceiling
    # HGT = 'HGT' # Geopotential Height cloud_top
    # HGT = 'HGT' # Geopotential Height level_of_adiabatic_condensation_from_sfc
    # HGT = 'HGT' # Geopotential Height surface
    # HGT = 'HGT' # Height at the 253 K 253K_level
    # HGT = 'HGT' # Height at the 263 K 263K_level
    # HGT = 'HGT' # Height of the highest tropospheric freezing level highest_tropospheric_freezing_level
    # HGT = 'HGT' # Height of the Level of Equilibrium Level equilibrium_level
    # HGT = 'HGT' # Height of the Level of Free Convection no_level
    # HLCY = 'HLCY' # Storm Relative Helicity 1000_0m_above_ground
    # LTPINX = 'LTPINX' # Lightning Potential Index 1m_above_ground
    # MNUPHL_1hr_min_fcst = 'MNUPHL_1hr_min_fcst' # Hourly Minimum of Updraft Helicity 3000_0m_above_ground
    # MNUPHL_1hr_min_fcst = 'MNUPHL_1hr_min_fcst' # Hourly Minimum of Updraft Helicity 5000_2000m_above_ground
    # MNUPHL_min_fcst = 'MNUPHL_min_fcst' # Hourly Minimum of Updraft Helicity 3000_0m_above_ground
    # MNUPHL_min_fcst = 'MNUPHL_min_fcst' # Hourly Minimum of Updraft Helicity 5000_2000m_above_ground
    # MXUPHL_1hr_max_fcst = 'MXUPHL_1hr_max_fcst' # Hourly Maximum of Updraft Helicity 3000_0m_above_ground
    # MXUPHL_1hr_max_fcst = 'MXUPHL_1hr_max_fcst' # Hourly Maximum of Updraft Helicity 5000_2000m_above_ground
    # MXUPHL_max_fcst = 'MXUPHL_max_fcst' # Hourly Maximum of Updraft Helicity 3000_0m_above_ground
    # MXUPHL_max_fcst = 'MXUPHL_max_fcst' # Hourly Maximum of Updraft Helicity 5000_2000m_above_ground
    # PRES = 'PRES' # Pressure at the 0°C isotherm 0C_isotherm
    # PRES = 'PRES' # Pressure at the highest tropospheric freezing level highest_tropospheric_freezing_level
    # PRES = 'PRES' # Pressure cloud_top
    # PRES = 'PRES' # Pressure surface
    # REFD = 'REFD' # Reflectivity 1000m_above_ground
    # REFD = 'REFD' # Reflectivity 4000m_Above_Ground
    # RELV_1hr_max_fcst = 'RELV_1hr_max_fcst' # Relative Vorticity 2000_0m_above_ground
    # RELV_max_fcst = 'RELV_max_fcst' # Relative Vorticity 2000_0m_above_ground
    # RH = 'RH' # Relative Humidity 2m_above_ground
    # RH = 'RH' # Relative Humidity at the highest tropospheric freezing level highest_tropospheric_freezing_level
    # TCDC = 'TCDC' # Total Cloud Cover boundary_layer_cloud_cover
    AOTK = 'AOTK' # Aeorosol Optical Thickness entire_atmosphere_single_layer
    APCP_1hr_acc_fcst = 'APCP_1hr_acc_fcst' # Total Precipitation UTC day surface
    APCP_acc_fcst = 'APCP_acc_fcst' # Total Precipitation UTC day surface
    ASNOW_1hr_acc_fcst = 'ASNOW_1hr_acc_fcst' # Total Snowfall surface
    ASNOW_acc_fcst = 'ASNOW_acc_fcst' # Total Snowfall surface
    BGRUN_1hr_acc_fcst = 'BGRUN_1hr_acc_fcst' # Baseflow Groundwater surface
    BGRUN_acc_fcst = 'BGRUN_acc_fcst' # Baseflow Groundwater surface
    CAPE = 'CAPE' # Convective Available Potential Energy surface
    # CAPE = 'CAPE' # Convective Available Potential Energy 0_3000m_above_ground
    # CAPE = 'CAPE' # Convective Available Potential Energy 180_0mb_above_ground
    # CAPE = 'CAPE' # Convective Available Potential Energy 255_0mb_above_ground
    # CAPE = 'CAPE' # Convective Available Potential Energy 90_0mb_above_ground
    CFNSF = 'CFNSF' # Cloud Forcing Net Solar Flux surface
    CFRZR = 'CFRZR' # Categorical Freezing Rain surface
    CICEP = 'CICEP' # Categorical Ice Pellets surface
    CIN = 'CIN' # Convective Inhibition 180_0mb_above_ground
    CNWAT = 'CNWAT' # Plant Canopy Surface Water surface
    COLMD = 'COLMD' # Total Column Integrated Mass Density entire_atmosphere_single_layer
    CPOFP = 'CPOFP' # Percent Frozen Precipitation surface
    CRAIN = 'CRAIN' # Categorical Rain surface
    CSNOW = 'CSNOW' # Categorical Snow surface
    DLWRF = 'DLWRF' # Downward Long Wave Rad. Flux surface
    DPT = 'DPT' # Dew Point Temperature
    DSWRF = 'DSWRF' # Downward Short Wave Rad. Flux surface
    DZDT = 'DZDT' # Vertical Velocity 700mb
    DZDT_1hr_ave_fcst = 'DZDT_1hr_ave_fcst' # Vertical Velocity 0.5_0.8_sigma_layer
    DZDT_ave_fcst = 'DZDT_ave_fcst' # Vertical Velocity 0.5_0.8_sigma_layer
    FOURLFTX = '4LFTX' # Best (4 layer) Lifted Index 180_0mb_above_ground
    FRICV = 'FRICV' # Frictional Velocity surface
    FROZR_1hr_acc_fcst = 'FROZR_1hr_acc_fcst' # Frozen RainUTC day surface
    FROZR_acc_fcst = 'FROZR_acc_fcst' # Frozen RainUTC day surface
    FRZR_1hr_acc_fcst = 'FRZR_1hr_acc_fcst' # Freezing Rain UTC day surface
    FRZR_acc_fcst = 'FRZR_acc_fcst' # Freezing Rain UTC day surface
    FTX = '4LFTX' # Best (4 layer) Lifted Index 180_0mb_above_ground
    GFLUX = 'GFLUX' # Ground Heat Flux surface
    GUST = 'GUST' # Wind Gust surface
    HAIL_1hr_max_fcst = 'HAIL_1hr_max_fcst' # Hail entire_atmosphere
    HAIL_max_fcst = 'HAIL_max_fcst' # Hail entire_atmosphere
    HCDC = 'HCDC' # High Cloud Cover high_cloud_layer
    HGT = 'HGT' # Height of the 0°C isotherm 0C_isotherm
    HLCY = 'HLCY' # Storm Relative Helicity 3000_0m_above_ground
    HPBL = 'HPBL' # Planetary Boundary Layer Height surface
    ICEC = 'ICEC' # Ice Cover surface
    LAI = 'LAI' # Leaf Area Index surface
    LAND = 'LAND' # Land Cover (0 sea, 1=land surface
    LAYTH = 'LAYTH' # Depth of Layer Supporting Dendritic Growth 261K_level___256K_level
    LCDC = 'LCDC' # Low Cloud Cover low_cloud_layer
    LFTX = 'LFTX' # Surface Lifted Index 500_1000mb
    LHTFL = 'LHTFL' # Latent Heat Net Flux surface
    LTNG = 'LTNG' # Lightning entire_atmosphere
    LTPINX = 'LTPINX' # Lightning Potential Index 2m_above_ground
    MASSDEN = 'MASSDEN' # Mass Density 8m_above_ground
    MAXDVV_1hr_max_fcst = 'MAXDVV_1hr_max_fcst' # Hourly Maximum of Downward Vertical Velocity 100_1000mb_above_ground
    MAXDVV_max_fcst = 'MAXDVV_max_fcst' # Hourly Maximum of Downward Vertical Velocity 100_1000mb_above_ground
    MAXREF_1hr_max_fcst = 'MAXREF_1hr_max_fcst' # Hourly Maximum of Simulated Reflectivity at 1km AGL 1000m_above_ground
    MAXREF_max_fcst = 'MAXREF_max_fcst' # Hourly Maximum of Simulated Reflectivity at 1km AGL 1000m_above_ground
    MAXUVV_1hr_max_fcst = 'MAXUVV_1hr_max_fcst' # Hourly Maximum of Upward Vertical Velocity 100_1000mb_above_ground
    MAXUVV_max_fcst = 'MAXUVV_max_fcst' # Hourly Maximum of Upward Vertical Velocity 100_1000mb_above_ground
    MAXUW_1hr_max_fcst = 'MAXUW_1hr_max_fcst' # U Component of Hourly Maximum Wind 10m_above_ground
    MAXUW_max_fcst = 'MAXUW_max_fcst' # U Component of Hourly Maximum Wind 10m_above_ground
    MAXVW_1hr_max_fcst = 'MAXVW_1hr_max_fcst' # V Component of Hourly Maximum Wind 10m_above_ground
    MAXVW_max_fcst = 'MAXVW_max_fcst' # V Component of Hourly Maximum Wind 10m_above_ground
    MCDC = 'MCDC' # Middle Cloud Cover middle_cloud_layer
    MNUPHL_1hr_min_fcst = 'MNUPHL_1hr_min_fcst' # Hourly Minimum of Updraft Helicity 2000_0m_above_ground
    MNUPHL_min_fcst = 'MNUPHL_min_fcst' # Hourly Minimum of Updraft Helicity 2000_0m_above_ground
    MNVEG = 'MNVEG' # Annual Minimum Vegetation Fraction surface
    MSLMA = 'MSLMA' # Mean Sea Level Pressure mean_sea_level
    MSTAV = 'MSTAV' # Moisture Availability 0m_underground
    MXUPHL_1hr_max_fcst = 'MXUPHL_1hr_max_fcst' # Hourly Maximum of Updraft Helicity 2000_0m_above_ground
    MXUPHL_max_fcst = 'MXUPHL_max_fcst' # Hourly Maximum of Updraft Helicity 2000_0m_above_ground
    MXVEG = 'MXVEG' # Annual Maximum Vegetation Fraction surface
    PLPL = 'PLPL' # Pressure of Level From Which Parcel Was Lifted 255_0mb_above_ground
    POT = 'POT' # Potential Temperature 2m_above_ground
    PRATE = 'PRATE' # Precipitation Rate surface
    PRES = 'PRES' # Pressure cloud_base
    PWAT = 'PWAT' # Precipitable Water entire_atmosphere_single_layer
    REFC = 'REFC' # Composite Reflectivity entire_atmosphere
    REFD = 'REFD' # Reflectivity 263K_level
    REFD_1hr_max_fcst = 'REFD_1hr_max_fcst' # Reflectivity 263K_level
    REFD_max_fcst = 'REFD_max_fcst' # Reflectivity 263K_level
    RELV_1hr_max_fcst = 'RELV_1hr_max_fcst' # Relative Vorticity 1000_0m_above_ground
    RELV_max_fcst = 'RELV_max_fcst' # Relative Vorticity 1000_0m_above_ground
    RETOP = 'RETOP' # Echo Top cloud_top
    RH = 'RH' # Relative Humidity at the 0°C isotherm 0C_isotherm
    RHPW = 'RHPW' # Relative Humidity with Respect to Precipitable Water entire_atmosphere
    SBT113 = 'SBT113' # Simulated Brightness Temperature for GOES 11, Channel 3 top_of_atmosphere
    SBT114 = 'SBT114' # Simulated Brightness Temperature for GOES 11, Channel 4 top_of_atmosphere
    SBT123 = 'SBT123' # Simulated Brightness Temperature for GOES 12, Channel 3 top_of_atmosphere
    SBT124 = 'SBT124' # Simulated Brightness Temperature for GOES 12, Channel 4 top_of_atmosphere
    SFCR = 'SFCR' # Surface Roughness surface
    SHTFL = 'SHTFL' # Sensible Heat Net Flux surface
    SNOD = 'SNOD' # Snow Depth surface
    SNOWC = 'SNOWC' # Snow Cover surface
    SPFH = 'SPFH' # Specific Humidity 2m_above_ground
    SSRUN_1hr_acc_fcst = 'SSRUN_1hr_acc_fcst' # Storm Surface Runoff surface
    SSRUN_acc_fcst = 'SSRUN_acc_fcst' # Storm Surface Runoff surface
    TCDC = 'TCDC' # Total Cloud Cover entire_atmosphere
    TCOLG_1hr_max_fcst = 'TCOLG_1hr_max_fcst' # Total Column Integrated Graupel entire_atmosphere_single_layer
    TCOLG_max_fcst = 'TCOLG_max_fcst' # Total Column Integrated Graupel entire_atmosphere_single_layer
    TCOLWold = 'TCOLWold' # Total Column Integrated Cloud Ice entire_atmosphere_single_layer
    TMP = 'TMP' # Temperature 
    UGRD = 'UGRD' # U Component of Wind
    ULWRF = 'ULWRF' # Upward Long Wave Rad. Flux surface
    # ULWRF = 'ULWRF' # Upward Long Wave Rad. Flux top_of_atmosphere
    USTM = 'USTM' # U Component Storm Motion 0_6000m_above_ground
    USWRF = 'USWRF' # Upward Short Wave Rad. Flux surface
    # USWRF = 'USWRF' # Upward Short Wave Rad. Flux top_of_atmosphere
    VBDSF = 'VBDSF' # Visible Beam Downward Solar Flux surface
    VDDSF = 'VDDSF' # Visible Diffuse Downward Solar Flux surface
    VEG = 'VEG' # Vegetation surface
    VGRD = 'VGRD' # V Component of Wind
    VGTYP = 'VGTYP' # Vegetation Type surface
    VIL = 'VIL' # Vertically Integrated Liquid entire_atmosphere
    VIS = 'VIS' # Visibility surface
    VSTM = 'VSTM' # V Component Storm Motion 0_6000m_above_ground
    VUCSH = 'VUCSH' # U Component Vertical Wind Shear 0_1000m_above_ground
    # VUCSH = 'VUCSH' # U Component Vertical Wind Shear 0_6000m_above_ground
    VVCSH = 'VVCSH' # V Component Vertical Wind Shear 0_1000m_above_ground
    # VVCSH = 'VVCSH' # V Component Vertical Wind Shear 0_6000m_above_ground
    WEASD = 'WEASD' # Water Equivalent of Accumulated Snow Depth surface
    WEASD_1hr_acc_fcst = 'WEASD_1hr_acc_fcst' # Water Equivalent of Accumulated Snow Depth UTC Day surface
    WEASD_acc_fcst = 'WEASD_acc_fcst' # Water Equivalent of Accumulated Snow Depth UTC Day surface
    WIND_1hr_max_fcst = 'WIND_1hr_max_fcst' # Wind Speed 10m_above_ground
    WIND_max_fcst = 'WIND_max_fcst' # Wind Speed 10m_above_ground

class Level(Enum):
    _0_1_SIGMA_LAYER = '0.1_sigma_layer'
    _0_5_0_8_SIGMA_LAYER = '0.5_0.8_sigma_layer'
    _0C_ISOTHERM = '0C_isotherm'
    _0_1000M_ABOVE_GROUND = '0_1000m_above_ground'
    _0_3000M_ABOVE_GROUND = '0_3000m_above_ground'
    _0_6000M_ABOVE_GROUND = '0_6000m_above_ground'
    _0M_UNDERGROUND = '0m_underground'
    _1000_0M_ABOVE_GROUND = '1000_0m_above_ground'
    _1000M_ABOVE_GROUND = '1000m_above_ground'
    _1000MB = '1000mb'
    _100_1000MB_ABOVE_GROUND = '100_1000mb_above_ground'
    _10M_ABOVE_GROUND = '10m_above_ground'
    _180_0MB_ABOVE_GROUND = '180_0mb_above_ground'
    _1M_ABOVE_GROUND = '1m_above_ground'
    _2000_0M_ABOVE_GROUND = '2000_0m_above_ground'
    _250MB = '250mb'
    _253K_LEVEL = '253K_level'
    _255_0MB_ABOVE_GROUND = '255_0mb_above_ground'
    _261K_LEVEL___256K_LEVEL = '261K_level___256K_level'
    _263K_LEVEL = '263K_level'
    _2M_ABOVE_GROUND = '2m_above_ground'
    _3000_0M_ABOVE_GROUND = '3000_0m_above_ground'
    _300MB = '300mb'
    _4000M_ABOVE_GROUND = '4000m_Above_Ground'
    _5000_2000M_ABOVE_GROUND = '5000_2000m_above_ground'
    _500_1000MB = '500_1000mb'
    _500MB = '500mb'
    _700MB = '700mb'
    _80M_ABOVE_GROUND = '80m_above_ground'
    _850MB = '850mb'
    _8M_ABOVE_GROUND = '8m_above_ground'
    _90_0MB_ABOVE_GROUND = '90_0mb_above_ground'
    _925MB = '925mb'
    _BOUNDARY_LAYER_CLOUD_COVER = 'boundary_layer_cloud_cover'
    _CLOUD_BASE = 'cloud_base'
    _CLOUD_CEILING = 'cloud_ceiling'
    _CLOUD_TOP = 'cloud_top'
    _ENTIRE_ATMOSPHERE = 'entire_atmosphere'
    _ENTIRE_ATMOSPHERE_SINGLE_LAYER = 'entire_atmosphere_single_layer'
    _EQUILIBRIUM_LEVEL = 'equilibrium_level'
    _HIGH_CLOUD_LAYER = 'high_cloud_layer'
    _HIGHEST_TROPOSPHERIC_FREEZING_LEVEL = 'highest_tropospheric_freezing_level'
    _LEVEL_OF_ADIABATIC_CONDENSATION_FROM_SFC = 'level_of_adiabatic_condensation_from_sfc'
    _LOW_CLOUD_LAYER = 'low_cloud_layer'
    _MEAN_SEA_LEVEL = 'mean_sea_level'
    _MIDDLE_CLOUD_LAYER = 'middle_cloud_layer'
    _NO_LEVEL = 'no_level'
    _SURFACE = 'surface'
    _TOP_OF_ATMOSPHERE = 'top_of_atmosphere'


VALID_LEVELS_FOR_VARIABLE_NAME = {
    VariableName.TMP: [
        Level._SURFACE,
        Level._2M_ABOVE_GROUND,
        Level._1000MB,
        Level._500MB,
        Level._700MB,
        Level._850MB,
        Level._925MB,
    ],
    VariableName.VGRD: [
        Level._10M_ABOVE_GROUND, 
        Level._80M_ABOVE_GROUND,
        Level._1000MB, 
        Level._250MB,
        Level._300MB,
        Level._500MB,
        Level._700MB,
        Level._850MB,
        Level._925MB
    ],
    VariableName.UGRD: [
        Level._10M_ABOVE_GROUND, 
        Level._80M_ABOVE_GROUND,
        Level._1000MB, 
        Level._250MB,
        Level._300MB,
        Level._500MB,
        Level._700MB,
        Level._850MB,
        Level._925MB
    ],
    VariableName.DPT: [
        Level._2M_ABOVE_GROUND,
        Level._500MB,
        Level._700MB,
        Level._850MB,
        Level._925MB,
        Level._1000MB,
    ],
}


VARIABLE_UNITS = {
    VariableName.APCP_acc_fcst: 'kg/m^2',
    VariableName.DPT: 'K',
    VariableName.RH: '%',
    VariableName.TMP: 'K',
    VariableName.UGRD: 'm/s',
    VariableName.VGRD: 'm/s',
}


class HRRRVariable(BaseModel):
    name: VariableName = Field(default=None)
    level: Level

    @computed_field
    @property
    def units(self) -> str | None:
        return VARIABLE_UNITS.get(self.name, None)
    
    def __repr__(self):
        return f"{self.name.value}_{self.level.value}"

    def __str__(self):
        return self.__repr__()
    