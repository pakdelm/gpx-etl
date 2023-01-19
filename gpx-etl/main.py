import pandas as pd
import reader
import gpxpy

pd.set_option("display.max_columns", None)

DATA_DIR = "../data"
TEST_FILE_PATH = f"{DATA_DIR}/gpx_trk_trkseg.gpx"

if __name__ == "__main__":

	test_list = [1, 2, 3]

	gpx = reader.load_gpx(TEST_FILE_PATH)

	converter = reader.DataFrameConverter(gpx)

	df_metadata = converter.get_metadata

	tmp = []
	for track in gpx.tracks:
		print(track.name)

		for index, segment in enumerate(track.segments):
			print(index)
			print(segment)
			print(segment.points)

			for point in segment.points:
				df_tmp = pd.DataFrame(
					{
						'track_name': track.name,
						'segment_index': index,
						'longitude': [point.longitude],
						'latitude': [point.latitude],
						'elevation': [point.elevation],
						'time': [point.time.replace(tzinfo=None, microsecond=0)]  # type: ignore
					}
				)
				tmp.append(df_tmp)

	df_concat = pd.concat(tmp).reset_index(drop=True)
	df_concat['data_row'] = df_concat.index

	print(gpx)
# data = reader.read_gpx_data(TEST_FILE_PATH)

# with open(TEST_FILE_PATH, 'r', encoding="utf-8") as gpx_file:
#	gpx = gpxpy.parse(gpx_file)

# print(type(gpx.tracks[0]))
# print(gpx.tracks[0].segments[0])
