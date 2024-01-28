import logging

import pandas as pd
import pytest
from gpxpy.gpx import GPXTrackPoint

from gpx_etl.convert import GPXTransformer
from gpx_etl.read import read_gpx_file
from gpx_etl.utils import COLS
from tests.test_utils import generate_gpx_data

pd.set_option("display.max_columns", None)
logger = logging.getLogger(__name__)

TEST_FILES_DIR = "tests/test_files"


@pytest.fixture(scope="function")
def create_gpx_data_from_class(request):
    gpx = generate_gpx_data(request.param)
    df_gpx = GPXTransformer(gpx).transform()
    return df_gpx


@pytest.fixture(scope="function")
def create_gpx_data_from_file(request) -> pd.DataFrame:
    gpx_file_name = request.param
    gpx = read_gpx_file(f"{TEST_FILES_DIR}/{gpx_file_name}")
    df_gpx = GPXTransformer(gpx).transform()
    return df_gpx


@pytest.mark.parametrize(
    "create_gpx_data_from_class",
    [
        [
            GPXTrackPoint(latitude=40.73, longitude=-73.93),
            GPXTrackPoint(latitude=34.05, longitude=-118.24),
        ]
    ],
    indirect=True,
)
def test_label_long_distances(create_gpx_data_from_class):
    df_gpx = create_gpx_data_from_class
    distance = df_gpx[COLS.distance].sum()
    assert distance == pytest.approx(3935.74 * 1000, rel=0.003)


@pytest.mark.parametrize(
    "create_gpx_data_from_class",
    [
        [
            GPXTrackPoint(latitude=40.75800984165629, longitude=-73.98555149950363),
            GPXTrackPoint(latitude=40.75792384534224, longitude=-73.98557159337123),
            GPXTrackPoint(latitude=40.75788219536777, longitude=-73.98560377987873),
            GPXTrackPoint(latitude=40.7578319106077, longitude=-73.98565742405792),
        ]
    ],
    indirect=True,
)
def test_label_short_distances(create_gpx_data_from_class):
    df_gpx = create_gpx_data_from_class
    distance = df_gpx[COLS.distance].sum()
    assert distance == pytest.approx(22.3, rel=0.003)


@pytest.mark.parametrize("create_gpx_data_from_file", ["gpx_distances.gpx"], indirect=True)
def test_label_distances_from_file(create_gpx_data_from_file):
    df_gpx = create_gpx_data_from_file
    actual_distance = df_gpx[COLS.distance].sum()
    assert actual_distance == pytest.approx(22600, abs=10)


@pytest.mark.parametrize(
    "create_gpx_data_from_class",
    [
        [
            GPXTrackPoint(latitude=12, longitude=13, elevation=90),
            GPXTrackPoint(latitude=12, longitude=13, elevation=100),
            GPXTrackPoint(latitude=12, longitude=13, elevation=50),
        ]
    ],
    indirect=True,
)
def test_label_altitude(create_gpx_data_from_class):
    df_gpx = create_gpx_data_from_class
    alt_gain = df_gpx[COLS.altitude_gain].sum()
    alt_loss = df_gpx[COLS.altitude_loss].sum()
    assert alt_gain == 10
    assert alt_loss == -50
