import json

file=input("Enter file location: \n")
#c:/qz.json
with open(file,'r') as f:
    data=json.load(f)

x=len(data["log"]["entries"])

a={}
for i in range(0,x):
    c = data["log"]["entries"][i]["time"]
    b=data["log"]["entries"][i]["request"]["url"]
    a[b]=(c)

c = ((k, a[k]) for k in sorted(a, key=a.get, reverse=True))
for i in c:
    print(i)
