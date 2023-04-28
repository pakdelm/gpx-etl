import logging

import pandas as pd
import pytest

from test_utils import add_sec
from utils import COLS

from convert import GPXTransformer
from read import read_gpx_file

import gpxpy.gpx as mod_gpx
from datetime import datetime, timedelta

pd.set_option("display.max_columns", None)

logger = logging.getLogger(__name__)

TEST_FILES_DIR = "test_files"


@pytest.fixture
def create_gpx_data() -> pd.DataFrame:
	gpx = read_gpx_file(f"{TEST_FILES_DIR}/gpx_distances.gpx")
	df_gpx = GPXTransformer(gpx).transform()
	return df_gpx


def test_label_distances(create_gpx_data):
	df_gpx = create_gpx_data
	actual_distance = df_gpx["distance"].sum()

	logger.debug(actual_distance)

	assert actual_distance == pytest.approx(22600, abs=10)


def test_label_altitude():
	start_time = datetime(2023, 1, 1, 0, 0, 0)
	one_second = timedelta(seconds=1)

	gpx = mod_gpx.GPX()
	gpx.tracks.append(mod_gpx.GPXTrack(name="test"))
	gpx.tracks[0].segments.append(mod_gpx.GPXTrackSegment())
	gpx.tracks[0].segments[0].points.append(
		mod_gpx.GPXTrackPoint(latitude=12, longitude=13, elevation=90, time=start_time))
	gpx.tracks[0].segments[0].points.append(
		mod_gpx.GPXTrackPoint(latitude=12, longitude=13, elevation=100,
							  time=add_sec(start_time, 1)))
	gpx.tracks[0].segments[0].points.append(
		mod_gpx.GPXTrackPoint(latitude=12, longitude=13, elevation=50,
							  time=add_sec(start_time, 2)))
	df_gpx = GPXTransformer(gpx).transform()

	alt_gain = df_gpx[COLS.altitude_gain].sum()
	alt_loss = df_gpx[COLS.altitude_loss].sum()

	assert alt_gain == 10
	assert alt_loss == -50
