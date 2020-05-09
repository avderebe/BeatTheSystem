#this will prevent the code from working without the environment set up properly
from binance.client import Client
import dataPull

def Main():
    data1m = dataPull.bitmexBarExtractor('XBTUSD')

if __name__ == "__main__":
    Main()