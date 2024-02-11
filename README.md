# gpx-etl - Transform GPX files to DataFrame
- ⚡ Parse, transform and create statistics from GPX files to pandas DataFrame format.
- 📡 GPX files contain GPS coordinates, elevation and metadata.
- 📊 Create track statistics e.g. distances, speed, altitude gain and loss and more.
- ✨ Easy usage to analyze and convert your own GPX data 
- 💖 Parsing and distance calculations use the amazing
[gpxpy - GPX file parser](https://github.com/tkrajina/gpxpy) library

🚨 gpx-etl is still in pre-release. The API is not yet stable and might change with next releases. 
Some GPX file versions might still lack compatibility. If you notice an issue, please raise an [Issue](https://github.com/pakdelm/gpx-etl/issues).

## 🔨 Installation

```shell
pip install gpx-etl
```

## 💡 Usage

Sample GPX file was used from [GitHub sample-gpx](https://github.com/gps-touring/sample-gpx/blob/master/RoscoffCoastal/Trebeurden_Lannion_parcours13.2RE.gpx).

### Transform to time series DataFrame
```python
from gpx_etl.transform import GPXTransformer

gpx_etl = GPXTransformer.from_file("path/to/gpx_file.gpx")
df_gpx = gpx_etl.to_dataframe

print(df_gpx.head())

"""
                    track_name  segment_index  longitude   latitude  elevation           timestamp   distance  total_distance  delta_t       min_timestamp       max_timestamp    duration      speed  min_speed  max_speed  mean_speed  delta_elevation  altitude_gain  altitude_loss  min_elevation  max_elevation  total_altitude_gain  total_altitude_loss author_email author_link author_link_text author_link_type                                             bounds copyright_author copyright_license copyright_year           creator description                   link             link_text link_type  name             time_metadata version                                   schema_locations
0  Trebeurden_Lannion_parcours              0  -3.562515  48.766598       75.6 2013-03-08 09:05:06   8.480550     13430.34966     64.0 2013-03-08 09:05:06 2013-03-08 11:06:01  120.916667   0.477031   0.060992  37.283963   15.123259             -2.4            0.0           -2.4            8.3          107.3                186.3               -252.6         None        None             None             None  <gpxpy.gpx.GPXBounds object at 0x000001A895209...             None              None           None  MapSource 6.16.3        None  http://www.garmin.com  Garmin International      None  None 2013-06-11 10:06:11+00:00     1.1  [http://www.topografix.com/GPX/1/1, http://www...
1  Trebeurden_Lannion_parcours              0  -3.562400  48.766602       73.2 2013-03-08 09:06:10   3.532892     13430.34966     11.0 2013-03-08 09:05:06 2013-03-08 11:06:01  120.916667   1.156219   0.060992  37.283963   15.123259              0.5            0.5            0.0            8.3          107.3                186.3               -252.6         None        None             None             None  <gpxpy.gpx.GPXBounds object at 0x000001A895209...             None              None           None  MapSource 6.16.3        None  http://www.garmin.com  Garmin International      None  None 2013-06-11 10:06:11+00:00     1.1  [http://www.topografix.com/GPX/1/1, http://www...
2  Trebeurden_Lannion_parcours              0  -3.562352  48.766606       73.7 2013-03-08 09:06:21  38.713129     13430.34966     10.0 2013-03-08 09:05:06 2013-03-08 11:06:01  120.916667  13.936726   0.060992  37.283963   15.123259             -0.5            0.0           -0.5            8.3          107.3                186.3               -252.6         None        None             None             None  <gpxpy.gpx.GPXBounds object at 0x000001A895209...             None              None           None  MapSource 6.16.3        None  http://www.garmin.com  Garmin International      None  None 2013-06-11 10:06:11+00:00     1.1  [http://www.topografix.com/GPX/1/1, http://www...
3  Trebeurden_Lannion_parcours              0  -3.561826  48.766632       73.2 2013-03-08 09:06:31  29.815679     13430.34966     20.0 2013-03-08 09:05:06 2013-03-08 11:06:01  120.916667   5.366822   0.060992  37.283963   15.123259              0.0            0.0            0.0            8.3          107.3                186.3               -252.6         None        None             None             None  <gpxpy.gpx.GPXBounds object at 0x000001A895209...             None              None           None  MapSource 6.16.3        None  http://www.garmin.com  Garmin International      None  None 2013-06-11 10:06:11+00:00     1.1  [http://www.topografix.com/GPX/1/1, http://www...
4  Trebeurden_Lannion_parcours              0  -3.561422  48.766605       73.2 2013-03-08 09:06:51  27.471280     13430.34966     14.0 2013-03-08 09:05:06 2013-03-08 11:06:01  120.916667   7.064043   0.060992  37.283963   15.123259             -3.8            0.0           -3.8            8.3          107.3                186.3               -252.6         None        None             None             None  <gpxpy.gpx.GPXBounds object at 0x000001A895209...             None              None           None  MapSource 6.16.3        None  http://www.garmin.com  Garmin International      None  None 2013-06-11 10:06:11+00:00     1.1  [http://www.topografix.com/GPX/1/1, http://www...
5  ...
"""
```

### Create aggregated track statistics

```python
from gpx_etl.transform import GPXTransformer

gpx_etl = GPXTransformer.from_file("path/to/gpx_file.gpx")
df_stats = gpx_etl.stats

print(df_stats.head())
"""
                        track_name  segment_index       min_timestamp       max_timestamp    duration  total_distance  min_speed  max_speed  mean_speed  min_elevation  max_elevation  total_altitude_gain  total_altitude_loss
0      Trebeurden_Lannion_parcours              0 2013-03-08 09:05:06 2013-03-08 11:06:01  120.916667    13430.349660   0.060992  37.283963   15.123259            8.3          107.3                186.3               -252.6
254  Trebeurden_Lannion_sensunique              0 2013-03-08 10:49:56 2013-03-08 10:52:01    2.083333      262.661056   0.528312  17.186635   11.522572           48.7           51.1                  4.3                 -4.3
"""
```

### Extract metadata
```python
from gpx_etl.transform import GPXTransformer

gpx_etl = GPXTransformer.from_file("path/to/gpx_file.gpx")
df_meta = gpx_etl.metadata

print(df_meta.head())
"""
  author_email author_link author_link_text author_link_type                                             bounds copyright_author copyright_license copyright_year           creator description                   link             link_text link_type  name             time_metadata version                                   schema_locations
0         None        None             None             None  <gpxpy.gpx.GPXBounds object at 0x0000027ED3A88...             None              None           None  MapSource 6.16.3        None  http://www.garmin.com  Garmin International      None  None 2013-06-11 10:06:11+00:00     1.1  [http://www.topografix.com/GPX/1/1, http://www...
"""
```