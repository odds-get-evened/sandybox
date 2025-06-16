import os.path
import warnings
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

# surpress weird deprecation notice i think from BeautifulSoup
warnings.filterwarnings('ignore', category=DeprecationWarning)

BASE_URL = "https://www.ncei.noaa.gov/data/normals-hourly/2006-2020/access/"

OUTPUT_DIR = Path.home().joinpath('.databox', 'noaa', 'wx', 'normals_hourly')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_csv_links(index_url: str):
    resp = requests.get(index_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    return [
        urljoin(index_url, a['href'])
        for a in soup.find_all('a', href=True)
        if a['href'].lower().endswith('.csv')
    ]

def download_one(url: str, save_dir: Path):
    fn = save_dir.joinpath(os.path.basename(url))

    if fn.exists():
        return f"skipped {fn.name}"

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        total_bytes = int(r.headers.get('Content-Length', 0))
        num_downloaded = 0

        print(f"{fn.name}: starting download ({total_bytes} bytes)")

        with open(fn, 'wb') as fh:
            for chunk in r.iter_content(8192):
                fh.write(chunk)
                num_downloaded += len(chunk)
                print(f"{fn.name}: {num_downloaded}/{total_bytes} bytes", end="\r")

        print()

    return f"downloaded {fn.name}"


def do_download(index_url: str, save_dir: Path, workers: int = 5):
    lnx = fetch_csv_links(index_url)
    total_files = len(lnx)
    print(f"found {total_files} CSVs, downloading with {workers} workers...\n")

    completed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(download_one, link, save_dir): link
            for link in lnx
        }

        for fut in as_completed(futures):
            result = fut.result()
            completed += 1
            print(f"[{completed}/{total_files} {result}")

    print("\nall done.")

def proc_csv(f: Path, dest: Path):
    pd.set_option('display.max_columns', None)
    if not f.suffix.__eq__('.csv'):
        raise ValueError("invalid file type. must be CSV format")

    df = pd.read_csv(f)
    col_want = [
        'STATION', 'LATITUDE', 'LONGITUDE',
        'ELEVATION', 'DATE', 'HLY-TEMP-NORMAL',
        'HLY-DEWP-NORMAL', 'HLY-PRES-NORMAL',
        'HLY-HIDX-NORMAL', 'HLY-WCHL-NORMAL',
        'HLY-WIND-AVGSPD', 'HLY-WIND-VCTDIR',
        'HLY-WIND-VCTSPD'

    ]
    df = df[col_want]
    df = df[col_want]
    y = df['HLY-TEMP-NORMAL']
    X = df.drop(columns=['HLY-TEMP-NORMAL', 'STATION'])
    # split into train/test
    X_train, X_test, y_train, y_test = train_test_split()

def do_training(model_path: Path, csv_path: Path, num_workers: int = 3):
    if not model_path.exists():
        model_path.mkdir(parents=True, exist_ok=True)

    csvs = csv_path.glob("*.csv")
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        futes = [
            ex.submit(proc_csv, csv, model_path)
            for csv in csvs
        ]

def main():
    '''
    do_download(BASE_URL, OUTPUT_DIR, workers=10)
    do_training(
        OUTPUT_DIR.joinpath('models'),
        OUTPUT_DIR
    )
    '''
    proc_csv(
        Path.home().joinpath('.databox', 'noaa', 'wx', 'normals_hourly', 'AQW00061705.csv'),
        Path.home().joinpath('.databox', 'noaa', 'wx', 'normals_hourly', 'models')
    )


if __name__ == "__main__":
    main()