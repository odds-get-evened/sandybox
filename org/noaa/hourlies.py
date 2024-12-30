import os.path
from pathlib import Path

import pandas as pd

"""
README for climate normals
https://www.ncei.noaa.gov/pub/data/normals/1981-2010/readme.txt

for converting text files to CSV from Unix command line
$ awk '{
    $1=$1  # trim leading and trailing whitespace
    for(i=1; i <= NF; i++) {  # loop thru all fields
        gsub(/"/, "\"\"", $i)  # escape double-quotes by replacing " with ""
        $i = "\"" $i "\""  # enclose all fields in double-quotes
    }
    print $0
}' hly-temp-normal.txt > hly-temp-normal.csv
"""

home_dir = os.path.expanduser('~')
# average temperature data
HOURLY_TEMPS_CSV = Path(home_dir, '.databox', 'noaa', 'normals', 'hourly', 'hly-temp-normal.csv')
# list of all stations providing hourly data
HOURLY_STATIONS_CSV = Path(home_dir, '.databox', 'noaa', 'normals', 'hourly', 'hly-inventory.csv')


def process_hourly_temps():
    df = pd.read_csv(HOURLY_TEMPS_CSV, header=None)

    stn_df = pd.read_csv(HOURLY_STATIONS_CSV, header=None)
    print(stn_df)


def main():
    process_hourly_temps()


if __name__ == "__main__":
    main()
