import os
import requests
import zipfile

# Configuration
base_url = "https://aqs.epa.gov/aqsweb/airdata/"
filename_template = "hourly_88101_{}.zip"  # 88101 = PM2.5 FRM/FEM mass
download_dir = "data/downloads"
extract_dir = "data/hourly_pm25_by_county"

# Create folders
os.makedirs(download_dir, exist_ok=True)
os.makedirs(extract_dir, exist_ok=True)

# Loop through years 2010–2024
for year in range(2010, 2025):
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

        # Unzip contents into extract_dir
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"Unzipped {filename} into {extract_dir}")
        except zipfile.BadZipFile:
            print(f"Skipped {filename} — not a valid ZIP file.")
    else:
        print(f"Failed to download {filename} — Status code: {response.status_code}")