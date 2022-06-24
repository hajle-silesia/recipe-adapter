import os
import unittest
from pathlib import Path
from time import sleep
from unittest import mock

from src.file_content_monitor import FileContentMonitor

url = "http://subscriber/update"


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == url:
        return MockResponse(None, 204)
    else:
        return MockResponse(None, 404)


@mock.patch("src.file_content_monitor.requests.post", side_effect=mocked_requests_post)
class TestFileContentMonitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.path = Path(__file__).parent / "./test.txt"
        cls.content = ".123inside\nfile"

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

        self.file_content_monitor = FileContentMonitor(self.path, url)

    def tearDown(self):
        super().tearDown()

        remove_file(self.path)

    def test_Should_GetEmptyContent_When_FileIsNotAvailable(self, mock_get):
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)
        self.assertEqual(None, self.file_content_monitor.response)

    def test_Should_GetEmptyContent_When_NotAvailableFileIsCreated(self, mock_get):
        wait_monitoring_interval_time_with_buffer()
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)
        self.assertEqual(None, self.file_content_monitor.response)

    def test_Should_GetEmptyContent_When_FileIsEmpty(self, mock_get):
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)
        self.assertEqual(None, self.file_content_monitor.response)

    def test_Should_GetContent_When_EmptyFileContentIsUpdated(self, mock_get):
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.append_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)
        self.assertEqual(204, self.file_content_monitor.response.status_code)
        self.assertEqual(None, self.file_content_monitor.response.json())

    def test_Should_GetContent_When_FileHasContent(self, mock_get):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)
        self.assertEqual(204, self.file_content_monitor.response.status_code)
        self.assertEqual(None, self.file_content_monitor.response.json())

    def test_Should_GetEmptyContent_When_FileContentWasRemoved(self, mock_get):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.write_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)
        self.assertEqual(None, self.file_content_monitor.response)

    def test_Should_GetEmptyContent_When_FileWasRemoved(self, mock_get):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        remove_file(self.path)
        wait_monitoring_interval_time_with_buffer()

        self.assertEqual("", self.file_content_monitor.content)
        self.assertEqual(None, self.file_content_monitor.response)

    def test_Should_GetTheSameContent_When_FileWasSavedWithoutChangingContent(self, mock_get):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.append_nothing_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(self.content, self.file_content_monitor.content)
        self.assertEqual(None, self.file_content_monitor.response)

    def test_Should_GetUpdatedContent_When_FileContentWasAdded(self, mock_get):
        self.write_content_to_file_and_wait_monitoring_interval_time_with_buffer()
        self.append_content_to_file_and_wait_monitoring_interval_time_with_buffer()

        self.assertEqual(2 * self.content, self.file_content_monitor.content)
        self.assertEqual(204, self.file_content_monitor.response.status_code)
        self.assertEqual(None, self.file_content_monitor.response.json())

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


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def wait_monitoring_interval_time_with_buffer():
    monitoring_interval_time = 5
    buffer = 1
    sleep(monitoring_interval_time + buffer)
