
from ftplib import FTP
from downloaders.commons import DATA_FOLDER


def download_ftp(url, cwd, fname, user='anonymous', passwd=''):

    fname_output = f"{DATA_FOLDER}/{fname}"

    try:
        ftp = FTP(url)
        ftp.login(user=user, passwd=passwd)
        ftp.cwd(cwd)
        ftp.retrbinary("RETR " + fname, open(fname_output, 'wb').write)
        ftp.close()
        return True
    except:
        return False

