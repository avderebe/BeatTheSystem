#this will prevent the code from working without the environment set up properly
from binance.client import Client
import dataPull
import pandas
import os,glob
from pathlib import Path


def Main():
    #data1m = dataPull.bitmexBarExtractor('XBTUSD')

    subfolders = [ f.name for f in os.scandir(r'C:/Users/timde/OneDrive/Desktop/algo/BeatTheSystem/XBTdata/') if f.is_file() ]
    subfolders = ([s.replace('XBT.csv', '') for s in subfolders]) 

    for d in pandas.date_range('20141122','20200505'):
        if(d.strftime('%Y%m%d') not in subfolders):
            print(d.strftime('%Y%m%d'))

    mb = pandas.read_csv(r"C:\Users\timde\OneDrive\Desktop\algo\BeatTheSystem\XBTUSD_MinuteBars_BitMEX.csv")
    print("ok")
    # for date in subfolders:
        # data_folder = Path("extracted/"+date+".csv")
        # file_to_open = data_folder / ("trade_"+date+".csv")
        # df = pandas.read_csv(file_to_open)
        # df = df[df.symbol == 'XBTUSD']
        # df.to_csv (r'C:/Users/timde/OneDrive/Desktop/algo/BeatTheSystem/XBTdata/' + date + 'XBT.csv', index = None, header=True)
        # print(date)



if __name__ == "__main__":
    Main()