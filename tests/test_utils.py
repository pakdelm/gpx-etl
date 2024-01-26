from datetime import datetime, timedelta
from typing import List

from gpxpy.gpx import GPX, GPXTrack, GPXTrackPoint, GPXTrackSegment

TRACK_NAME_DEFAULT = "test_track"
START_TIME_DEFAULT = datetime(2023, 1, 1, 0, 0, 0)


def generate_gpx_data(
    track_points: List[GPXTrackPoint],
    track_name: str = TRACK_NAME_DEFAULT,
    start_time: datetime = START_TIME_DEFAULT,
) -> GPX:
    gpx = GPX()
    gpx.tracks.append(GPXTrack(name=track_name))
    gpx.tracks[0].segments.append(GPXTrackSegment())

    for second, track_point in enumerate(track_points):
        gpx.tracks[0].segments[0].points.append(
            GPXTrackPoint(
                latitude=track_point.latitude,
                longitude=track_point.longitude,
                elevation=track_point.elevation,
                time=_add_sec(start_time, second),
            )
        )

    return gpx


def _add_sec(start_time: datetime, seconds: int) -> datetime:
    for i in range(0, seconds):
        start_time = start_time + timedelta(seconds=1)
    return start_time
