"""GPXDataFrameConverter converts GPX xml to tabular data to pandas DataFrames.

This module converts gpx data and returns metadata and track points as pandas
DataFrames.
"""
from typing import List, Dict
import logging
from utils import COLS, LOG_FORMAT, METADATA_SCHEMA

import pandas as pd
import gpxpy

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
# logger.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)



class GPXDataFrameConverter:
    """This class converts gpx data and returns metadata and track points."""

    def __init__(self, gpx: gpxpy.gpx.GPX):
        """Instantiate class with gpx data."""
        self.gpx = gpx

    def get_metadata(self) -> pd.DataFrame:
        """Return pandas DataFrame with metadata from gpx data."""
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
        """Return time series pandas DataFrame converted from gpx data.

        Rows will be labeled by track_name and segment_index that originates
        from gpx xml structure. Data schema as columns: track_name,
        segment_index, longitude, latitude, elevation, timestamp.
        """
        tmp = []
        for track in self.gpx.tracks:
            logger.info(f"Track name: {track.name}")

            for index, segment in enumerate(track.segments):
                logger.info(f"Segment index: {index}")
                logger.debug(f"Segment: {segment}")

                for point in segment.points:
                    logger.debug(f"Track point: {point}")

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

        logger.debug(f"GPX file converted to DataFrame: {df_concat.head()}")

        return df_concat
