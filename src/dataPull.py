import pandas as pd
from bitmex import bitmex
import datetime
import pytz
import time

# YOUR API KEYS HERE
api_id = "hPu7gV8dM-HSo8ogCm-1bZXG"    #Enter your own API-key here
api_secret = "e_vHfPGIsGfrUizDM_c6SOF1PEthjCPx6pEpQtEehtG0ijHC" #Enter your own API-secret here

bclient =  bitmex(test=False, api_key=api_id, api_secret=api_secret)

def bitmexBarExtractor(symbol):
    start_date = datetime.datetime.strptime('1 Jan 2015', '%d %b %Y')
    print('working...')
    filename = '{}_MinuteBars_BitMEX.csv'.format(symbol)
    staging = []
  
    while start_date.replace(tzinfo=pytz.utc) < (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=1)):
        start_point = time.time()
        print('processing from: {}'.format(start_date))
        klines = bclient.Trade.Trade_getBucketed(symbol='XBTUSD', binSize='1m', count=1000, startTime=start_date, endTime=datetime.datetime.utcnow()).result()[0]
        if len(klines) == 0: # no data, start date reference too early.
            start_date = start_date + datetime.timedelta(weeks=4.5)
        else:
            start_date = klines[len(klines)-1]['timestamp'].replace(tzinfo=pytz.utc)
            for item in klines:
                staging.append(item)

        end_point = time.time()
        diff_time = end_point - start_point

        if diff_time < 1: #if less than 1 second, sleep the difference so we don't trigger the rate limiter on BitMEX's end.
            #print('sleeping for {}ms'.format((1 - diff_time + 0.010) * 100))
            time.sleep((1 - diff_time + 0.010))

    data = pd.DataFrame(staging)
  
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data = data.drop_duplicates()

    data = data.dropna(axis=0, subset=['open']) # Clean up rows with no price data because BitMEX server has iffy data sometimes.

    data.set_index('timestamp', inplace=True)
  
    data.to_csv(filename)
    print('finished!')
    return data

if __name__ == '__main__':
    bitmexBarExtractor('XBTUSD')