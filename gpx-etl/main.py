import pandas as pd
import reader
import gpxpy

pd.set_option("display.max_columns", None)

DATA_DIR = "../data"
TEST_FILE_PATH = f"{DATA_DIR}/gpx_trk_trkseg.gpx"

if __name__ == "__main__":

	test_list = [1, 2, 3]

	gpx = reader.load_gpx(TEST_FILE_PATH)

	converter = reader.GPXDataFrameConverter(gpx)

	df_metadata = converter.get_metadata
	df_gpx = converter.get_track_points

	df_join = df_gpx.merge(df_metadata, how="cross")

	print(df_join.head())
# data = reader.read_gpx_data(TEST_FILE_PATH)

# with open(TEST_FILE_PATH, 'r', encoding="utf-8") as gpx_file:
#	gpx = gpxpy.parse(gpx_file)

# print(type(gpx.tracks[0]))
# print(gpx.tracks[0].segments[0])
