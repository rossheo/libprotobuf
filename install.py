import subprocess
import os
import shutil

if(os.name == "nt"):
    os_build_script = "build_win64.py"
else:
    os_build_script = "build_linux.py"

subprocess.call(os_build_script, shell=True, cwd="build")
if not os.path.exists(os.path.join("..", "ThirdParty")):
    os.mkdir(os.path.join("..", "ThirdParty"))
if os.path.exists(os.path.join("..", "ThirdParty", "libprotobuf")):
    shutil.rmtree(os.path.join("..", "ThirdParty", "libprotobuf"), True)

shutil.copytree("libprotobuf", os.path.join("..", "ThirdParty", "libprotobuf"))
