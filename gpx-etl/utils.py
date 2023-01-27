from dataclasses import dataclass


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
	"schema_locations"
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
	COLS.schema_locations
]