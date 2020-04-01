import argparse
import requests
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('lat', type=float, help='Широта')
parser.add_argument('lon', type=float, help='Долгота')
parser.add_argument('alt', type=int, help='Высота в метрах')
parser.add_argument('n', type=int, help='Количество проходов')
args = parser.parse_args()


URL = 'http://api.open-notify.org/iss-pass.json'


def get_pass_times(lat, lon, alt, n):
    try:
        # Проверка параметров
        lat = lat if -80 <= lat <= 80 else 55.7522
        lon = lon if -180 <= lon <= 180 else 37.6156
        alt = alt if 0 <= alt <= 10.000 else 1
        n = n if 1 <= n <= 100 else 1

        params = {
            'lat': lat,
            'lon': lon,
            'alt': alt,
            'n': n,
        }
        resp = requests.get(
            url=URL,
            params=params
        )
        if resp.status_code != 200:
            return None
        else:
            return resp.json()
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None


# Запуск скрипта
response = get_pass_times(args.lat, args.lon, args.alt, args.n)
if response is not None:
    for item in response['response']:
        next_date = datetime.fromtimestamp(item['risetime'])
        print((f'МКС будет над текущей точкой {next_date}'))
else:
    print(f'Ошибка подключения к {URL}')

