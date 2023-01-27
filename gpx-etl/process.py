import logging
from typing import List, Dict
import pandas as pd
import gpxpy
from gpxpy.geo import haversine_distance

import convert

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class GPXDataFrameTransformer:
	def __init__(self, gpx: gpxpy.gpx.GPX):
		self.gpx = gpx
		self.converter = convert.GPXDataFrameConverter(self.gpx)

	def enrich_metadata(self) -> pd.DataFrame:

		return self.converter.get_track_points().merge(self.converter.get_metadata(), how="cross")

	@classmethod
	def label_distances(cls, df: pd.DataFrame) -> pd.DataFrame:

		# df = df.sort_values(by=['Time'], ascending=True)

		df['lead_longitude'] = df['longitude'].shift(-1)
		df['lead_latitude'] = df['latitude'].shift(-1)

		df["distance"] = df.apply(
			lambda x: gpxpy.geo.haversine_distance(
				latitude_1=x.latitude,
				longitude_1=x.longitude,
				latitude_2=x.lead_latitude,
				longitude_2=x.lead_latitude
			),
			axis=1
		)

		return df

	def label_speed(self):
		pass
