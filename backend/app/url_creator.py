from datetime import date

from backend.enums import Enums


class Url:

    @staticmethod
    def mount(url, station: str, date_extract: date) -> str:
        url = Enums.urls[url]
        day, month, year = date_extract.day, date_extract.month, date_extract.year

        url = url.replace("$$$$$$$$", f"{year}{month}{day}")
        url = url.replace("#####", station)
        return url
