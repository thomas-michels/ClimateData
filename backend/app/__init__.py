
from datetime import datetime
from typing import List

import pendulum

from backend.app.exceptions import UnprocessableEntityException
from backend.app.file_creator import File
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
            if data.status_code == 400:
                data = get(self.create_url(day))

            if data.status_code != 200:
                raise UnprocessableEntityException('Estação inválida')

            all_data.append(data.json())

        self.save(all_data)

    def save(self, all_data: List[dict]):
        if self._files == '1 Arquivo':
            station = all_data[0]['observations'][0]['stationID']
            name = f'{station}-' \
                   f'{self._date_initial.year}-{self._date_initial.month}-{self._date_initial.day}' \
                   f'_{self._date_final.year}-{self._date_final.month}-{self._date_final.day}'

            file = File().get_file(name)

            for data in all_data:
                data = data['observations']

                for observations in data:
                    line = ''
                    for key in observations.keys():
                        if not type(observations[key]) == dict:
                            line += str(observations[key]) + ';'

                        else:
                            for new_key in observations[key].keys():
                                line += str(observations[key][new_key]) + ';'

                    line = line[0:-1] + line[-1].replace(';', '\n')
                    file.write(line)

        else:
            station = all_data[0]['observations'][0]['stationID']

            for data in all_data:
                data = data['observations']

                for observations in data:

                    date = observations['obsTimeLocal'][:10]
                    name = f'{station}-' \
                           f'{date}'

                    file = File().get_file(name)

                    line = ''

                    for key in observations.keys():
                        if not type(observations[key]) == dict:
                            line += str(observations[key]) + ';'

                        else:
                            for new_key in observations[key].keys():
                                line += str(observations[key][new_key]) + ';'

                    line = line[0:-1] + line[-1].replace(';', '\n')
                    file.write(line)

    def create_url(self, date_for_url: datetime):
        url = Enums().urls[self._url]

        month = date_for_url.month if date_for_url.month > 9 else f'0{date_for_url.month}'
        day = date_for_url.day if date_for_url.day > 9 else f'0{date_for_url.day}'

        url = url.replace("$$$$$$$$", f"{date_for_url.year}{month}{day}")
        url = url.replace("#####", self._station)
        return url

    def set_date_initial(self, date_initial: datetime):
        check_is_future_date(date_initial)
        self._date_initial = date_initial

    def set_date_final(self, date_final: datetime):
        check_is_future_date(date_final)
        self._date_final = date_final

    def set_period(self):
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