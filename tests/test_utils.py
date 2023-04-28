from datetime import datetime, timedelta

def add_sec(start_time: datetime, seconds: int) -> datetime:
	for i in range(0, seconds):
		start_time = start_time + timedelta(seconds=1)
	return start_time