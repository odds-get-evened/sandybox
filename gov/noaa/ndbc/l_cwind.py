import asyncio
import os.path
import secrets
from pathlib import Path

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

L_CWIND_URL = "https://www.ndbc.noaa.gov/data/l_cwind/"

DESIGNATED_PATH = Path(os.path.expanduser('~'), '.databox', 'buoys', 'downloads', 'l_cwind')
if not DESIGNATED_PATH.exists():
    DESIGNATED_PATH.mkdir(parents=True, exist_ok=True)

MASTER_SHEET_PATH = Path(os.path.expanduser('~'), '.databox', 'buoys', 'masters', 'l_cwind.txt')


async def fetch(sess, url):
    async with sess.get(url) as response:
        response.raise_for_status()  # for HTTP errors

        return await response.text()


async def train_content(content):
    # mash all the text files together

    # with aiofiles.open(MASTER_SHEET_PATH, 'a+') as f:


    return "nothing yet"


async def process_txt_content(content, url):
    print(f"starting to process {url}")
    print(await train_content(content))
    # await asyncio.sleep(2)
    print(f"finished processing {url}")


async def download_and_process_txt(sess, url):
    local_file = os.path.basename(url)
    local_path = Path(DESIGNATED_PATH, local_file)

    # check to see if file exists already
    if local_path.exists():
        print(f"file already exists: {local_path}. skipping download.")
    else:
        try:
            print(f"starting download of {url}")
            content = await fetch(sess, url)
            # savethe ccontent to file
            async with aiofiles.open(local_path, 'w') as f:
                await f.write(content)
            print(f"finised download and saved to {local_path}")
        except Exception as e:
            print(f"error downloading {url}: {e}")
            return

    try:
        async with aiofiles.open(local_path, 'r') as f:
            content = await f.read()
        await process_txt_content(content, url)
    except Exception as e:
        print(f"error reading {local_path}: {e}")


async def pull_remote_data(url: str):
    async with aiohttp.ClientSession() as session:
        print("fetching main index...")
        html = await fetch(session, L_CWIND_URL)
        print("main index fetched.")

        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.find_all('a')
        txt_files = [
            f"{L_CWIND_URL}{tag['href']}"
            for tag in a_tags
            if tag.get('href') and tag['href'].lower().endswith('.txt')
        ]

        print(f"found  {len(txt_files)} .txt files to download.")

        tasks = [
            asyncio.create_task(download_and_process_txt(session, txt_url))
            for txt_url in txt_files
        ]

        await asyncio.gather(*tasks)
        print(f"all downloads and processing completed.")


def main():
    asyncio.run(pull_remote_data(L_CWIND_URL))


if __name__ == "__main__":
    main()
