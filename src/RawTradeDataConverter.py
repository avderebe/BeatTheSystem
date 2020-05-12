import pandas
import os


files = [f.name for f in os.scandir("./XBTData") if f.is_file()]

for file in files:
    data = pandas.read_csv('.\\XBTData\\' + file)

    xbtData = data.loc[data['symbol'] == "XBTUSD"]

    xbtData.to_csv(".\\postProcessingData\\XBT" + file[6:])
    os.remove(".\\XBTData\\" + file) 