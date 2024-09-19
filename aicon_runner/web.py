import requests
import shutil
import os

from typing import Literal, Optional
from tenacity import retry, wait_random_exponential, stop_after_delay
from urllib.parse import urlparse
from .utils import hash_file_path


def preprocess_url(url: str, force_https: bool = False) -> str:
    if force_https:
        components = urlparse(url)
        components = components._replace(scheme='https')
        return components.geturl()
    return url


class BaseAPI:
    def __init__(self, auth_token: Optional[str] = None, verify: bool = False, force_https: bool = False):
        self.session = requests.Session()
        self.session.headers = {"Authorization": f"Token {auth_token}"}
        self.verify = verify
        self.force_https = force_https

    @retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_delay(60))
    def request(self, url: str, method: Literal["get", "post", "delete", "put"] = 'get', **kwargs) -> requests.Response:
        url = preprocess_url(url, force_https=self.force_https)
        response = getattr(self.session, method)(url, verify=self.verify, **kwargs)
        return response

    @retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_delay(60))
    def download(self, url: str, filepath: str) -> requests.Response:
        url = preprocess_url(url, force_https=self.force_https)
        response = self.session.get(url, stream=True)
        with open(filepath, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return response


class AiconAPI(BaseAPI):
    jobs_url = "jobs"

    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def job_do(self, submission_data: dict, action: Literal["run", "end"]) -> requests.Response:
        url = f"{self.url}/{self.jobs_url}/{submission_data['id']}/{action}/"
        response = self.request(url, method="post", json=submission_data)
        return response

    def job_run(self, submission_data: dict) -> requests.Response:
        return self.job_do(submission_data, action="run")

    def job_end(self, submission_data: dict) -> requests.Response:
        return self.job_do(submission_data, action="end")

    def download_package(self, data: dict, filepath: str, force: bool = False) -> requests.Response:
        if "file_hash" in data and os.path.exists(filepath) and hash_file_path(filepath) == data["file_hash"] and not force:
            response = requests.Response()
            response.status_code = 200
            return response
        return self.download(data["file_url"], filepath=filepath)
