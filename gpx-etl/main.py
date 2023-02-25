import logging
import utils
import pandas as pd
import read
import convert
import process

pd.set_option("display.max_columns", None)

DATA_DIR = "../data"
TEST_FILE_PATH = f"{DATA_DIR}/gpx.gpx"


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=utils.LOG_FORMAT)

if __name__ == "__main__":

    gpx = read.read_gpx_file(TEST_FILE_PATH)
    gpx_converter = convert.GPXDataFrameConverter(gpx)
    gpx_converter.get_track_points()
    gpx_converter.get_metadata()
    # transformer = process.GPXDataFrameTransformer(gpx)
    # df = transformer.create_data_frame(enrich_metadata=True).pipe(
    #     process.GPXDataFrameTransformer.label_distance
    # )

    # print(df_enriched_metadata.head())

    # print(df.head(50))
    # print(df.columns)
# data = reader.read_gpx_data(TEST_FILE_PATH)

# with open(TEST_FILE_PATH, 'r', encoding="utf-8") as gpx_file:
# 	gpx = gpxpy.parse(gpx_file)

# print(type(gpx.tracks[0]))
# print(gpx.tracks[0].segments[0])
