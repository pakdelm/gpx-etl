"""
Functions to parse gpx files
"""
from typing import List, Dict
import pandas as pd
import gpxpy

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


class DataFrameConverter:
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

	def get_track_points(self) -> pd.DataFrame:
		self.gpx

def read_gpx_data(path: str) -> List[gpxpy.gpx.GPX]:
	"""
    Parse gpx data from file path
    :param path: Path to gpx file
    :return: GPXTrackPoint class containing elements of gps coordinate information
    """
	with open(path, 'r', encoding="utf-8") as gpx_file:
		gpx = gpxpy.parse(gpx_file)

	return gpx
