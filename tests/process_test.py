import logging
import pytest
from dataclasses import dataclass
from read import read_gpx_file
from process import GPXDataFrameTransformer
from convert import GPXDataFrameConverter
from utils import COLS
import test_utils

import gpxpy
import pandas as pd

logger = logging.getLogger(__name__)


@pytest.fixture
def convert_distance_dataframe() -> pd.DataFrame:
	gpx = test_utils.parse_gpx_file("gpx_distances.gpx")
	converter = GPXDataFrameConverter(gpx)
	return converter.get_track_points()


def test_distance_sum(convert_distance_dataframe) -> None:
	"""Test total calculated distance of converted gpx data."""
	df_actual = GPXDataFrameTransformer.label_distance(
		convert_distance_dataframe)
	actual = df_actual[COLS.distance].sum()
	logger.debug(actual)
	assert actual == pytest.approx(22600, abs=10)

# TODO: fix issue with 2d haversine distance calculation. Large distances
# are inaccurate
distance_values_1 = test_utils.TestDistanceValue(long1=47.98,
												 lat1=-37.30,
												 long2=47.14,
												 lat2=-35.26,
												 distance=180.0
												 )

def test_distance_value() -> None:
	actual = gpxpy.geo.haversine_distance(
		latitude_1=distance_values_1.lat1,
		longitude_1=distance_values_1.long1,
		latitude_2=distance_values_1.lat2,
		longitude_2=distance_values_1.long2,
	)
	assert actual == distance_values_1.distance
