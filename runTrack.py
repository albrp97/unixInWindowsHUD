import subprocess
import sys

DETACHED_PROCESS = 0x00000008

args = [sys.executable, 'track.py']
subprocess.Popen(args, creationflags=DETACHED_PROCESS)
sys.exit()
