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
    df = pd.DataFrame(columns=['Date','Unix','Ticker','DE Ratio'])
    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir) # LISTS THE SUB-FOLDERS INSIDE EACH FOLDER IN THE LIST
        ticker = each_dir.split("_KeyStats")[1].replace('/','')
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
                    df = df.append({'Date':date_stamp, 'Unix':unix_time,'Ticker':ticker,'DE Ratio':value}, ignore_index = True)
                except Exception as e:
                    pass
    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','').replace(':','')+'.csv'
    print(save)
    df.to_csv(save)


            #time.sleep(15)


key_stats()



