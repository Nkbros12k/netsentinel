"""Download NSL-KDD dataset for training."""

import os
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

FILES = {
    "KDDTrain+.txt": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt",
    "KDDTest+.txt": "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt",
}


def download():
    os.makedirs(DATA_DIR, exist_ok=True)
    for filename, url in FILES.items():
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            print(f"  {filename} already exists, skipping")
            continue
        print(f"  Downloading {filename}...")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
        print(f"  Saved {filename} ({len(resp.content):,} bytes)")


if __name__ == "__main__":
    print("Downloading NSL-KDD dataset...")
    download()
    print("Done.")
