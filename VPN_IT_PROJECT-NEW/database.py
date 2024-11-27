import json


class DataBase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__keys = dict()
        with open("keys.json") as keys_file:
            self.__keys = json.load(keys_file)

    def dump_keys(self):
        with open("keys.json", "w") as keys_file:
            json.dump(self.__keys, keys_file, indent=2)

    def add_key(self, key: str, key_name: str, ):
        self.__keys[key] = key_name

    def remove_key(self, key: str):
        if key in self.__keys:
            del self.__keys[key]

    def exist_key(self, key):
        return key in self.__keys

    @property
    def keys(self):
        return self.__keys


def __test_database1():
    db = DataBase()
    db.add_key("1923131238", "key0")
    db.remove_key("1923131238")
    db.dump_keys()
    print(db.keys)


if __name__ == "__main__":
    __test_database1()
