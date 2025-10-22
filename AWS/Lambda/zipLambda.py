#Accept the directory path that will be zipped as an argument
#Accept the output zip file path and name as an argument
#Output the the location of the zip file and the directory of what was zipped and whether it was successful or not
import os
import zipfile
import sys
import shutil
from pathlib import Path
import subprocess

## Accpet arguments ## accpet a zip name in an argument
sys.argv = ['path/to/file/to/be/zipped/zipLambda.py', 'output\path\where\file\will\go', 'other_dependencies_to_import']
path_to_lambda = sys.argv[0]
output_zip_path = sys.argv[1]
packages = sys.argv[2:]


## make directory ##
# we wipe the directory if it exists already
tmpdir = Path('lambda_dir') #Stores in cwd
tmpdir.mkdir(exist_ok=True) 
if os.path.exists(tmpdir) and os.path.isdir(tmpdir):
    # Remove it completely
    shutil.rmtree(tmpdir)
    print(f"Deleted existing directory: {tmpdir}")
else:
    print(f"Directory does not exist: {tmpdir}")


## make call to copy files from directory into our new directory ##

shutil.copytree(sys.argv[0], tmpdir, dirs_exist_ok=True)
for pkg in packages:
    subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-t", str(tmpdir)], check=True)
#make a loop that will go through the rest of the arguments and install them into the tmpdir

## make zip file ##
shutil.make_archive(tmpdir, 'zip', root_dir=tmpdir)

## return the location of the zipped file and the name and whether it was successful or not ##