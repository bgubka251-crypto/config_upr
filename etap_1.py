#Вариант 28

import os
import getpass
import socket

def expand(s:str):
    for k in os.environ:
        s = s.replace("$" + k, os.environ[k])
    return s

username = getpass.getuser()
hostname = socket.gethostname()


while True:
    raw = expand(input(username + "@" + hostname + ":~ $ "))
    cmd, *args = raw.split()
    if cmd == "exit":
        break
    if cmd == "ls":
        print(cmd, args)
    if cmd == "cd":
        print(cmd, args)
    else:
        print("Unsupported command: " + cmd)