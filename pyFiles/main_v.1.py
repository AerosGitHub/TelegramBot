import config_inf
import telebot
import weather_modul
import os
from YandexTranslator import yandex_translator_modul
import db_modul
from telebot import types


def upd_users_base_weather():
    global users_base_weather
    users_base_weather.clear()
    for _ in db_modul.get_all_inf_from_db():
        user_id, user_city = _[0], _[1]
        users_base_weather[user_id] = user_city


def main():
    bot = telebot.TeleBot(config_inf.config['token'])

    @bot.message_handler(commands=['dev'])
    def inf_for_dev(inf):
        bot.send_message(inf.chat.id, inf)

    @bot.message_handler(commands=['start'])
    def greeting(inf):
        bot.send_message(inf.chat.id, 'Привет! Я сейчас нахожусь в разработке, но ты уже можешь использовать некоторые'
                                      ' мои функции')

    @bot.message_handler(commands=['weather'])
    def weather_work(inf):
        upd_users_base_weather()
        if inf.chat.id in users_base_weather:
            try:
                weather_inf_for_user = weather_modul.get_weather(users_base_weather[inf.chat.id])
                bot.send_message(inf.chat.id,
                                 f'Сейчас в {users_base_weather[inf.chat.id]} {weather_inf_for_user[0]} и '
                                 f'{weather_inf_for_user[1]}°C')
            except:
                bot.send_message(inf.chat.id,
                                 'Установлен неправильный город. Воспользуйтель командой /setcity и укажите правильное '
                                 'название города')

        else:
            bot.send_message(inf.chat.id, 'Установите город командой /setcity, чтобы посмотреть температуру в нём')

    @bot.message_handler(commands=['setcity'])
    def add_user_city_in_database(inf):
        upd_users_base_weather()
        if inf.chat.id in users_base_weather:
            db_modul.delete_inf_from_db(inf.chat.id)
        users_modes[inf.chat.id] = 'setcity'
        bot.send_message(inf.chat.id, 'Напишите свой город')

    @bot.message_handler(commands=['save'])
    def safe_message(inf):
        users_modes[inf.chat.id] = 'save'
        bot.send_message(inf.chat.id, 'Напишито то, что должен сохранить бот')

    @bot.message_handler(commands=['give', 'delete'])
    def work_with_saved_file(inf):
        if inf.text == '/give':
            bot.send_message(inf.chat.id, open(f'{inf.chat.id}').read())
        elif inf.text == '/delete':
            os.remove(f'{inf.chat.id}')
            bot.send_message(inf.chat.id, 'Текст успешно удалён')

    @bot.message_handler(commands=['translate', 'stop'])
    def translate_message(inf):
        if inf.text == '/translate':
            users_modes[inf.chat.id] = 'translate'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton('/stop')
            markup.row(button)
            bot.send_message(inf.chat.id,
                             'Вы включили режим перевода. С этого момента каждое сообщение будет переводится ботом',
                             reply_markup=markup)
        else:
            users_modes.pop(inf.chat.id)
            markup = types.ReplyKeyboardRemove()
            bot.send_message(inf.chat.id, 'Вы выключили режим перевода', reply_markup=markup)

    @bot.message_handler(commands=['help'])
    def send_help_message(inf):
        text_of_file = open('command list', encoding='UTF-8').read()
        bot.send_message(inf.chat.id, text_of_file)

    @bot.message_handler()
    def start(inf):
        try:
            if users_modes[inf.chat.id] == 'save':
                open(f'{inf.chat.id}', 'w').write(inf.text)
                bot.send_message(inf.chat.id, 'Текст успешно сохранён')
                users_modes.pop(inf.chat.id)
            elif users_modes[inf.chat.id] == 'setcity':
                translate_frase = yandex_translator_modul.do_translate(inf.text).capitalize()
                db_modul.add_inf_in_db((inf.chat.id, translate_frase))
                upd_users_base_weather()
                bot.send_message(inf.chat.id, 'Город установлен')
                users_modes.pop(inf.chat.id)
            elif users_modes[inf.chat.id] == 'translate':
                translate_frase = yandex_translator_modul.do_translate(inf.text).capitalize()
                bot.send_message(inf.chat.id, translate_frase)
        except Exception as e:
            print(e)

    bot.polling(non_stop=True)


if __name__ == '__main__':
    users_base_weather = {}
    users_modes = {}
    main()
