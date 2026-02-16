from pathlib import Path
import subprocess
import sys
import os

def run():
    path = Path(__file__).resolve().parent

    phoenix_path = path / "phoenix"

    os.chdir(phoenix_path)

    subprocess.run([sys.executable, phoenix_path / "phoenix.py"])

if __name__ == "__main__":
    run()