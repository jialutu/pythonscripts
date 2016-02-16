import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import urllib
import numpy as np
import datetime as dt
from matplotlib import style

style.use('ggplot')

#print(plt.style.available)
#print(plt.__file__)

def bytespdate2num(fmt,encoding='utf-8'):
    str_converter = mdates.strpdate2num(fmt)
    def bytes_converter(b):
        s = b.decode(encoding)
        return str_converter(s)
    return bytes_converter

def graph_data(stock):
    fig=plt.figure()
    ax1=plt.subplot2grid((1,1),(0,0))
    plt.ylabel('price')
    plt.xlabel('date')

    print('Currently pulling:',stock)
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=3m/csv'
    source_code=urllib.request.urlopen(url).read().decode()
    stock_data=[]
    split_source=source_code.split('\n')

    for each_line in split_source:
        split_line=each_line.split(',')
        if len(split_line)==6:
            if 'values' not in each_line:
                stock_data.append(each_line)

    date,closep,highp,lowp,openp,volume=np.loadtxt(stock_data,delimiter=',',unpack=True,
                                                   converters={0:bytespdate2num('%Y%m%d')})
#    date,closep,highp,lowp,openp,volume=np.loadtxt(stock_data,delimiter=',',unpack=True)
#    date_conv = np.vectorize(dt.datetime.fromtimestamp)
#    date = date_conv(date)

    x=0
    y=len(date)

    new_list=[]
    while x<y:
        append_line = date[x], closep[x],highp[x],lowp[x],openp[x],volume[x]
        new_list.append(append_line)
        x+=1

    #ax1.fill_between(date, closep, 146, alpha=0.5, edgecolor='r')
#    ax1.plot_date(date,closep,'-')
#    ax1.fill_between(date,closep,155, where=(closep>=155), facecolor='g',alpha=0.5)
#    ax1.fill_between(date,closep,152, where=(closep<=155), facecolor='r',alpha=0.5)
#    ax1.axhline(152, color='r')
#    ax1.axhline(155, color='g')

    candlestick_ohlc(ax1, new_list, width=.6, colorup='#ff1717', colordown='#41ad49')
    ax1.grid(False)
#    ax1.yaxis.label.set_color('m')
#    ax1.xaxis.label.set_color('c')
#    ax1.set_yticks([146,155,164])
#    ax1.spines['left'].set_color('c')
#    ax1.spines['bottom'].set_color('c')
#    ax1.spines['top'].set_visible(False)
#    ax1.spines['right'].set_visible(False)
#    ax1.spines['left'].set_linewidth(5)
#    ax1.spines['bottom'].set_linewidth(5)

    plt.title(stock)
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.annotate('Zuma fired finance minister!', (date[17],openp[17]), xytext=(0.6,0.9), textcoords='axes fraction',
                 arrowprops=dict(facecolor="#585858"))
    bbox_props=dict(boxstyle='larrow, pad=0.3', fc='#f2f1f1', ec='k', lw=2)
    ax1.annotate(str(closep[-1]), (date[-1],closep[-1]), xytext=(date[-1]+2.5,closep[-1]), bbox=bbox_props)

    plt.ylabel('Price')

    plt.subplots_adjust(left=.09,bottom=.16,right=.94,top=.95,wspace=.2,hspace=.2)
    plt.show()

stock = input('Stock to plot: ')
graph_data(stock)
