import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import urllib
import numpy as np
import datetime as dt
from matplotlib import style

style.use('ggplot')

MA1=10
MA2=30

#print(plt.style.available)
#print(plt.__file__)

def bytespdate2num(fmt,encoding='utf-8'):
    str_converter = mdates.strpdate2num(fmt)
    def bytes_converter(b):
        s = b.decode(encoding)
        return str_converter(s)
    return bytes_converter

def moving_average(values,window):
    weights=np.repeat(1.0, window)/window
    smas=np.convolve(values,weights,'valid')
    return smas

def high_minus_low(highs,lows):
    return highs-lows

def graph_data(stock):
    fig=plt.figure()
    ax1=plt.subplot2grid((6,1),(0,0),rowspan=1,colspan=1)
    plt.ylabel('H-L')
    ax2=plt.subplot2grid((6,1),(1,0),rowspan=4,colspan=1,sharex=ax1)
    plt.ylabel('Price')
    ax3=plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)
    plt.ylabel('MAvgs')
#    plt.xlabel('date')

    print('Currently pulling:',stock)
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=6m/csv'
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

    ma1=moving_average(closep,MA1)
    ma2=moving_average(closep,MA2)
    start=len(date[MA2-1:])

    x=0
    y=len(date)

    new_list=[]
    while x<y:
        append_line = date[x], closep[x],highp[x],lowp[x],openp[x],volume[x]
        new_list.append(append_line)
        x+=1
    h_l=list(map(high_minus_low,highp,lowp))
    ax1.plot_date(date[-start:],h_l[-start:],'-')
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5,prune='lower'))

    #ax1.fill_between(date, closep, 146, alpha=0.5, edgecolor='r')
#    ax1.plot_date(date,closep,'-')
#    ax1.fill_between(date,closep,155, where=(closep>=155), facecolor='g',alpha=0.5)
#    ax1.fill_between(date,closep,152, where=(closep<=155), facecolor='r',alpha=0.5)
#    ax1.axhline(152, color='r')
#    ax1.axhline(155, color='g')

    candlestick_ohlc(ax2, new_list[-start:], width=.6, colorup='#ff1717', colordown='#41ad49')
    ax2.grid(False)
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
    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)

    #ax2.annotate('Zuma fired finance minister!', (date[15],openp[15]), xytext=(0.6,0.9), textcoords='axes fraction',
    #             arrowprops=dict(facecolor="#585858"))
    bbox_props=dict(boxstyle='larrow, pad=0.3', fc='#c5cbdf', ec='k', lw=2)
    ax2.annotate(str(closep[-1]), (date[-1],closep[-1]), xytext=(date[-1]+2.5,closep[-1]), bbox=bbox_props)
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5,prune='upper'))

    ax3.plot(date[-start:],ma1[-start:], linewidth=1)
    ax3.plot(date[-start:],ma2[-start:], linewidth=1)
    ax3.fill_between(date[-start:], ma2[-start:],ma1[-start:],where=(ma2[-start:]>=ma1[-start:]),facecolor='r',edgecolor='r',alpha=0.5)
    ax3.fill_between(date[-start:], ma2[-start:],ma1[-start:],where=(ma2[-start:]<=ma1[-start:]),facecolor='g',edgecolor='g',alpha=0.5)

    ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5,prune='upper'))

    plt.subplots_adjust(left=.09,bottom=.16,right=.94,top=.95,wspace=.2,hspace=.02)
    plt.show()

stock = input('Stock to plot: ')
graph_data(stock)
