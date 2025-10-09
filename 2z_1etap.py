def parser(string):
    list = string.split(" ")
    return(list[2])

print("Параметры файла:")
with open("config.ini", "r") as file:
    file.readline()
    i = ""
    i = file.readline()
    if (i == ""):
        print("Ошибка: Пустое значение поля имя")
    else:
        print(i.rstrip("\n"))

    i = file.readline()
    if (i == ""):
        print("Ошибка: Неправильная ссылка или путь к файлу")
    else:
        print(i.rstrip("\n"))

    i = file.readline()
    if (parser(i)[:1] == "W" or parser(i)[:1] == "R"):
        print(i.rstrip("\n"))
    else:
        print("Ошибка: Некоректный режим работы с репазиторием")
    i = file.readline()
    if (i == ""):
        print("Ошибка: Пустое значение поля имя")
    else:
        print(i.rstrip("\n"))
    i = file.readline()
    if (i == ""):
        print("Ошибка: Пустое значение поля имя")
    else:
        print(i.rstrip("\n"))




