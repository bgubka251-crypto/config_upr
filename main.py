import os
import getpass
import socket
#import sys
import argparse
import yaml
#import subprocess
#from pathlib import Path


def expand(s: str):
    for k in os.environ:
        s = s.replace("$" + k, os.environ[k])
    return s


def load_config(config_path):
    #Загрузка конфигурации из YAML файла
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Ошибка чтения конфигурационного файла {config_path}: {e}")
        return {}


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Эмулятор командной оболочки')
    parser.add_argument('--vfs-path', help='Путь к физическому расположению VFS')
    parser.add_argument('--script-path', default= 'startup_script.txt' ,help='Путь к стартовому скрипту')
    parser.add_argument('--config-path', default='config.yaml', help='Путь к конфигурационному файлу')

    return parser.parse_args()


def execute_script(script_path, username, hostname):
    """Выполнение стартового скрипта"""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Пропуск пустых строк и комментариев
            if not line or line.startswith('#'):
                continue

            # Отображение ввода (имитация пользовательского ввода)
            print(f"{username}@{hostname}:~ $ {line}")

            # Обработка команд
            cmd, *args = line.split()

            if cmd == "exit":
                break
            elif cmd == "ls":
                # Эмуляция вывода ls
                try:
                    files = os.listdir('.')
                    for file in files:
                        print(file)
                except Exception as e:
                    print(f"Ошибка выполнения ls: {e}")
            elif cmd == "cd":
                # Эмуляция смены директории
                try:
                    if args:
                        os.chdir(args[0])
                        print(f"Переход в директорию: {args[0]}")
                    else:
                        os.chdir(os.path.expanduser("~"))
                        print("Переход в домашнюю директорию")
                except Exception as e:
                    print(f"Ошибка выполнения cd: {e}")
            elif cmd == "pwd":
                # Показать текущую директорию
                print(os.getcwd())
            elif cmd == "echo":
                # Эмуляция echo
                print(' '.join(args))
            else:
                print(f"Unsupported command: {cmd}")

    except Exception as e:
        print(f"Ошибка во время исполнения стартового скрипта {script_path}: {e}")
        return False

    return True


def main():
    # Парсинг аргументов командной строки
    args = parse_arguments()

    print("=== Отладочный вывод параметров ===")
    print(f"Аргументы командной строки:")
    print(f"  VFS путь: {args.vfs_path}")
    print(f"  Путь к скрипту: {args.script_path}")
    print(f"  Конфигурационный файл: {args.config_path}")

    # Загрузка конфигурации из файла
    config = {}
    if os.path.exists(args.config_path):
        config = load_config(args.config_path)
        print(f"\nКонфигурация из файла {args.config_path}:")
        print(f"  VFS путь: {config.get('vfs_path')}")
        print(f"  Путь к скрипту: {config.get('script_path')}")
    else:
        print(f"\nКонфигурационный файл {args.config_path} не найден")

    # Определение финальных параметров (приоритет файла над командной строкой)
    vfs_path = config.get('vfs_path') or args.vfs_path or '.'
    script_path = config.get('script_path') or args.script_path

    print(f"\nФинальные параметры:")
    print(f"  VFS путь: {vfs_path}")
    print(f"  Путь к скрипту: {script_path}")
    print("====================================\n")

    # Установка VFS пути как текущей рабочей директории
    try:
        os.chdir(vfs_path)
        print(f"Установлена рабочая директория: {os.getcwd()}")
    except Exception as e:
        print(f"Ошибка установки VFS пути {vfs_path}: {e}")
        return

    username = getpass.getuser()
    hostname = socket.gethostname()

    # Если указан скрипт - выполняем его, иначе интерактивный режим
    if script_path:
        if not execute_script(script_path, username, hostname):
            return
        print("\nСкрипт выполнен. Переход в интерактивный режим...\n")

    # Интерактивный режим
    while True:
        try:
            raw = expand(input(username + "@" + hostname + ":~ $ "))
            cmd, *args = raw.split()

            if cmd == "exit":
                break
            elif cmd == "ls":
                try:
                    files = os.listdir('.')
                    for file in files:
                        print(file)
                except Exception as e:
                    print(f"Ошибка: {e}")
            elif cmd == "cd":
                try:
                    if args:
                        os.chdir(args[0])
                    else:
                        os.chdir(os.path.expanduser("~"))
                except Exception as e:
                    print(f"Ошибка: {e}")
            elif cmd == "pwd":
                print(os.getcwd())
            elif cmd == "echo":
                print(' '.join(args))
            else:
                print("Unsupported command: " + cmd)

        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()