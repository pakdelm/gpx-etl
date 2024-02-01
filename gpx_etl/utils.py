"""
Utils contains data structures for DataFrame columns and gpx schema
"""

from dataclasses import dataclass

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


@dataclass
class Columns:
    track_name: str
    segment_index: str
    longitude: str
    latitude: str
    elevation: str
    timestamp: str
    author_email: str
    author_link: str
    author_link_text: str
    author_link_type: str
    bounds: str
    copyright_author: str
    copyright_license: str
    copyright_year: str
    creator: str
    description: str
    link: str
    link_text: str
    link_type: str
    name: str
    time_metadata: str
    version: str
    schema_locations: str
    distance: str
    total_distance: str
    delta_t: str
    speed: str
    min_speed: str
    max_speed: str
    mean_speed: str
    delta_elevation: str
    altitude_gain: str
    altitude_loss: str
    min_elevation: str
    max_elevation: str
    total_altitude_gain: str
    total_altitude_loss: str
    min_timestamp: str
    max_timestamp: str
    duration: str


COLS = Columns(
    "track_name",
    "segment_index",
    "longitude",
    "latitude",
    "elevation",
    "timestamp",
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
    "time_metadata",
    "version",
    "schema_locations",
    "distance",
    "total_distance",
    "delta_t",
    "speed",
    "min_speed",
    "max_speed",
    "mean_speed",
    "delta_elevation",
    "altitude_gain",
    "altitude_loss",
    "min_elevation",
    "max_elevation",
    "total_altitude_gain",
    "total_altitude_loss",
    "min_timestamp",
    "max_timestamp",
    "duration",
)

METADATA_SCHEMA = [
    COLS.author_email,
    COLS.author_link,
    COLS.author_link_text,
    COLS.author_link_type,
    COLS.bounds,
    COLS.copyright_author,
    COLS.copyright_license,
    COLS.copyright_year,
    COLS.creator,
    COLS.description,
    COLS.link,
    COLS.link_text,
    COLS.link_type,
    COLS.name,
    COLS.time_metadata,
    COLS.version,
    COLS.schema_locations,
]
