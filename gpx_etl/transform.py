"""GPXTransformer converts gpx data to tabular data format.

This module converts gpx data and returns metadata and track points as pandas
DataFrames.
"""
import logging
from typing import AnyStr, Dict, List
from functools import cached_property
import gpxpy
import numpy as np
import pandas as pd
from gpxpy.geo import haversine_distance
from gpxpy.gpx import GPX
from pandas import DataFrame

from gpx_etl.utils import COLS, METADATA_SCHEMA

logger = logging.getLogger(__name__)

ORDER_BY_COL = [COLS.timestamp]
TRACK_PARTITIONS = [COLS.track_name, COLS.segment_index]


class GPXTransformer:
    """This class converts gpx data and returns metadata and track points."""

    def __init__(self, gpx: GPX) -> None:
        """Instantiate class with gpx data."""
        self._gpx = gpx

    @property
    def gpx(self):
        return self._gpx

    @cached_property
    def to_dataframe(self):
        return self.transform()

    @classmethod
    def from_file(cls, path: str):
        """Return GPXTransformer object from .gpx file path."""
        with open(path, "r", encoding="utf-8") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        return cls(gpx)

    @classmethod
    def from_xml(cls, xml: AnyStr):
        """Return GPXTransformer object from xml."""
        gpx = gpxpy.parse(xml)
        return cls(gpx)

    def convert(self, with_metadata: bool = True) -> DataFrame:
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

    def transform(self, with_metadata: bool = True) -> DataFrame:
        """Transform gpx data to DataFrame format and label metrics."""
        df = (
            self.convert(with_metadata=with_metadata)
            .pipe(self._label_distance)
            .pipe(self._label_total_distance)
            .pipe(self._label_time_diff)
            .pipe(self._label_time_metrics)
            .pipe(self._label_speed)
            .pipe(self._label_speed_metrics)
            .pipe(self._label_alt_gain_loss)
            .pipe(self._label_altitude_metrics)
        )
        return df

    @property
    def stats(self) -> DataFrame:
        """Return aggregated statistics of gpx data."""
        df = self.to_dataframe[
            [
                COLS.track_name,
                COLS.segment_index,
                COLS.min_timestamp,
                COLS.max_timestamp,
                COLS.duration,
                COLS.total_distance,
                COLS.min_speed,
                COLS.max_speed,
                COLS.mean_speed,
                COLS.min_elevation,
                COLS.max_elevation,
                COLS.total_altitude_gain,
                COLS.total_altitude_loss,
            ]
        ].drop_duplicates()

        return df

    def _get_metadata(self) -> DataFrame:
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

        df_metadata = DataFrame(metadata_map)

        return df_metadata

    def _get_track_points(self) -> DataFrame:
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

                    df_tmp = DataFrame(
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

    def _label_distance(self, df: DataFrame) -> DataFrame:
        lead_long: str = f"lead_{COLS.longitude}"
        lead_lat: str = f"lead_{COLS.latitude}"

        df_lead = self._lead_by_partition(df, COLS.longitude, ORDER_BY_COL, TRACK_PARTITIONS)
        df_lead = self._lead_by_partition(df_lead, COLS.latitude, ORDER_BY_COL, TRACK_PARTITIONS)

        df_lead[COLS.distance] = df_lead.apply(
            lambda x: haversine_distance(
                latitude_1=x[COLS.latitude],
                longitude_1=x[COLS.longitude],
                latitude_2=x[lead_lat],
                longitude_2=x[lead_long],
            ),
            axis=1,
        )

        df_distance = df_lead.drop(columns=[lead_long, lead_lat])

        return df_distance

    def _label_time_diff(self, df: DataFrame) -> DataFrame:
        """Label time delta between timestamps."""
        lead_ts: str = f"lead_{COLS.timestamp}"

        df_lead = self._lead_by_partition(df, COLS.timestamp, ORDER_BY_COL, TRACK_PARTITIONS)

        df_lead[COLS.delta_t] = df_lead[lead_ts] - df_lead[COLS.timestamp]
        df_lead[COLS.delta_t] = df_lead[COLS.delta_t] / pd.Timedelta(seconds=1)  # type: ignore

        df_time_diff = df_lead.drop(columns=[lead_ts])

        return df_time_diff

    def _label_alt_gain_loss(self, df: DataFrame) -> DataFrame:
        """Label elevation difference and alt gain and loss.

        Calculate altitude gain and loss. Sum to get total gain and loss in meters. Note: alt_dif
        col might be misleading as negative differences for n-1 indicate alt gain and vice verca.
        """
        lead_elevation: str = f"lead_{COLS.elevation}"

        df_lead = self._lead_by_partition(df, COLS.elevation, ORDER_BY_COL, TRACK_PARTITIONS)

        df_lead[COLS.delta_elevation] = df_lead[lead_elevation] - df_lead[COLS.elevation]

        df_lead[COLS.altitude_gain] = np.where(
            df_lead[COLS.delta_elevation] > 0, df_lead[COLS.delta_elevation], 0
        )
        df_lead[COLS.altitude_loss] = np.where(
            df_lead[COLS.delta_elevation] < 0, df_lead[COLS.delta_elevation], 0
        )

        df_alt = df_lead.drop(columns=[lead_elevation])

        return df_alt

    @staticmethod
    def _label_speed(df: DataFrame) -> DataFrame:
        """Label speed in km per hour."""
        df[COLS.speed] = (df[COLS.distance] / df[COLS.delta_t]) * 3.6

        return df

    def _label_total_distance(self, df: DataFrame) -> DataFrame:
        """Label total distance in meters (m) partitioned by track name and segments index."""
        agg_func = "sum"
        df_agg = self._aggregate_by_partition(
            df, COLS.distance, ORDER_BY_COL, TRACK_PARTITIONS, agg_func
        )
        df_agg = df_agg.rename(columns={f"{agg_func}_{COLS.distance}": f"total_{COLS.distance}"})

        return df_agg

    def _label_speed_metrics(self, df: DataFrame) -> DataFrame:
        """Label min, max, mean speed km per hour partitioned by track name and segments index."""
        agg_funcs = ["min", "max", "mean"]

        for func in agg_funcs:
            df = self._aggregate_by_partition(df, COLS.speed, ORDER_BY_COL, TRACK_PARTITIONS, func)

        return df

    def _label_altitude_metrics(self, df: DataFrame) -> DataFrame:
        """Label min, max elevation and total altitude gain/loss in meters."""
        agg_funcs = ["min", "max"]
        agg_cols = [COLS.altitude_gain, COLS.altitude_loss]

        for func in agg_funcs:
            df = self._aggregate_by_partition(
                df, COLS.elevation, ORDER_BY_COL, TRACK_PARTITIONS, func
            )

        for col in agg_cols:
            df = self._aggregate_by_partition(df, col, ORDER_BY_COL, TRACK_PARTITIONS, "sum")

        df_agg = df.rename(
            columns={
                f"sum_{COLS.altitude_gain}": f"total_{COLS.altitude_gain}",
                f"sum_{COLS.altitude_loss}": f"total_{COLS.altitude_loss}",
            }
        )

        return df_agg

    def _label_time_metrics(self, df: DataFrame) -> DataFrame:
        """Label min, max timestamps and duration in minutes."""
        agg_funcs = ["min", "max"]
        delta_t_col_name = f"sum_{COLS.delta_t}"

        for func in agg_funcs:
            df = self._aggregate_by_partition(
                df, COLS.timestamp, ORDER_BY_COL, TRACK_PARTITIONS, func
            )

        df[COLS.duration] = (df[COLS.max_timestamp] - df[COLS.min_timestamp]) / pd.Timedelta(
            minutes=1
        )

        return df

    @staticmethod
    def _lead_by_partition(
            df: DataFrame, col: str, order_by: List[str], partitions: List[str]
    ) -> DataFrame:
        """Return DataFrame with shifted values by 1 by partitions and order.

        Create extra column "lead_" + input col name.
        """
        lead_col: str = f"lead_{col}"

        df[lead_col] = (
            df.sort_values(by=order_by, ascending=True).groupby(partitions)[col].shift(-1)
        )

        return df

    @staticmethod
    def _aggregate_by_partition(
            df: DataFrame, col: str, order_by: List[str], partitions: List[str], func: str
    ) -> DataFrame:
        """Return DataFrame with aggregated values over partitions."""
        agg_col: str = f"{func}_{col}"

        df[agg_col] = (
            df.sort_values(by=order_by, ascending=True).groupby(partitions)[col].transform(func)
        )

        return df
