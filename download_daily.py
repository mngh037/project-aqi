import os
import requests
import zipfile

# Configuration
base_url = "https://aqs.epa.gov/aqsweb/airdata/"
filename_template = "daily_aqi_by_county_{}.zip"
download_dir = "data/downloads"
extract_dir = "data"

# Create folders
os.makedirs(download_dir, exist_ok=True)
os.makedirs(extract_dir, exist_ok=True)

# Download and unzip
for year in range(1980, 2025):
    filename = filename_template.format(year)
    url = base_url + filename
    zip_path = os.path.join(download_dir, filename)

    print(f"Downloading {filename}...")
    response = requests.get(url)

    if response.status_code == 200:
        # Save ZIP file
        with open(zip_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")

        # Unzip to .csv
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"Unzipped {filename} into {extract_dir}")
        except zipfile.BadZipFile:
            print(f"Skipped {filename} - not a valid ZIP file.")
    else:
        print(f"Failed to download {filename} — Status code: {response.status_code}")