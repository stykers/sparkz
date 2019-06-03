import json


def change_value(file, value, target):
    try:
        with open(file, "r") as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        raise FileNotFoundError("No such file or directory.")

    data[value] = target
    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)


def append_value(file, value, addition):
    try:
        with open(file, "r") as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        raise FileNotFoundError("No such file or directory.")

    data[value].append(addition)
    with open(file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)
