import tempfile
import tomllib
import sys
import os
import urllib.request
import shutil
import subprocess
from utils import get_repo_data, ProgressBar, setup_env, CROSS_TARGET_TRIPLET, TARGET_TRIPLET, SYSTEM_ROOT, post_status

class PackageGet:
    def __init__(self, repo_path: str, version: str | None):
        self.manifest: dict = tomllib.loads(get_repo_data(repo_path+"/metadata.toml"))
        self.build_info: dict = tomllib.loads(get_repo_data(repo_path+"/build-"+(version if version is not None else self.manifest["package"]["latest-version"])+".toml"))
        self.version = version

    def build(self) -> list[str]:
        progress_bar: ProgressBar = None
        pkg_name = self.manifest["package"]["name"]+" "+self.version
        workspace = tempfile.mkdtemp()
        install = tempfile.mkdtemp()
        env = {
            "WORKSPACE": workspace,
            "INSTALL": install,
            "ROOT": SYSTEM_ROOT.value,
            "HOST_TARGET": TARGET_TRIPLET,
            "CROSS_TARGET": CROSS_TARGET_TRIPLET,
        }
        src_url = ""
        try:
            src_url = self.build_info["metadata"]["source-url"]
        except KeyError as _:
            pass
        if len(src_url) > 0:
            src_archive = tempfile.gettempdir()+"/"+src_url.split("/")[-1]
            progress_bar = ProgressBar("Download "+pkg_name)
            progress_bar.update_progress(0)
            urllib.request.urlretrieve(self.build_info["metadata"]["source-url"],src_archive, lambda blk,blksize,filesize: progress_bar.update_progress(float(blk*blksize)/filesize))
            progress_bar = ProgressBar("Extract "+pkg_name,True)
            progress_bar.start_spinner()
            shutil.unpack_archive(src_archive,workspace)
            os.remove(src_archive)
            progress_bar.stop_spinner()
        # We can finally start building!
        failed = False
        while not failed:
            if self.build_info.get("build",None) is None:
                break
            post_status("Configure "+pkg_name)
            # ,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL
            if subprocess.run(setup_env(env)+self.build_info["build"].get("configure",""),shell=True,executable="/bin/bash",cwd=workspace).returncode > 0:
                failed = True
                break
            post_status("Build "+pkg_name)
            if subprocess.run(setup_env(env)+self.build_info["build"].get("build",""),shell=True,executable="/bin/bash",cwd=workspace).returncode > 0:
                failed = True
                break
            post_status("Finalize "+pkg_name)
            if subprocess.run(setup_env(env)+self.build_info["build"].get("install",""),shell=True,executable="/bin/bash",cwd=workspace).returncode > 0:
                failed = True
                break
            break
        if not failed:
            # Install files to root
            progress_bar = ProgressBar("Install "+pkg_name,True)
            progress_bar.start_spinner()
            if not self.build_info["metadata"].get("bootstrap-oneshot", False):
                category = pkg_name.split("/")[0]
                instlistpath = os.path.join(SYSTEM_ROOT.value,"var/db/vix/instfiles",category)
                if not os.path.exists(instlistpath):
                    os.makedirs(instlistpath,exist_ok=True)
                subprocess.run(f"find -mindepth 1 -printf \"%p:%y\\n\" | cut -c 2- > {os.path.join(instlistpath,self.manifest["package"]["name"].split("/")[1])}",shell=True,executable="/bin/bash",cwd=install)
            shutil.copytree(install,SYSTEM_ROOT.value, dirs_exist_ok=True)
            progress_bar.stop_spinner()
            if self.build_info["build"].get("post-install","") != "":
                post_status("Post-install "+pkg_name)
                subprocess.run(setup_env(env)+self.build_info["build"].get("post-install",""),shell=True,executable="/bin/bash",cwd=SYSTEM_ROOT.value)
        progress_bar = ProgressBar("Cleanup "+pkg_name,True)
        progress_bar.start_spinner()
        shutil.rmtree(workspace)
        shutil.rmtree(install)
        progress_bar.stop_spinner()
        if failed:
            
            sys.exit(1)
