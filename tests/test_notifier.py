import unittest
from unittest import mock

from src.notifier import Notifier

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


@mock.patch("src.notifier.requests.post", side_effect=mocked_requests_post)
class TestNotifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        pass

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

        self.notifier = Notifier(None)

    def tearDown(self):
        super().tearDown()

    def test_Should_GetEmptyObservers_When_ObserversWereNotAdded(self, mock_get):
        self.assertEqual([], self.notifier.observers)

    def test_Should_GetObserver_When_ObserverWasAdded(self, mock_get):
        self.notifier.register_observer(url)

        self.assertEqual([url], self.notifier.observers)

    def test_Should_GetOneObserver_When_TheSameObserverWasAddedMultipleTimes(self, mock_get):
        self.notifier.register_observer(url)
        self.notifier.register_observer(url)

        self.assertEqual([url], self.notifier.observers)

    def test_Should_GetEmptyObservers_When_ObserverWasAddedAndRemoved(self, mock_get):
        self.notifier.register_observer(url)
        self.notifier.remove_observer(url)

        self.assertEqual([], self.notifier.observers)
