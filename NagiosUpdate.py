import os
import fnmatch

a = "C:/Users/jtu/Documents/pb-nagios/files/pb_objects/services/UAT/gresham"

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

            newdata = filedata.replace("pb_247_freq3-service","pb_247_freq15-service")

            f = open(c,'w')
            f.write(newdata)
            f.close()
