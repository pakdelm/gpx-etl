"""
GPXDataFrameConverter converts GPX xml to tabular data in pandas DataFrame
format
"""

import logging
from utils import COLS, METADATA_SCHEMA

import pandas as pd
import gpxpy

from typing import List, Dict

logging.basicConfig(
	level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GPXDataFrameConverter:
	def __init__(self, gpx: gpxpy.gpx.GPX):
		"""

        :type gpx: object
        """
		self.gpx = gpx

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
			self.gpx.schema_locations,
		]

		metadata_map: Dict[str, List[str]] = dict(
			zip(METADATA_SCHEMA, [[v] for v in metadata_values])
		)

		df_metadata = pd.DataFrame(metadata_map)

		return df_metadata

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
							COLS.track_name: [track.name],
							COLS.segment_index: [index],
							COLS.longitude: [point.longitude],
							COLS.latitude: [point.latitude],
							COLS.elevation: [point.elevation],
							COLS.timestamp: [
								point.time.replace(  # type: ignore
									tzinfo=None, microsecond=0
								)
							],
						}
					)
					tmp.append(df_tmp)

		df_concat = pd.concat(tmp).reset_index(drop=True)

		logging.debug(f"GPX file converted to DataFrame: {df_concat.head()}")

		return df_concat
