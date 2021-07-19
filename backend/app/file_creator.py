from settings import PATH


class File:

    @staticmethod
    def header(file):
        file.write("stationID;tz;obsTimeUtc;obsTimeLocal;epoch;lat;lon;solarRadiationHigh;uvHigh;winddirAvg;")
        file.write("humidityHigh;humidityLow;humidityAvg;qcStatus;tempHigh;tempLow;windspeedHigh;windspeedLow;")
        file.write("windspeedAvg;windgustHigh;windgustLow;windgustAvg;dewptHigh;dewptLow;dewptAvg;")
        file.write("windchillHigh;windchillLow;windchillAvg;heatindexHigh;heatindexLow;heatindexAvg;")
        file.write("pressureMax;pressureMin;pressureTrend;precipRate;precipTotal\n")

    def get_file(self, name, header=True):
        file = open(f"{PATH}\{name}.txt", 'a')
        if header:
            self.header(file)
        return file
