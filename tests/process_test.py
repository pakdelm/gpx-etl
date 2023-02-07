import logging
import pytest

from read import read_gpx_file
from process import GPXDataFrameTransformer

logger = logging.getLogger(__name__)

TEST_FILES_DIR = "tests/test_files"


def test_label_distances():
	gpx = read_gpx_file(f"{TEST_FILES_DIR}/gpx_distances.gpx")
	gpx_transformer = GPXDataFrameTransformer(gpx)
	df_gpx = gpx_transformer.converter.get_track_points()
	df_distances = gpx_transformer.label_distance(df_gpx)
	expected_distance = df_distances["distance"].sum()

	logger.debug(expected_distance)

	assert expected_distance == pytest.approx(22600, abs=10)
