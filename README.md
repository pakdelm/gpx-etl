# gpx-etl
Parse, transform, process and create statistics from gpx files.

## Poetry
### Install Dependencies From pyproject.toml
- Install dependencies `poetry install`
- Create a poetry.lock file `poetry lock`
### Activate Venv and Set Up in IDE
- Get path to venv `poetry env info --path`
- Activate venv using `{path_to_venv}\Scripts\activate.bat`
- In PyCharm, go to File -> Settings -> Project -> Python Interpreter -> Add
- Add new system interpreter and set dir to `{path_to_venv}\Scripts\python.exe`
- If not configured automatically, go to run configurations and select venv interpreter