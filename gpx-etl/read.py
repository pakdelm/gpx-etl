"""
Functions to read gpx files or xml
"""

from typing import AnyStr
import gpxpy


def read_gpx_file(path: str) -> gpxpy.gpx.GPX:
	with open(path, 'r', encoding="utf-8") as gpx_file:
		gpx = gpxpy.parse(gpx_file)

	return gpx


def read_gpx_xml(xml: AnyStr) -> gpxpy.gpx.GPX:
	gpx = gpxpy.parse(xml)

	return gpx
