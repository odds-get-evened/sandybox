import gzip
import hashlib
import os.path
import re
import sys
import urllib.parse
from pathlib import Path
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup


def matches_remote(local: Path, url: str):
    remote_res = requests.get(url)

    if remote_res.ok:
        remote_content = gzip.decompress(remote_res.content)

        with gzip.open(local, 'r') as f:
            local_content = f.read()

        remote_hash = hashlib.sha256(remote_content).hexdigest()
        local_hash = hashlib.sha256(local_content).hexdigest()

        return remote_hash.__eq__(local_hash)


def download_report(url: str, p: Path):
    up = urllib.parse.urlparse(url)
    dest = p.joinpath(up.path.split('/')[-1])

    if dest.exists():
        # check to see if it matches remote
        match = matches_remote(dest, url)
        if not match:
            dest.unlink(missing_ok=True)
            res = urlretrieve(url, dest)
            return res[0]
    else:
        res = urlretrieve(url, dest)
        return res[0]


def download_cwind(url: str, p: Path):
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        hold = soup.find_all('a', string=re.compile(r".*\.txt\.gz$"))
        hold = [f"{url}{th['href']}" for th in hold]

        if not p.exists():
            p.mkdir(exist_ok=True, parents=True)

        dl = [download_report(gz, p) for gz in hold]
        print(dl)


def main():
    download_cwind(
        "https://www.ndbc.noaa.gov/data/cwind/Apr/",
        Path(os.path.expanduser('~'), ".databox", "buoys", "downloads")
    )


if __name__ == "__main__":
    main()
