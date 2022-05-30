import unittest
from time import sleep
import os
from pathlib import Path

from src.file_content_monitor import FileContentMonitor


class TestFileContentMonitor(unittest.TestCase):
    path = None

    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    def tearDown(self):
        self.remove_file()

    @classmethod
    def set_test_arguments(cls):
        cls.path = Path(__file__).parent / "./test.txt"
        cls.content = ".123inside\nfile"

    @classmethod
    def set_tested_objects(cls):
        cls.file_content_monitor = FileContentMonitor(cls.path)

    @classmethod
    def set_test_expected_results(cls):
        pass

    def test_Should_GetEmptyContent_When_FileIsNotAvailable(self):
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetEmptyContent_When_NotAvailableFileIsCreated(self):
        wait_monitoring_interval_time_with_buffer()
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetEmptyContent_When_FileIsEmpty(self):
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetContent_When_EmptyFileContentIsUpdated(self):
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.append_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)

    def test_Should_GetContent_When_FileHasContent(self):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)

    def test_Should_GetEmptyContent_When_FileContentWasRemoved(self):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetEmptyContent_When_FileWasRemoved(self):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.remove_file()
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetTheSameContent_When_FileWasSavedWithoutChangingContent(self):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.append_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)

    def test_Should_GetUpdatedContent_When_FileContentWasAdded(self):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.append_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(2 * self.content, self.file_content_monitor.content)

    def write_content_to_file_and_wait_monitoring_interval_time_with_buffer(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(self.content)
        wait_monitoring_interval_time_with_buffer()

    def write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("")
        wait_monitoring_interval_time_with_buffer()

    def append_nothing_to_file_and_wait_monitoring_interval_time_with_buffer(self):
        with open(self.path, "a", encoding="utf-8") as file:
            file.write("")
        wait_monitoring_interval_time_with_buffer()

    def append_content_to_file_and_wait_monitoring_interval_time_with_buffer(self):
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(self.content)
        wait_monitoring_interval_time_with_buffer()

    def remove_file(self):
        if os.path.exists(self.path):
            os.remove(self.path)


def wait_monitoring_interval_time_with_buffer():
    monitoring_interval_time = 5
    buffer = 1
    sleep(monitoring_interval_time + buffer)


if __name__ == "__main__":
    unittest.main()
