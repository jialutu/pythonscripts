import json

file=input("Enter file location: \n")
#c:/qz.json
with open(file,'r') as f:
    data=json.load(f)

x=len(data["log"]["entries"])

a={}
for i in range(0,x):
    b=data["log"]["entries"][i]["request"]["url"]
    a[b]=(data["log"]["entries"][i]["time"])

for key, value in sorted(a.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)
