import os

items = {}
with os.open("private/creds.init") as f:
    for line in f:
       (key, val) = line.split('=')
       items[int(key)] = val

