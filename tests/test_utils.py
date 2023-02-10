from dataclasses import dataclass

import gpxpy.gpx

from read import read_gpx_file

TEST_FILES_DIR = "test_files"

@dataclass
class TestDistanceValue:
	long1: float
	lat1: float
	long2: float
	lat2: float
	distance: float


def parse_gpx_file(file_name: str) -> gpxpy.gpx.GPX:
	return read_gpx_file(f"{TEST_FILES_DIR}/{file_name}")