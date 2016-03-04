import os, time, sys

path = r"C:\temp"
now = time.time()

for f in os.listdir(path):
    f = os.path.join(path, f)
    if os.stat(f).st_mtime < now - 60 * 86400:
        if os.path.isfile(f):
            os.remove(f)
