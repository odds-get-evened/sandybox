import gzip
import hashlib
import os.path
import re
import sys
import time
import urllib.parse
from pathlib import Path
from urllib.request import urlretrieve

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

CWIND_MASTER = Path(os.path.expanduser('~'), '.databox', 'buoys', 'cwind-master.txt')
DOWNLOADS_PATH = Path(os.path.expanduser('~'), '.databox', 'buoys', 'downloads')


def matches_remote(local: Path, url: str) -> bool:
    remote_res = requests.get(url)

    if remote_res.ok:
        remote_content = gzip.decompress(remote_res.content)

        with gzip.open(local, 'r') as f:
            local_content = f.read()

        remote_hash = hashlib.sha256(remote_content).hexdigest()
        local_hash = hashlib.sha256(local_content).hexdigest()

        return remote_hash.__eq__(local_hash)


def download_report(url: str, p: Path) -> Path:
    up = urllib.parse.urlparse(url)
    dest = p.joinpath(up.path.split('/')[-1])

    if dest.exists():
        # check to see if it matches remote
        match = matches_remote(dest, url)
        if not match:
            dest.unlink(missing_ok=True)
            res = urlretrieve(url, dest)
            return Path(res[0])

        return dest
    else:
        res = urlretrieve(url, dest)
        return Path(res[0])


def process_reports(p: Path):
    with gzip.open(p, 'rt', encoding='utf8') as f:
        lines = f.readlines()
        # get first line for column headers
        header = lines[0].replace('#', '')

        content = ''.join([s for s in [header] + lines if not s.startswith('#')])

    with open(CWIND_MASTER, 'wt') as fw:
        fw.write(content)

    print(f"saved {content[:16]}...{content[48:]} (partial data) to {CWIND_MASTER.__str__()}")


def download_cwind(url: str, p: Path):
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        hold = soup.find_all('a', string=re.compile(r".*\.txt\.gz$"))
        hold = [f"{url}{th['href']}" for th in hold]

        if not p.exists():
            p.mkdir(exist_ok=True, parents=True)

        dl = [download_report(gz, p) for gz in hold]
        [process_reports(r) for r in dl]

        print(f"sync complete. data saved to {CWIND_MASTER}")


def cwind_train(p: Path):
    try:
        # col_names = [x.replace('\n', '') for x in get_header()[1:].split(' ') if x]
        with open(p, 'r') as f:
            col_names = [
                x for x in
                f.readlines()[0].strip().replace('\n', '').split(' ')
                if x
            ]
        res = pd.read_csv(p, sep=r'\s+', names=col_names, skiprows=1)
        res.replace([999, 99.0, 9999], np.nan, inplace=True)
        # combine the date columns into one
        res['TS'] = pd.to_datetime(res[['YY', 'MM', 'DD', 'hh', 'mm']].apply(
            lambda row: f"{row['YY']}-{row['MM']}-{row['DD']} {row['hh']}:{row['mm']}",
            axis=1
        ))
        # drop originals
        res.drop(['YY', 'MM', 'DD', 'hh', 'mm'], axis=1, inplace=True)
        res.fillna(0, inplace=True)

        print(res.describe())
        print(res.head(25))

        res['TS'] = pd.to_datetime(res['TS'])
        res['hour'] = res['TS'].dt.hour
        res['minute'] = res['TS'].dt.minute
        res['dayofweek'] = res['TS'].dt.dayofweek

        # define features and target
        y = res['WSPD']
        X = res.drop(['WSPD', 'TS'], axis=1)

        # feature scaling (optional)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # split up the data for testing and training
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.3, random_state=42
        )

        # train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # predict
        y_pred = model.predict(X_test)

        joblib.dump(model, Path(
            os.path.expanduser('~'), '.databox', 'buoys', 'models',
            f'buoy-cwind-linreg-{time.strftime('%Y%m%d%H%M%S')}.pkl'
        ).__str__())

        # evaluate
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"mean squared error: {mse:.2f}")
        print(f"R^2 score: {r2:.2f}")

        final_res = pd.DataFrame({'actual': y_test.values, 'predicted': y_pred})
        print(final_res)

        residuals = y_test - y_pred
        plt.scatter(y_pred, residuals)
        plt.hlines(y=0, xmin=min(y_pred), xmax=max(y_pred), colors='red')
        plt.xlabel('predicted values')
        plt.ylabel('residuals')
        plt.title('residual plot')
        plt.show()
    except FileNotFoundError as e:
        print(f"please provide a valid cwind master file or run a sync.\n{e}")
        sys.exit(-1)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1].__eq__('sync'):
            if len(sys.argv) < 3:
                print("url is required")

            download_cwind(
                "https://www.ndbc.noaa.gov/data/cwind/Apr/",
                DOWNLOADS_PATH
            )

        if sys.argv[1].__eq__('train'):
            cwind_train(CWIND_MASTER)


if __name__ == "__main__":
    main()
