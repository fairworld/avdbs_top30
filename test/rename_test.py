import os

try:
    os.rename('1', '2')
except FileExistsError as e:
    print("File exist")