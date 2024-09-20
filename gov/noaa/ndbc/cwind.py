import enum
import gzip
import hashlib
import re
import sys
import urllib.parse
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def matches_remote(local_path: Path, remote_url: str) -> bool:
    remote = requests.get(remote_url)

    if remote.ok:
        remote_content = gzip.decompress(remote.content)

        with gzip.open(local_path, 'r') as f:
            local_content = f.read()

        remote_hash = hashlib.sha256(remote_content).hexdigest()
        local_hash = hashlib.sha256(local_content).hexdigest()

        return remote_hash.__eq__(local_hash)

    return False


def download_report(url: str, p: Path) -> Path:
    parsed_url = urllib.parse.urlparse(url)
    dest = p.joinpath(parsed_url.path.split('/')[-1])

    if dest.exists():
        matches = matches_remote(dest, url)
        if not matches:
            dest.unlink(missing_ok=True)
            res = urlretrieve(url, dest)

            return Path(res[0])

        return dest
    else:
        res = urlretrieve(url, dest)

        return Path(res[0])


def normalize_reports(reports: list[Path], dest: Path) -> Path:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.touch(exist_ok=True)

    with gzip.open(reports[0], 'rt') as f:
        lines = f.readlines()

        headers = ' '.join([header for header in lines[0][1:].replace('\n', '').split(' ') if header != '']) + '\n'
        content = ''.join([s for s in [headers] + lines if not s.startswith('#')])

    with open(dest, 'wt') as wf:
        wf.write(content)

    print(f"saved normalized data to `{dest.__str__()}`")

    return dest


def download_cwind_data(url: str, p: Path, dest: Path) -> Path:
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        hold = [f"{url}{a['href']}" for a in soup.find_all('a', string=re.compile(r".*\.txt\.gz$"))]

        if not p.exists():
            p.mkdir(exist_ok=True, parents=True)

        reports = [download_report(remote_gz, p) for remote_gz in hold]
        normalized_data = normalize_reports(reports, dest)

    return dest


def normalize_cwind(f: Path) -> DataFrame:
    r = pd.read_csv(f, sep=r'\s+')

    # NOAA uses 9s for NaNs o0
    r.replace([999, 99.0, 9999], 0, inplace=True)

    # combine the date features into on date/time feature
    r['TS'] = pd.to_datetime(r[['YY', 'MM', 'DD', 'hh', 'mm']].apply(
        lambda row: f"{row['YY']}-{row['MM']}-{row['DD']} {row['hh']}:{row['mm']}",
        axis=1
    ))

    # drop original date features
    r.drop(['YY', 'MM', 'DD', 'hh', 'mm'], axis=1, inplace=True)
    # replace NaNs with 0
    # r.fillna(0, inplace=True)

    return r


def visualize_training(r: DataFrame):
    r.replace(0, np.nan, inplace=True)

    # print(r.describe())
    # print(r.head(25))

    # scatter plot between wind speed (WSPD) and gust speed (GST)
    plt.figure(figsize=(8, 6))
    plt.scatter(r['TS'], r['WSPD'], label='wind speed', alpha=0.5)
    plt.scatter(r['TS'], r['GST'], label='gusts', alpha=0.5)
    plt.title('wind speed vs. gusts')
    plt.xlabel('time')
    plt.xticks(rotation=45)
    plt.ylabel('speed (?/?)')
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()


class ModelType(enum.Enum):
    LINEAR_REGRESSION = {'key': 1, 'val': ''}


def do_linreg_model(X_scaled, y):
    mdl = LinearRegression(n_jobs=3)

    return mdl.fit(X_scaled, y)


def train_cwind(master: Path, model: Path, mdl: ModelType = ModelType.LINEAR_REGRESSION) -> object:
    training_data = normalize_cwind(master)

    visualize_training(training_data)

    X = training_data[['WDIR', 'WSPD']].dropna()  # features
    y = training_data['TS']  # target

    # split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # standardize the feature data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    if mdl is ModelType.LINEAR_REGRESSION:
        _model = do_linreg_model(X_train_scaled, y_train)

        print(_model)
        return _model


def main():
    args = sys.argv
    subcmd = None
    if len(args) > 1:  # we have an argument
        subcmd = args[1].strip()

    if subcmd is not None:
        # we have a command
        if subcmd == 'pull':
            # command example: pull <url> <path to store downloads> <path to comprehensive training file>
            if len(args) == 5:
                url = args[2].strip()
                path = Path(args[3].strip())
                dump_path = Path(args[4].strip())
                print(f"downloading from `{url}`\nto `{path}`.\nplacing curated data in `{dump_path}`")
                download_cwind_data(url, path, dump_path)

        if subcmd == 'train':
            if len(args) == 4:
                master_file = Path(args[2].strip())
                model_file = Path(args[3].strip())

                train_cwind(master_file, model_file)


if __name__ == "__main__":
    main()
