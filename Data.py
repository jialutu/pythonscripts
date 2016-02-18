import urllib.request
import json
import time
import datetime

def fetchPreMarket(symbol, exchange):
    link = "http://finance.google.com/finance/info?client=ig&q="
    url = link+"%s:%s" % (exchange, symbol)
    u = urllib.request.urlopen(url)
    content = u.read().decode()
    data = json.loads(content[3:])
    info = data[0]
    t = str(info["lt_dts"])    # time stamp
    l = float(info["pcls_fix"])    # close price (previous trading day)
    p = float(info["l"])   # stock price in pre-market (after-hours)
    return (t,l,p)

p0 = 0
while True:
    try:
        t,l,p = fetchPreMarket("INVP","LON")
        with open("C:\Test\invp.l.txt",'a') as f:
            f.write("%s,%s,%s\n"%(t,str(l),str(p)))
            f.close()
    except (RuntimeError, TypeError, NameError) as e:
        print(e)
    if(p!=p0):
        p0 = p
        print("%s\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % (#datetime.datetime.now().strftime("%I:%M:%S%p on %d %B %Y"),
                                                      t, l, p, p-l,(p/l-1)*100.))
    time.sleep(60)
