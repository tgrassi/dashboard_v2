import requests
import os
from downloaders.commons import DATA_FOLDER

def download_file(url, destination_filename):
    """Download a file from a URL and save it to the data folder."""
    # Get the directory of the current file
    output_path = os.path.join(DATA_FOLDER, destination_filename)

    # set agent to avoid 403 error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        with open(output_path, 'w') as f:
            f.write(response.text)

        print(f"Successfully downloaded CSV to {output_path}")
        return output_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
