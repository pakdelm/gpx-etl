"""GPXDataFrameConverter converts GPX xml to tabular data to pandas DataFrames.

This module converts gpx data and returns metadata and track points as pandas
DataFrames.
"""
import logging
from typing import Dict, List

import gpxpy
import numpy as np
import pandas as pd
from gpx_etl.utils import COLS, METADATA_SCHEMA

logger = logging.getLogger(__name__)

ORDER_BY_COL = [COLS.timestamp]
TRACK_PARTITIONS = [COLS.track_name, COLS.segment_index]


class GPXTransformer:
    """This class converts gpx data and returns metadata and track points."""

    def __init__(self, gpx: gpxpy.gpx.GPX):
        """Instantiate class with gpx data."""
        self.gpx = gpx

    def convert(self, with_metadata: bool = True) -> pd.DataFrame:
        """Convert gpx data to DataFrame format.

        :param with_metadata: If true, enrich time series DataFrame with
        metadata columns from the gpx xml. If false, return time series
        DataFrame only.
        :return: Return converted DataFrame with time series gpx data.
        """
        df_track_points = self._get_track_points()
        if with_metadata:
            return df_track_points.merge(self._get_metadata(), how="cross")
        else:
            return df_track_points

    def transform(self, with_metadata: bool = True) -> pd.DataFrame:
        """Transform all"""
        df = (
            self.convert(with_metadata=with_metadata)
            .pipe(self._label_distance)
            .pipe(self._label_time_diff)
            .pipe(self._label_speed)
            .pipe(self._label_alt_gain_loss)
        )
        return df

    def _get_metadata(self) -> pd.DataFrame:
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

    def _get_track_points(self) -> pd.DataFrame:
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
                                point.time.replace(tzinfo=None, microsecond=0)  # type: ignore
                            ],
                        }
                    )
                    tmp.append(df_tmp)

        df_concat = pd.concat(tmp).reset_index(drop=True)

        logger.debug(f"GPX file converted to DataFrame: {df_concat.head()}")

        return df_concat

    def _label_distance(self, df: pd.DataFrame) -> pd.DataFrame:
        lead_long: str = f"lead_{COLS.longitude}"
        lead_lat: str = f"lead_{COLS.latitude}"

        df_lead = self.__lead_by_partition(df, COLS.longitude, ORDER_BY_COL, TRACK_PARTITIONS)
        df_lead = self.__lead_by_partition(df_lead, COLS.latitude, ORDER_BY_COL, TRACK_PARTITIONS)

        df_lead[COLS.distance] = df_lead.apply(
            lambda x: gpxpy.geo.haversine_distance(
                latitude_1=x[COLS.latitude],
                longitude_1=x[COLS.longitude],
                latitude_2=x[lead_lat],
                longitude_2=x[lead_long],
            ),
            axis=1,
        )

        return df_lead.drop(columns=[lead_long, lead_lat])

    def _label_time_diff(self, df: pd.DataFrame) -> pd.DataFrame:
        """Label time delta between timestamps."""
        lead_ts: str = f"lead_{COLS.timestamp}"

        df_lead = self.__lead_by_partition(df, COLS.timestamp, ORDER_BY_COL, TRACK_PARTITIONS)

        df_lead[COLS.delta_t] = df_lead[lead_ts] - df_lead[COLS.timestamp]
        df_lead[COLS.delta_t] = df_lead[COLS.delta_t] / pd.Timedelta(seconds=1)  # type: ignore

        return df_lead

    def _label_alt_gain_loss(self, df: pd.DataFrame) -> pd.DataFrame:
        """Label elevation difference and alt gain and loss.

        TODO: Test logic
        Calculate altitude gain and loss. Sum to get total gain and loss in meters. Note: alt_dif
        col might be misleading as negative differences for n-1 indicate alt gain and vice verca.
        """
        lead_elevation: str = f"lead_{COLS.elevation}"

        df_lead = self.__lead_by_partition(df, COLS.elevation, ORDER_BY_COL, TRACK_PARTITIONS)

        df_lead[COLS.delta_elevation] = df_lead[lead_elevation] - df_lead[COLS.elevation]

        df_lead[COLS.altitude_gain] = np.where(
            df_lead[COLS.delta_elevation] > 0, df_lead[COLS.delta_elevation], 0
        )
        df_lead[COLS.altitude_loss] = np.where(
            df_lead[COLS.delta_elevation] < 0, df_lead[COLS.delta_elevation], 0
        )

        return df_lead

    @staticmethod
    def _label_speed(df: pd.DataFrame) -> pd.DataFrame:
        """Label speed in km/h."""
        df[COLS.speed] = (df[COLS.distance] / df[COLS.delta_t]) * 3.6

        return df

    def _label_total_distance(self):
        """TODO: How to partition over segments"""
        pass

    def _label_average_speed(self):
        """TODO: How to partition over segments"""
        pass

    @staticmethod
    def __lead_by_partition(
        df: pd.DataFrame, col: str, order_by: List[str], partitions: List[str]
    ) -> pd.DataFrame:
        """Return DataFrame with shifted values by 1 by partitions and order.

        Create extra column "lead_" + input col name.
        """
        lead_col: str = f"lead_{col}"

        df[lead_col] = (
            df.sort_values(by=order_by, ascending=True).groupby(partitions)[col].shift(-1)
        )

        return df
