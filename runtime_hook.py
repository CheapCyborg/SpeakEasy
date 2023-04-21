import sys
import os

if getattr(sys, 'frozen', False) and not sys.stderr:
    stderr_path = os.path.join(os.path.dirname(sys.executable), 'log.txt')
    sys.stderr = open(stderr_path, 'w')
