import pytest

import read
from process import GPXDataFrameTransformer

TEST_FILES_DIR = "test_files"

def test_label_distances():
	gpx = read.read_gpx_file(f"{TEST_FILES_DIR}/gpx_distances.gpx")
	gpx_transformer = GPXDataFrameTransformer(gpx)

	df_gpx = gpx_transformer.converter.get_track_points()

	df_distances = gpx_transformer.label_distances(df_gpx)

	sum_distance = df_distances["distance"].sum()

	assert (sum_distance) == pytest.approx(22600, 6)