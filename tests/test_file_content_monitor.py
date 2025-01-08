import pathlib
import unittest

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
        cls.nonempty_raw_content = ".123inside\nfile"

    def setUp(self):
        super().setUp()

        self.file_content_monitor = FileContentMonitor(self.producer)

    def test_Should_GetEmptyContent_When_UpdatedWithEmptyContent(self):
        self.file_content_monitor.update("")

        self.assertEqual("", self.file_content_monitor.content)

    def test_Should_GetContent_When_UpdatedWithNonemptyContent(self):
        self.file_content_monitor.update(self.nonempty_raw_content)

        self.assertEqual(self.nonempty_raw_content, self.file_content_monitor.content)


if __name__ == '__main__':
    unittest.main()
