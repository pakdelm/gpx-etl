import logging

import convert
import pandas as pd
import read
import utils

pd.set_option("display.max_columns", None)

DATA_DIR = "../data"
TEST_FILE_PATH = f"{DATA_DIR}/gpx.gpx"


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=utils.LOG_FORMAT)

if __name__ == "__main__":
    gpx = read.read_gpx_file(TEST_FILE_PATH)
    gpx_etl = convert.GPXTransformer(gpx)
    df = gpx_etl.transform()
    print(df.head())
