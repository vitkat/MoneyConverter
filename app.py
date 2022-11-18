import telebot

from config import keys, TOKEN

from extension import APIExtension, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'go'])
def help(message: telebot.types.Message):
    text = 'Здраствуйте! Я бот который может помочь Вам сделать конверсию валют по актуальному курсу. Перед началом работы введите команду в следующем формате (Пример: доллар евро 4):' \
           ' \n- <Название валюты, стоимость которой Вы хотите узнать>  \n- <Название валюты, которую конвертируем> ' \
           ' \n- <Количество первой валюты>\n \
 Список доступных валют: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# base, quote, amount = message.text.split(' ')
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIExtension('Неверно, введите корректные данные')


        base, quote, amount = values
        total_base = MoneyConverter.get_price(base, quote, amount)
    except APIExtension as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить,введено отрицательное число, ошибка: \n{e}')
    else:
        text = f'Сумма {amount} {quote} в конверции на  {base} составит: {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)
