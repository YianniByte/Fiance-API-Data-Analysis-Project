import requests
import pandas as pd
from datetime import datetime
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

print("starting script")
##Requests scripts from Alphavantage documentaion
forexkey = '' #IMPORTANT: FOR SCRIPT TO RUN, ACQUIRE AN API KEY (see README)
alumkey = ''  #IMPORTANT: FOR SCRIPT TO RUN, ACQUIRE AN API KEY (see README)

url = 'https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=USD&to_symbol=CNY&apikey={forexkey}'
r = requests.get(url)

url2 = 'https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey={alumkey}'
r2 = requests.get(url2)

##The 4 functions:

def forexdata(json_data):
    data = json_data['Time Series FX (Weekly)']
    df = pd.DataFrame.from_dict(data, orient='index') #Function from KDnuggets tutorial by Kanwal Mehreen 10/06/24
    df.reset_index(inplace=True)                      #reset the index to column from index values; function derived from Chatgpt

    ##Format table and columns
    df.rename(columns={"index": "date","1. open": "Open","2. high": "High","3. low": "Low","4. close": "Close"}, inplace = True) #function from Chatgpt, rename and inplace to existing dataframe
    df['date'] = pd.to_datetime(df['date'], errors = 'coerce')
    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    #print(df.dtypes)

    df["AvgFOREX"] = (df["High"] + df["Low"])/2
    df_filt = df[df["date"] >= "2019-12-31"]
    #print(df_filt.tail())
    #print(df_filt.head())
    return df_filt

def alumdata (json_data):
    data2 = json_data['data']
    #print(data2)
    df2 = pd.DataFrame(data2)                  #Because no row labels, no orient
    df2.reset_index(drop = True, inplace=True) # drop will remove the old index
    #print(df2.head())

    ##Format table and columns
    df2.rename(columns={"value":"AlumUSD_mt"}, inplace = True)
    df2['date'] = pd.to_datetime(df2['date'], errors = 'coerce')
    ##Convert . to Na; ChatGPT used to find the correct package and function for this
    df2['AlumUSD_mt'] = df2['AlumUSD_mt'].replace('.', np.nan)
    ##na.rm the NA before changing all values to float
    df2clean = df2.dropna()
    df2clean.loc[:,'AlumUSD_mt'] = df2clean['AlumUSD_mt'].astype(float) #.loc to set the value explicitly otherwise warning; suggested by Chatgpt to avoid warning.
    #print(df2clean.tail())

    df2_filt = df2clean[df2clean["date"] >= "2019-12-31"]
    return df2_filt

def sqlupload (forex, alum):
    ##Storing both dataframes in SQL database; Key SQL functions from slqite module documentation.
    cx = sqlite3.connect('apidata.db') # Make database
    cursor = cx.cursor()
    ##Make the SQL tables
    cursor.execute("CREATE TABLE IF NOT EXISTS forexweekly(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date DATE NOT NULL," \
            "avgFOREX NUMERIC NOT NULL)")    #Need to add IF NOT EXISTS which was suggested by ChatGPT
    cursor.execute("CREATE TABLE IF NOT EXISTS alummonthly(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date DATE NOT NULL," \
            "AlumUSD_mt NUMERIC NOT NULL)")
    for index, row in forex.iterrows():      #iterate over dataframe rows. Needs index to make row a pandas series, iterrows argument suggested by Chatgpt as fix.
        date = row["date"]
        avgFOREX = row["AvgFOREX"]
        date_str = date.strftime('%Y-%m-%d') #Fixed by Chatgpt as dates were not added correctly
        cursor.execute("INSERT INTO forexweekly (date, avgFOREX) VALUES (?,?)", (date_str, avgFOREX))

    for index, row in alum.iterrows():
        date = row["date"]
        AlumUSD_mt = row["AlumUSD_mt"]
        date_str = date.strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO alummonthly (date, AlumUSD_mt) VALUES (?,?)", (date_str, AlumUSD_mt))
    cx.commit() #Suggested by chatgpt
    cx.close()
    print("Dataframes uploaded")

def plot (forex, alum):
    ##General plot structure derived from StackOverflow by Quang Hoang 17/09/2020
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx() #create right-hand side y axis
    sns.lineplot(x= 'date', y = 'AvgFOREX', data = forex, label = 'FOREX', markers= '8', color = '#a3c4f3', ax = ax1)
    sns.lineplot(x = 'date', y = 'AlumUSD_mt', data = alum, label = 'Aluminium', markers= 's', color = '#f1c0e8', ax = ax2)
    ax1.xaxis.set_minor_locator(mdates.MonthLocator()) ##function found with ChatGPT
    plt.xticks(rotation = 90)
    plt.legend(loc='lower right', labelspacing = 2)    #function suggested by ChatGPT to correct positioning of legends
    ax1.set_xlabel("Date (Years)")
    ax1.set_ylabel("AvgFOREX_(USD/CNY)")
    ax2.set_ylabel("Aluminium (USD/mt)")
    plt.title("Change in FOREX USD/CNY to global aluminium price in the last 5 years")
    plt.grid(True, which='major', axis = 'both', linestyle = '--', linewidth = 0.5) #function found with ChatGPT
    plt.show()

##Main script bringing all functions together
if r.status_code == 200:
    print("Success, API requests OK!")
    jdata = r.json()
    df_filt = forexdata(jdata)
    print(df_filt.head())

    jdataal = r2.json()
    df2_filt = alumdata(jdataal)
    print(df2_filt.head())
    print(df2_filt.tail())
    print(df2_filt.dtypes)

    outcome = sqlupload(df_filt, df2_filt)
    print(outcome)

    plot(df_filt, df2_filt)

#Error checking suggested by Chatgpt
else:
    print("Error with API request, code:", r.status_code)
