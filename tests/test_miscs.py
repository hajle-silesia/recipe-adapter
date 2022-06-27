import os
import unittest
from pathlib import Path

from miscs import remove_file


class TestMiscs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.path = Path(__file__).parent / "./test.txt"

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_Should_NotCauseError_When_FileDoesNotExist(self):
        remove_file(self.path)

    def test_Should_RemoveFile_When_FileExists(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("test")

        remove_file(self.path)

        self.assertEqual(False, os.path.exists(self.path))
