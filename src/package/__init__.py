import tempfile
import tomllib

PACKAGE_DATABASE = "/var/db/vix"

class PackageGet:
    def __init__(self, name: str, build_data: str):
        self.name: str = name
        self.build_data: dict = tomllib.loads(build_data)
    
    def unpack(self):
        packages = self.build_data["packages"]
        stage1 = packages["stage1"]
        
    
