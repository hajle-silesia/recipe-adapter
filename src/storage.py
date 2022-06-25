import json


class Storage:
    def __init__(self):
        self.path = ""

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    def store_data(self, data):
        if data:
            self.__dump_data(data)

    def __dump_data(self, data):
        if self.path:
            with open(self.path, "w", encoding="utf-8") as data_json:
                json.dump(data, data_json)
