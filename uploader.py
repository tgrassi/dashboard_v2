import glob
import os
from ftplib import FTP


def upload_files():
    files = glob.glob("website/data/*.json")
    if not files:
        print("No files found")
        return

    ftp = FTP()
    ftp.connect("smanettare.altervista.org", 21)
    ftp.login(user="smanettare", passwd="C2DgqgSpnJE7")

    remote_folder = "climate_dash/data"
    ftp.cwd(remote_folder)

    try:
        for filepath in files:
            filename = os.path.basename(filepath)
            with open(filepath, "rb") as f:
                print(f"Uploading {filepath} -> {remote_folder}/{filename}")
                ftp.storbinary(f"STOR {filename}", f)
    finally:
        ftp.quit()


if __name__ == "__main__":
    upload_files()