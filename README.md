# gpx-etl
Parse, transform, process and create statistics from gpx files in DataFrame
formats.

## What's it good for
- GPX files is a unified format that contain GPS coordinate information in a 
xml schema 
- The aim is to create a lightweight python library that allows to load and 
transform gpx files to a time series pandas DataFrame format with gps
coordinates and labeled metrics e.g. distances, speed, altitude gain and loss
etc. It is intended for developers or data scientists that prefer tabular data
- Parsing and some calculations use the amazing
[gpxpy - GPX file parser](https://github.com/tkrajina/gpxpy) library


## Poetry
### Install Dependencies From pyproject.toml
- Install dependencies `poetry install`
### Activate Venv and Set Up in IDE
- Get path to venv `poetry env info --path`
- Activate venv using `{path_to_venv}\Scripts\activate.bat`
- In PyCharm, go to File -> Settings -> Project -> Python Interpreter -> Add
- Add new system interpreter and set dir to `{path_to_venv}\Scripts\python.exe`
- If not configured automatically, go to run configurations and select venv
interpreter