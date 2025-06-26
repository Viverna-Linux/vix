import tempfile
import tomllib
import sys
import urllib.request
from utils import get_repo_data

class PackageGet:
    def __init__(self, repo_path: str, version: str | None):
        self.manifest: dict = tomllib.loads(get_repo_data(repo_path+"/metadata.toml"))
        self.build_info: dict = tomllib.loads(get_repo_data(repo_path+"/build-"+(version if version is not None else self.manifest["package"]["latest-version"])+".toml"))
    
    def build(self):
        src_url = ""
        try:
            src_url = self.build_info["metadata"]["source-url"]
        except KeyError as _:
            pass
        if len(src_url) > 0:
            src_archive = tempfile.gettempdir()+"/"+src_url.split("/")[-1]
            urllib.request.urlretrieve(self.build_info["metadata"]["source-url"],src_archive)
        
