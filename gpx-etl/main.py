import utils
import pandas as pd
import read
import convert
import process
import gpxpy

pd.set_option("display.max_columns", None)

DATA_DIR = "../data"
TEST_FILE_PATH = f"{DATA_DIR}/gpx_trk_trkseg.gpx"

if __name__ == "__main__":
	print(utils.COLS)

	gpx = read.read_gpx_file(TEST_FILE_PATH)

	gpx_converter = convert.GPXDataFrameConverter(gpx)

	#df_metadata = gpx_converter.get_metadata()
	#df_gpx = gpx_converter.get_track_points()

	# df_join = df_gpx.merge(df_metadata, how="cross")

	gpx_transformer = process.GPXDataFrameTransformer(gpx)
	df_enriched_metadata = gpx_transformer.enrich_metadata()
	df_label_distances = gpx_transformer.label_distances(df_enriched_metadata)
	# print(df_enriched_metadata.head())

	print(df_label_distances.head(50))
	print(df_label_distances.columns)
# data = reader.read_gpx_data(TEST_FILE_PATH)

# with open(TEST_FILE_PATH, 'r', encoding="utf-8") as gpx_file:
#	gpx = gpxpy.parse(gpx_file)

# print(type(gpx.tracks[0]))
# print(gpx.tracks[0].segments[0])
