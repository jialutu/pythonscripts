import os
import fnmatch
import re

a = "C:/Users/jtu/Documents/pb-nagios/files/pb_objects/services/UAT/centurylink"

def NagiosUpdate(a):
    folders = os.listdir(a)

    for folder in folders:
        b = a+'/'+folder
        files = os.listdir(b)
        for file in files:
            if fnmatch.fnmatch(file, 'dsk_*.cfg'):
                c = b+'/'+file

                f = open(c,mode='r+')
                filedata = f.read()
                f.close()

                newdata = re.sub("pb_247_freq\d-service","pb_247_freq15-service",filedata)

                f = open(c,'w')
                f.write(newdata)
                f.close()

NagiosUpdate(a)
