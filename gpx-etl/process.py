import logging
from typing import List, Dict
import pandas as pd
import reader

class GPXTransformer:
	def __init__(self, path: str):
		self.gpx = reader.load_gpx(path)
		self.converter = reader.GPXDataFrameConverter(self.gpx)
		self.df_meta = self.converter.get_metadata
		self.df_gpx = self.converter.get_track_points

	def label_distances(self):
		pass

	def label_speed(self):
		pass
