import tempfile
import tomllib
from utils import get_repo_data

class PackageGet:
    def __init__(self, repo_path: str):
        self.manifest = tomllib.loads(get_repo_data(repo_path+"/metadata.toml"))
    
    def unpack(self):
        
        
    
