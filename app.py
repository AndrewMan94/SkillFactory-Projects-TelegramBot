import telebot
from Config import keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '''Приветствую Вас! Здесь Вы сможете рассчитать интересующее Вас количество денежных средств в разных валютах!\
     \nИтак, приступим! \nДля того, чтобы начать - введите мне команду в формате:\n<имя валюты> *пробел*
<в какую валюту нужно перевести (для дробного расчета используете, например: '1.1' )> *пробел*   \
   \n <количество переводимой валюты>\
   \nУвидеть список всех доступных валют: /values'''
    bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
   text = 'Доступные валюты:'
   for key in keys.keys():
       text = '\n'.join((text,key, ))
   bot.send_message(message.chat.id,text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
      try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Вы ввели слишком много параметров для расчета.')
        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
      except APIException as e:
          bot.send_message(message.chat.id, f'Неправильный ввод со стороны пользователя.\n{e}')
      except Exception as e:
          bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
      else:
        number = total_base * float(amount)
        number = round(number, 4)
        text = f'Цена {amount} {quote} в {base} равняется {number}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)