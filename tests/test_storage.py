import json
import os
import unittest
from pathlib import Path

from src.storage import Storage


class TestStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.path = Path(__file__).parent / "./data.json"
        cls.data = ["a", "b", "c"]

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

        self.storage = Storage()

    def tearDown(self):
        super().tearDown()

        remove_file(self.path)

    def test_Should_GetEmptyPath_When_PathWasNotSet(self):
        self.assertEqual("", self.storage.path)

    def test_Should_GetPath_When_PathWasSet(self):
        self.storage.path = self.path

        self.assertEqual(self.path, self.storage.path)

    def test_Should_NotCreateDataFile_When_OnlyPathWasNotSet(self):
        self.storage.store_data(self.data)

        self.assertEqual(False, os.path.exists(self.path))

    def test_Should_NotCreateDataFile_When_OnlyDataWasNotSet(self):
        self.storage.path = self.path
        self.storage.store_data(None)

        self.assertEqual(False, os.path.exists(self.path))

    def test_Should_NotCreateDataFile_When_PathAndDataWereNotSet(self):
        self.assertEqual(False, os.path.exists(self.path))

    def test_Should_CreateDataFile_When_PathAndDataWereSet(self):
        self.storage.path = self.path
        self.storage.store_data(self.data)

        self.assertEqual(True, os.path.exists(self.path))

    def test_Should_StoreData_When_PathAndDataWereSet(self):
        self.storage.path = self.path
        self.storage.store_data(self.data)

        with open(self.path, encoding="utf-8") as data_file:
            data = json.load(data_file)

        self.assertEqual(self.data, data)


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
