import pathlib
import time
import unittest

import common.utils

from src.file_content_monitor import FileContentMonitor


class MockProducer:
    def send(self, topic, value):
        pass


class TestFileContentMonitor(unittest.TestCase):
    producer = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.producer = MockProducer()
        cls.file_path = pathlib.Path(__file__).parent / "./test.txt"
        cls.content = ".123inside\nfile"

    def setUp(self):
        super().setUp()

        self.file_content_monitor = FileContentMonitor(self.producer)
        self.file_content_monitor.path = self.file_path

    def tearDown(self):
        super().tearDown()

        common.utils.remove_file(self.file_path)

    def test_Should_GetEmptyPath_When_PathWasNotSet(self):
        self.file_content_monitor = FileContentMonitor(self.producer)

        self.assertEqual("", self.file_content_monitor.path)

    def test_Should_GetPath_When_PathWasSet(self):
        self.assertEqual(self.file_path, self.file_content_monitor.path)

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
        common.utils.remove_file(self.file_path)
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
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(self.content)
        wait_monitoring_interval_time_with_buffer()

    def write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("")
        wait_monitoring_interval_time_with_buffer()

    def append_nothing_to_file_and_wait_monitoring_interval_time_with_buffer(self):
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write("")
        wait_monitoring_interval_time_with_buffer()

    def append_content_to_file_and_wait_monitoring_interval_time_with_buffer(self):
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(self.content)
        wait_monitoring_interval_time_with_buffer()


def wait_monitoring_interval_time_with_buffer():
    monitoring_interval_time = 5
    buffer = 1
    time.sleep(monitoring_interval_time + buffer)


if __name__ == '__main__':
    unittest.main()
