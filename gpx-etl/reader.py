"""
Functions to parse gpx files
"""
import logging
from typing import List, Dict
import pandas as pd
import gpxpy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

METADATA_SCHEMA = [
	"author_email",
	"author_link",
	"author_link_text",
	"author_link_type",
	"bounds",
	"copyright_author",
	"copyright_license",
	"copyright_year",
	"creator",
	"description",
	"link",
	"link_text",
	"link_type",
	"name",
	"time",
	"version",
	'schema_locations'
]

def load_gpx(path: str) -> gpxpy.gpx.GPX:
	with open(path, 'r', encoding="utf-8") as gpx_file:
		gpx = gpxpy.parse(gpx_file)

	return gpx


class GPXDataFrameConverter:
	def __init__(self, gpx: gpxpy.gpx.GPX):
		self.gpx = gpx

	@property
	def get_metadata(self) -> pd.DataFrame:

		metadata_values: List = [
			self.gpx.author_email,
			self.gpx.author_link,
			self.gpx.author_link_text,
			self.gpx.author_link_type,
			self.gpx.bounds,
			self.gpx.copyright_author,
			self.gpx.copyright_license,
			self.gpx.copyright_year,
			self.gpx.creator,
			self.gpx.description,
			self.gpx.link,
			self.gpx.link_text,
			self.gpx.link_type,
			self.gpx.name,
			self.gpx.time,
			self.gpx.version,
			self.gpx.schema_locations
		]

		metadata_map: Dict[str, List[str]] = dict(zip(METADATA_SCHEMA, [[v] for v in metadata_values]))

		df_metadata = pd.DataFrame(metadata_map)

		return df_metadata

	@property
	def get_track_points(self) -> pd.DataFrame:
		tmp = []
		for track in self.gpx.tracks:
			logging.info(f"Track name: {track.name}")

			for index, segment in enumerate(track.segments):
				logging.info(f"Segment index: {index}")
				logging.debug(f"Segment: {segment}")

				for point in segment.points:
					logging.debug(f"Track point: {point}")

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

		logging.debug(f"GPX file converted to DataFrame: {df_concat.head()}")

		return df_concat
