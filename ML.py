import pandas as pd
from Quandl import Quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

df = Quandl.get('WIKI/GOOGL')

df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume',]]

df['HL_PCT'] = (df['Adj. High']-df['Adj. Low'])/df['Adj. Low'] *100.0
df['PCT_Change'] = (df['Adj. Close']-df['Adj. Open'])/df['Adj. Open'] *100.0

df=df[['Adj. Close','HL_PCT','PCT_Change','Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df)))

df['label']=df[forecast_col].shift(-forecast_out)

X = np.array(df.drop(['label'],1))
X = X[:-forecast_out]
X_lately = X[-forecast_out:]
x = preprocessing.scale(X)

df.dropna(inplace=True)
y = np.array(df['label'])
y = np.array(df['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(accuracy)
