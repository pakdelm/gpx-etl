import logging
import pytest

from convert import GPXTransformer
from read import read_gpx_file

logger = logging.getLogger(__name__)

TEST_FILES_DIR = "tests/test_files"


def test_label_distances():
	gpx = read_gpx_file(f"{TEST_FILES_DIR}/gpx_distances.gpx")
	gpx_etl = GPXTransformer(gpx)
	df_gpx = gpx_etl._get_track_points()
	df_distances = gpx_etl._label_distance(df_gpx)
	expected_distance = df_distances["distance"].sum()

	logger.debug(expected_distance)

	assert expected_distance == pytest.approx(22600, abs=10)
