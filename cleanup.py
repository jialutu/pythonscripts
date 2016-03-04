import os, time, sys

def cleanup(path):
    f = os.listdir(path)
    now = time.time()

    for a in f:
        a=os.path.join(path, a)
        if os.stat(a).st_mtime < now - 60 * 86400:
            if os.path.isfile(a):
                os.remove(a)
