from datetime import datetime
import time

print(time.ctime())
name = input('Введите свой логин: ')
time_list = time.localtime()
hours = time_list[3]
if 5 <= int(hours) <= 12:
    print("Доброго утра,", name)
elif 12 <= int(hours) <= 18:
    print("Доброго дня,", name)
elif 18 <= int(hours) <= 22:
    print("Доброго вечера,", name)
else:
    print("Доброй ночи,", name)
