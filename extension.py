import json
import requests
from config import *

class APIExtension(Exception):
    pass


class MoneyConverter:
   @staticmethod
   def get_price(base: str, quote: str, amount: str):

       if quote == base:
           raise APIExtension(f'Введите различные валюты: {base}.')

       # quote_ticker, base_ticker = keys[quote], keys[base]
       try:
           base_ticker = keys[base]
       except KeyError:
           raise APIExtension(f'Не удалось обработать, введена та же валюта {base}')
       try:
           quote_ticker = keys[quote]
       except KeyError:
           raise APIExtension(f'Не удалось обработать, введена та же валюта {quote}')
       try:
           amount = float(amount)


       except ValueError:
           raise APIException(f'Не удалось обработать количество {amount}')
       if amount < 0:
           raise APIException(f'Отрицательное количество валюты. Попробуйте еще раз')
       if amount == float('inf'):
           raise APIException(f'Вы ввели недопустимо длинное число')

       r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
       total_base = json.loads(r.content)[keys[base]]

       total_base = total_base * amount

       return total_base
