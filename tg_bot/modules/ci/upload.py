from ftplib import FTP, error_perm
from tg_bot import get_config
from tg_bot.core.logging import LOGI
from tg_bot.modules.ci.artifacts import Artifact
import os.path
import paramiko
from pathlib import Path
import shutil

ALLOWED_METHODS = ["localcopy", "ftp", "sftp"]


def ftp_chdir(ftp: FTP, remote_directory: Path):
    if remote_directory == "/":
        ftp.cwd("/")
        return
    if remote_directory == "":
        return
    try:
        ftp.cwd(str(remote_directory))
    except error_perm:
        dirname, basename = os.path.split(str(remote_directory).rstrip("/"))
        ftp_chdir(ftp, dirname)
        ftp.mkd(basename)
        ftp.cwd(basename)
        return True


def sftp_chdir(sftp: paramiko.SFTPClient, remote_directory: Path):
    if remote_directory == "/":
        sftp.chdir("/")
        return
    if remote_directory == "":
        return
    try:
        sftp.chdir(str(remote_directory))
    except IOError:
        dirname, basename = os.path.split(str(remote_directory).rstrip("/"))
        sftp_chdir(sftp, dirname)
        sftp.mkdir(basename)
        sftp.chdir(basename)
        return True


class Uploader:
    """
    Uploader class.
    """

    def __init__(self):
        """
        Initialize the uploader variables.
        """
        self.method = get_config("CI_ARTIFACTS_UPLOAD_METHOD")
        self.destination_path_base = Path(get_config("CI_UPLOAD_BASE_DIR"))
        self.host = get_config("CI_UPLOAD_HOST")
        self.port = get_config("CI_UPLOAD_PORT")
        self.server = (self.host if self.port is None or self.port == "" else
                       f"{self.host}:{self.port}")
        self.username = get_config("CI_UPLOAD_USERNAME")
        self.password = get_config("CI_UPLOAD_PASSWORD")

        if self.method not in ALLOWED_METHODS:
            raise NotImplementedError("Upload method not valid")

    def upload(self, artifact: Artifact, destination_path_ci: Path):
        """
        Upload an artifact using settings from config.env

        Returns True if the upload went fine
        """
        if not artifact.path.is_file():
            raise FileNotFoundError("File doesn't exists")

        if self.destination_path_base is None:
            destination_path = destination_path_ci
        else:
            destination_path = self.destination_path_base / destination_path_ci

        LOGI(f"Started uploading of {artifact.path.name}")

        if self.method == "localcopy":
            os.makedirs(destination_path, exist_ok=True)
            shutil.copy(artifact.path, destination_path)
        elif self.method == "ftp":
            ftp = FTP(self.server)
            ftp.login(self.username, self.password)
            ftp_chdir(ftp, destination_path)
            with open(artifact.path, "rb") as f:
                ftp.storbinary("STOR %s" % artifact.path.name, f)
                f.close()
            ftp.close()
        elif self.method == "sftp":
            transport = paramiko.Transport(self.server)
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp_chdir(sftp, destination_path)
            sftp.put(artifact.path, artifact.path.name)
            sftp.close()
            transport.close()

        LOGI(f"Finished uploading of {artifact.path.name}")
        return True
