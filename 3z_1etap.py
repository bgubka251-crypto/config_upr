import argparse
import re

class Command:
    def __init__(self, opcode, fields):
        self.opcode = opcode
        self.fields = fields

    def __repr__(self):
        pairs = ", ".join(f"{k}={v}" for k, v in self.fields.items())
        return f"{self.opcode}({pairs})"


def parse_line(line: str) -> Command:
    line = line.strip()

    if not line or line.startswith("#"):
        return None

    m = re.match(r"([A-Z]+)\s*(.*)", line)
    if not m:
        raise ValueError(f"Не могу разобрать строку: {line}")

    opcode = m.group(1)
    args_part = m.group(2).strip()

    args = {}

    if args_part:
        parts = args_part.split(",")
        for p in parts:
            name, value = p.split("=")
            args[name.strip()] = int(value.strip())

    A_values = {
        "LOAD": 0,
        "READ": 8,
        "WRITE": 4,
        "MUL": 6,
    }

    if opcode not in A_values:
        raise ValueError(f"Неизвестная команда {opcode}")

    args["A"] = A_values[opcode]

    return Command(opcode, args)

def parse_file(path: str):
    commands = []
    with open(path, "r") as f:
        for line in f:
            cmd = parse_line(line)
            if cmd:
                commands.append(cmd)
    return commands

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Файл программы")
    parser.add_argument("output", help="Файл результата (бинарный)")
    parser.add_argument("--test", action="store_true", help="Тестовый режим")
    args = parser.parse_args()

    commands = parse_file(args.source)

    if args.test:
        print("Промежуточное представление:")
        for i, cmd in enumerate(commands, 1):
            print(f"{i}) {cmd}")
        return

    with open(args.output, "wb") as f:
        f.write(b"")

main()
