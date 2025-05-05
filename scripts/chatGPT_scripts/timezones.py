import datetime
import pytz
from concurrent.futures import ThreadPoolExecutor

# Get all time zones
all_timezones = pytz.country_timezones("US")

def print_time_in_timezone(timezone):
    # Get the current time in the given timezone
    tz = pytz.timezone(timezone)
    current_time = datetime.datetime.now(tz)
    # Print the timezone and current time
    print(f"{timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Create a thread pool to execute the print_time_in_timezone function for each timezone concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(print_time_in_timezone, all_timezones)