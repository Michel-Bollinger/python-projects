"""
This script is designed to work with VK API methods. 
The script makes a request to obtain the public data 
of the selected user and them's friends. Then, using the date of birth, 
compiles a sorted list of tuples of the form: (age, number)
"""

from operator import itemgetter
import requests

# скрипт в виде одной процедуры. почему так?
# а почему бы и нет?
def calc_age(uid):
    # это решение задания на Курсере, поэтому обе ссылки
    # имеют конкретные параметры, а не абстрагированные.
    # первая - позволяет найти числовой id 
    # по буквенному id страницы, вторая - json списка друзей.
    _USER_ID_URL = f"https://api.vk.com/method/users.get?v=5.71" \
        f"&access_token=05ebec0b05ebec0b05ebec0b9405" \
        f"838f2b005eb05ebec0b59b925c9620154ef65ff7414" \
        f"&user_ids={uid}"
    _FRIENDS_URL = "https://api.vk.com/method/friends.get?v=5.71" \
                   "&access_token=05ebec0b05ebec0b05ebec0b9405" \
                   "838f2b005eb05ebec0b59b925c9620154ef65ff7414" \
                   "&user_id={}&fields=bdate"
    
    # мы не знаем, буквенный id у нас (строка)
    # или числовой, поэтому приводим к общему типу
    identificator = str(uid)
    
    # проверяем, является ли id - числом
    # если нет, узнаем его
    if not uid.isdigit():
        req = requests.get(_USER_ID_URL).json()
        identificator = req["response"][0]["id"]
    
    # получаем по числовому id друзей юзера
    req = requests.get(_FRIENDS_URL.format(identificator)).json()
    # проверяем, не пуст ли словарь с друзьями юзера
    # обычно это значит, что друзья скрыты
    if req["response"].get("items") is None:
        return []

    # создаем список всех возрастов
    # и кортеж из уникальных возрастов
    all_ages = []
    unique_ages = set()
    for friend_dict in req["response"]["items"]:
        # пропускаем пользователя, 
        # если не указана дата рождения
        if friend_dict.get("bdate") is None:
            continue
        # и если указаны только день и месяц
        bday_list = friend_dict["bdate"].split(".")
        if len(bday_list) < 3:
            continue
        # получаем возраст и добавляем каждый 
        # в созданные структуры данных
        friend_age = 2019 - int(bday_list[2])
        all_ages.append(friend_age)
        unique_ages.add(friend_age)
    
    # итерируемся по уникальным возрастам
    # и считаем в списке всех возрастов, как часто встречается
    # формируем список (возраст, частота)
    age_and_count = []
    for age in unique_ages:
        count = all_ages.count(age)
        age_and_count.append((age, count))

    # сортируем спиоск сначала по возрасту
    # а затем по частоте, начиная с наибольшей
    ages_sorted = sorted(age_and_count, key=itemgetter(0))
    ages_sorted = sorted(ages_sorted, key=itemgetter(1), reverse=True)

    return ages_sorted


if __name__ == '__main__':
    res = calc_age(input())
    print(res)
