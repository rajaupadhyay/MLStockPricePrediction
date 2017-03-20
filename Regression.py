import pandas as pd
import quandl
import math

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

print(df.head())

# train, test, predict

