import json
import requests
from Config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Извините, но невозможно вывести одинаковые валюты {base}. Посмотрите повторно инструкцию!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать введенную валюту {quote}. Введите корректную валюту!')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать введенную валюту {base}. Введите корректную валюту! ')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать введенное количество запрашиваемой валюты {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base