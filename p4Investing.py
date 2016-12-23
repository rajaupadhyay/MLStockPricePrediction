# PULLING SPECIFIC DATA OUT FROM THE DATASET (intraQuarter) S&P 500
import pandas as pd
import os
import time
from datetime import datetime

path = "/Users/RAJA/Desktop/COMPUTER SCIENCE/intraQuarter"


def key_stats(gather= "Total Debt/Equity (mrq):"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)] # GATHERS FOLDERS IN THE DIRECTORY INTO A LIST
    # print(stock_list)
    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'DE Ratio',
                               'Price',
                               'stock_p_change',
                               'SP500',
                               'sp500_p_change'])

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    ticker_list = []

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir) # LISTS THE SUB-FOLDERS INSIDE EACH FOLDER IN THE LIST
        ticker = each_dir.split("_KeyStats")[1].replace('/','')
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if len(each_file) > 0 :
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time)
                full_file_path = each_dir + '/' + file
                #print(full_file_path)
                source = open(full_file_path).read()
                try:
                    value = float(source.split(gather+'</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])

                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    #print(ticker, stock_price)

                    if not starting_stock_value:
                        starting_stock_value = stock_price

                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value)*100
                    sp500_p_change = ((sp500_value - starting_stock_value) / starting_sp500_value) * 100


                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price': stock_price,
                                    'stock_p_change': stock_p_change,
                                    'sp500_p_change': sp500_p_change,
                                    'SP500': sp500_value}, ignore_index = True)
                except Exception as e:
                    pass
    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','').replace(':','')+'.csv'
    print(save)
    df.to_csv(save)


    #time.sleep(15)


key_stats()



