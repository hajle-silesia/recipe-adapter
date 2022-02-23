import unittest
from time import sleep
import os

from app.src.file_content_monitor import FileContentMonitor


class TestFileContentMonitor(unittest.TestCase):
    def setUp(self):
        self.set_test_arguments()
        self.set_tested_objects()
        self.set_test_expected_results()

    def tearDown(self):
        self.remove_file()

    def set_test_arguments(self):
        self.path = "./test.txt"
        self.content = ".123inside\nfile"

    def set_tested_objects(self):
        self.file_content_monitor = FileContentMonitor(self.path)

    def set_test_expected_results(self):
        pass

    def test_Should_GetNoContent_When_FileIsNotAvailable(self):
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetNoContent_When_NotAvailableFileIsCreated(self):
        wait_monitoring_interval_time_with_buffer()
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetNoContent_When_FileIsEmpty(self):
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetContent_When_EmptyFileContentIsUpdated(self):
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.append_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)

    def test_Should_GetContent_When_FileHasContent(self):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)

    def test_Should_GetNoContent_When_FileContentWasRemoved(self):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetNoContent_When_FileWasRemoved(self):
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
    sleep(6)
