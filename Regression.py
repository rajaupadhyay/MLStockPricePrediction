import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, svm
from sklearn.linear_model import LinearRegression
from sklearn import model_selection
df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open','Adj. High','Adj. Close','Adj. Low','Adj. Volume']]

df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] * 100.0

df['PCT_CHANGE'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_CHANGE', 'Adj. Volume']]

# Adjusted close should be a feature

forecast_col = "Adj. Close"
df.fillna(-9999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df))) # Initial prediction out 10%

# Label sorted out
df['label'] = df[forecast_col].shift(-forecast_out) #Shift columns

# print(df.head())
df.dropna(inplace=True)

# train, test, predict with classifier

X = np.array(df.drop(['label'], 1)) #Features - 1 denotes dropping of column and not of a row
y = np.array(df['label']) #label

X = preprocessing.scale(X) #Scaling X before feeding it to the classifier

X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y, test_size=0.2)

clf = LinearRegression(n_jobs=10) # Holy shit - 95% accuracy - Try threading LinearRegression (running linearly lol but try run in parallel)

# clf = svm.SVR(kernel="poly") # Support vector regression - this kinda sucks - 71% accuracy
clf.fit(X_train, y_train) #fit features and labels
accuracy = clf.score(X_test, y_test) #accuracy is squared error

print(accuracy)

