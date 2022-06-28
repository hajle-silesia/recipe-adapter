import hashlib
import os
import threading
from time import sleep


class FileContentMonitor(threading.Thread):
    _content_default = ""

    def __init__(self, notifier):
        threading.Thread.__init__(self, daemon=True)

        self.__notifier = notifier

        self.__path = ""
        self.__monitoring_interval_time = 5
        self.__last_modification_time = 0
        self.__checksum = None
        self.__content = self._content_default

        self.start()

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def content(self):
        return self.__content

    def run(self):
        while True:
            self.__monitor_file()

    def __monitor_file(self):
        if os.path.exists(self.__path):
            if self.__file_changed():
                self.__update_data()
                self.__notify()
        else:
            self.__clear_content()

        self.__wait_time_interval()

    def __file_changed(self):
        self.__get_last_modification_time()

        if self.__modification_time_changed():
            self.__calculate_file_checksum()

            if self.__checksum_changed():
                return True

        return False

    def __get_last_modification_time(self):
        self.__new_last_modification_time = os.path.getmtime(self.__path)

    def __modification_time_changed(self):
        return True if self.__new_last_modification_time > self.__last_modification_time else False

    def __calculate_file_checksum(self):
        self.__read_file()
        self.__get_checksum()

    def __read_file(self):
        with open(self.__path, encoding="utf-8") as file:
            self.__new_content = file.read()

    def __get_checksum(self):
        self.__new_checksum = hashlib.sha256(self.__new_content.encode()).hexdigest()

    def __checksum_changed(self):
        return True if self.__new_checksum != self.__checksum else False

    def __update_data(self):
        self.__update_last_modification_time()
        self.__update_checksum()
        self.__update_content()

    def __update_last_modification_time(self):
        self.__last_modification_time = self.__new_last_modification_time

    def __update_checksum(self):
        self.__checksum = self.__new_checksum

    def __update_content(self):
        self.__content = self.__new_content

    def __notify(self):
        if self.content:
            self.__notifier.notify_observers(self.content)

    def __clear_content(self):
        if self.content != self._content_default:
            self.__content = self._content_default

    def __wait_time_interval(self):
        sleep(self.__monitoring_interval_time)
