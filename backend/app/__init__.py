
from datetime import datetime
from typing import List

import pendulum
import pandas as pd

from backend.app.exceptions import UnprocessableEntityException
from backend.app.utils import check_is_future_date
from backend.enums import Enums
from requests import get


class ExtractorManager:

    _date_initial: datetime
    _date_final: datetime
    _url: str
    _station: str
    _files: str
    _period: list = []

    def __init__(self, date_initial: datetime, date_final: datetime, url: str, station: str, files: str):
        self.set_date_initial(date_initial)
        self.set_date_final(date_final)
        self.set_url(url)
        self.set_station(station)
        self.set_files(files)

    def extract(self):
        self.set_period()
        all_data = []
        for day in self._period:
            data = get(self.create_url(day))

            if data.status_code != 200:
                raise UnprocessableEntityException('Estação inválida')

            if data.status_code == 200 and self._files == 'Varios Arquivos':
                self.save_many_files([data.json()])

            else:
                all_data.append(data.json())

        if self._files == '1 Arquivo':
            self.save_one_file(all_data)
        self.reset_dates()

    @staticmethod
    def convert_data(all_data: list):
        data_list = []
        for data in all_data:
            data = data['observations']
            for line in data:
                new_dict = {}
                for key in line:
                    if type(line[key]) == dict:
                        for new_key in line[key]:
                            new_dict[new_key] = line[key][new_key]

                    else:
                        new_dict[key] = line[key]

                data_list.append(new_dict)

        return data_list

    def save_one_file(self, all_data: List[dict]):
        data_list = self.convert_data(all_data)

        df = pd.DataFrame(data_list)

        station = df['stationID'][0]
        date = df['obsTimeLocal'][0][0:10]
        date_final = list(df['obsTimeLocal'])[-1][0:10]

        df.to_csv(f'{station}_{date}_{date_final}.csv', index=False, sep=';')

    def save_many_files(self, all_data):
        data_list = self.convert_data(all_data)

        df = pd.DataFrame(data_list)

        station = df['stationID'][0]
        date = df['obsTimeLocal'][0][0:10]

        df.to_csv(f'{station}_{date}.csv', index=False, sep=';')

    def create_url(self, date_for_url: datetime):
        url = Enums().urls[self._url]

        month = date_for_url.month if date_for_url.month > 9 else f'0{date_for_url.month}'
        day = date_for_url.day if date_for_url.day > 9 else f'0{date_for_url.day}'

        url = url.replace("$$$$$$$$", f"{date_for_url.year}{month}{day}")
        url = url.replace("#####", self._station)
        return url

    def reset_dates(self):
        self._date_initial = datetime.today()
        self._date_final = datetime.today()

    def set_date_initial(self, date_initial: datetime):
        check_is_future_date(date_initial)
        self._date_initial = date_initial

    def set_date_final(self, date_final: datetime):
        check_is_future_date(date_final)
        self._date_final = date_final

    def set_period(self):
        if len(self._period) != 0:
            self._period = []

        period = pendulum.period(self._date_initial, self._date_final)
        for days in period.range('days'):
            self._period.append(datetime(days.year, days.month, days.day))

    def set_url(self, url):
        self._url = url

    def set_station(self, station):
        if station is None or station == '':
            raise UnprocessableEntityException('A estação não pode estar vazia')

        self._station = station

    def set_files(self, files):
        self._files = files

    def get_date_initial(self) -> datetime:
        return self._date_initial

    def get_date_final(self) -> datetime:
        return self._date_final

    def get_url(self) -> str:
        return self._url

    def get_station(self) -> str:
        return self._station

    def get_files(self) -> str:
        return self._files
