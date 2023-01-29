import logging
from typing import List
import pandas as pd

from utils import COLS

import gpxpy
from gpxpy.geo import haversine_distance

import convert

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ORDER_BY_COL = [COLS.timestamp]
TRACK_PARTITIONS = [COLS.track_name, COLS.segment_index]


class GPXDataFrameTransformer:
	def __init__(self, gpx: gpxpy.gpx.GPX):
		self.gpx = gpx
		self.converter = convert.GPXDataFrameConverter(self.gpx)

	def enrich_metadata(self) -> pd.DataFrame:
		return self.converter.get_track_points().merge(self.converter.get_metadata(), how="cross")

	@classmethod
	def label_distances(cls, df: pd.DataFrame) -> pd.DataFrame:
		lead_long: str = f"lead_{COLS.longitude}"
		lead_lat: str = f"lead_{COLS.latitude}"

		df_lead = _lead_by_partition(df, COLS.longitude, ORDER_BY_COL, TRACK_PARTITIONS)
		df_lead = _lead_by_partition(df_lead, COLS.latitude, ORDER_BY_COL, TRACK_PARTITIONS)

		df_lead[COLS.distance] = df_lead.apply(
			lambda x: gpxpy.geo.haversine_distance(
				latitude_1=x[COLS.latitude],
				longitude_1=x[COLS.longitude],
				latitude_2=x[lead_lat],
				longitude_2=x[lead_long]
			),
			axis=1
		)

		return df_lead.drop(columns=[lead_long, lead_lat])

	def label_speed(self):
		pass

	def label_time_diff(self):
		pass

	def label_alt_gain_loss(self):
		pass


def _lead_by_partition(df: pd.DataFrame, col: str, order_by: List[str], partitions: List[str]) -> pd.DataFrame:
	lead_col: str = f"lead_{col}"

	df[lead_col] = df.sort_values(by=order_by, ascending=True).groupby(partitions)[col].shift(-1)

	return df
