import requests


class Notifier:
    def __init__(self, events_handler):
        self.__events_handler = events_handler

        self.__observers = []
        # self.__responses = []

    @property
    def observers(self):
        return self.__observers

    def register_observer(self, observer):
        if observer not in self.observers:
            self.__observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
