import os
import sys
import requests
import zipfile

if len(sys.argv) < 2:
    print("1 argument for CNETID required. Format: python script.py <CNETID>")
    sys.exit(1)

CNETID = sys.argv[1]
root = f"/scratch/midway3/{CNETID}/project-aqi-data/"

def get_data(base_url, file):
    download_dir = root + "downloads"

    if file == "aqi":
        filename_template = "daily_aqi_by_county_{}.zip"
        extract_dir = root + "daily_aqi_by_county" 
        start_year = 1980 
    elif file == "pm25":
        filename_template = "hourly_88101_{}.zip"
        extract_dir = root + "hourly_pm25_by_county"
        start_year = 2010

    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(extract_dir, exist_ok=True)

    for year in range(start_year, 2025):
        filename = filename_template.format(year)
        url = base_url + filename
        zip_path = os.path.join(download_dir, filename)

        print(f"Downloading {filename}...")
        response = requests.get(url)

        if response.status_code == 200:
            # Save .zip
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename}")

            # To .csv
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                print(f"Unzipped {filename} into {extract_dir}")
            except zipfile.BadZipFile:
                print(f"Skipped {filename} - not a valid ZIP file.")
        else:
            print(f"Failed to download {filename} — Status code: {response.status_code}")

if __name__ == "__main__":
    base_url = "https://aqs.epa.gov/aqsweb/airdata/"
    get_data(base_url, "aqi")
    get_data(base_url, "pm25")
