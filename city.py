""" 
A simple script that receives the weather forecast from the Yahoo API 
and prints it to the user. Over time, it may stop working if the Yahoo API will change 
or the fields will change in JSON. 
The script is built on class composition and easily expandable.
"""

import requests
import sys
from dateutil.parser import parse


class YahooWeatherForecast:

    def __init__(self):  
        # сохраняет кэш уже полученной погоды
        self._city_cache = {}

    def get(self, city):
        # если погода города имеется в кэше, возвращает ее
        if city in self._city_cache:
            return self._city_cache[city]
        url = f"https://query.yahooapis.com/v1/public/yql?q=" 
        + f"select%20*%20from%20weather.forecast%20where%20w"
        + f"oeid%20in%20(select%20woeid%20from%20geo.places("
        + f"1)%20where%20text%3D%22{city}%22)%20and%20u%3D%2"
        + f"7c%27&format=json&env=store%3A%2F%2Fdatatables.o"
        + f"rg%2Falltableswithkeys"
        print("Sending HHTP request")
        # обращается к url и обрабатывает ответ-json в виде словаря
        data = requests.get(url).json() 
        # вытаскиваем словарь с погодой
        forecast_data = data["query"]["results"]["channel"]["item"]["forecast"] 
        forecast = []
        # для каждого дня в прогнозе создаем словарь с днем и температурой
        for day_data in forecast_data: 
            forecast.append({
                "date": parse(day_data["date"]), 
                "high_temp": day_data["high"]
            })
        # сохраняем полученную погоду в кэш объекта
        self._city_cache[city] = forecast 
        return forecast


class CityInfo:
    """ 
    Class for information about the city. 
    Expandable to infinity through the composition of other classes
    """
    def __init__(self, city, weather_forecast=None): 
        self.city = city
        # позволяет использовать всего один объект YahooWeatherForecast для разных городов
        self._weather_forecast = weather_forecast or YahooWeatherForecast()
    def weather_forecast(self):
        return self._weather_forecast.get(self.city)


def _main():
    weather_forecast = YahooWeatherForecast() 
    # проверяем работу кэширования через принт совершения HHTP-запроса (будет всего 1 раз вместо 5)
    for i in range(5): 
        # используем один и тот же объект YahooWeatherForecast
        city = CityInfo(sys.argv[1], weather_forecast=weather_forecast) 
        forecast = city.weather_forecast()
        print(forecast)


if __name__ == "__main__":
    _main()
