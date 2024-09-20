import argparse
from tarfile import TarFile

parser = argparse.ArgumentParser()
parser.add_argument("username", help="Имя пользователя")
parser.add_argument("hostname", help="Имя компьютера")
parser.add_argument("path_to_archive", help="Путь до архива")
parser.add_argument("path_to_script", help="Путь до стартового скрипта")

args = parser.parse_args()

print(args.username, args.hostname, args.path_to_archive, args.path_to_script)
