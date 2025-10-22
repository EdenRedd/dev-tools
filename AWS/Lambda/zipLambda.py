import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    # Check arguments
    if len(sys.argv) < 3:
        print("Usage: python zipLambda.py <path_to_lambda_dir> <output_zip_path> [packages...]")
        sys.exit(1)

    path_to_lambda = Path(sys.argv[1])
    output_zip_path = Path(sys.argv[2])
    packages = sys.argv[3:]  # optional additional packages

    # Validate input directory
    if not path_to_lambda.exists():
        print(f"Error: Source directory does not exist: {path_to_lambda}")
        sys.exit(1)

    # Create temporary directory
    tmpdir = Path("lambda_dir")

    if tmpdir.exists() and tmpdir.is_dir():
        shutil.rmtree(tmpdir)
        print(f"Deleted existing directory: {tmpdir}")

    tmpdir.mkdir(exist_ok=True)
    print(f"Created fresh directory: {tmpdir}")

    # Copy lambda files into tmpdir
    shutil.copytree(path_to_lambda, tmpdir, dirs_exist_ok=True)
    print(f"Copied contents from {path_to_lambda} to {tmpdir}")

    # Install any requested packages
    for pkg in packages:
        print(f"Installing {pkg}...")
        subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-t", str(tmpdir)], check=True)

    # Make zip file
    zip_file = shutil.make_archive(str(output_zip_path), 'zip', root_dir=tmpdir)

    print(f"\n✅ Successfully created zip file: {zip_file}")
    print(f"📁 Zipped contents from: {path_to_lambda}")
    print(f"📦 Temporary directory used: {tmpdir}")

if __name__ == "__main__":
    main()
