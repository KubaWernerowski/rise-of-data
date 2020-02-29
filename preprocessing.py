#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

transcriptDir = r'/Users/Xi/Documents/比赛/Hackathon 2020 TDxRotman/hackathon_data/company_transcripts'

df = pd.DataFrame()
for filename in os.listdir(transcriptDir):
    if '.json' in filename: 
        print(filename)
        ticker = filename[:-5]
        fullFilename = r"{0}/{1}".format(transcriptDir,filename)
        tempData = pd.read_json(fullFilename)
        tempData['Ticker'] = ticker
        df = df.append(tempData, ignore_index = True)

priceDir = r'/Users/Xi/Documents/比赛/Hackathon 2020 TDxRotman/hackathon_data/company_prices_returns'

def getStockPrice(row):
    ticker = row['Ticker']
    print(ticker)
    date = row['date'].strftime("%Y-%m-%d")
    fileName = r'{0}/{1}_adj_close.csv'.format(priceDir,ticker)
    tempData = pd.read_csv(fileName)
    tempDataDate = tempData.loc[tempData.Date == date]
    tempDataDate.reset_index(inplace = True, drop = True)
    if tempDataDate.shape[0] > 0:
        return tempDataDate.loc[0, 'Returns']
    else:
        return 0

df['Returns'] = df.apply(getStockPrice,axis=1)
