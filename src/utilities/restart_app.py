import os
import sys

def restart_application():
    os.execv(sys.executable, [sys.executable, sys.argv[0]] + sys.argv[1:])