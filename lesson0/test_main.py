from unittest.mock import patch, Mock
import unittest

import requests.exceptions
from requests.exceptions import Timeout

from main import (
    get_interest_fact, count_word_in_interest_fact, InterestFactException,
    TIMEOUT_EXCEPTION, CONNECTION_EXCEPTION, BAD_REQUEST_EXCEPTION
)


class TestInterestFact(unittest.TestCase):

    def setUp(self):
        self.interest_fact = "Just not interest fact"
        self.word = "just"
        self.count = 1
        self.success_status = 200
        self.timeout_exception = TIMEOUT_EXCEPTION
        self.connection_exception = CONNECTION_EXCEPTION
        self.bad_request_exception = BAD_REQUEST_EXCEPTION
        self.exceptions = [self.timeout_exception, self.connection_exception, 
        self.bad_request_exception]

    @patch('main.get_interest_fact')
    def test_count_word_in_interest_fact(self, mock_get_interest_fact):
        mock_get_interest_fact.return_value = self.interest_fact

        count_word = count_word_in_interest_fact(word=self.word)

        self.assertEqual(count_word, self.count)

    @patch('main.get_interest_fact')
    def test_count_word_in_interest_fact_exceptions(self, mock_get_interest_fact):
        for exception in self.exceptions:
            with self.subTest(exception=exception):
                self._check_exception(
                    mock_get_interest_fact, 
                    exception,
                    count_word_in_interest_fact,
                    self.word
                )

    @patch('main.requests')
    def test_get_interest_fact(self, mock_requests):
        mock_response = Mock(
            status_code=self.success_status,
            text=self.interest_fact
        )
        mock_requests.get.return_value = mock_response

        response = get_interest_fact()

        self.assertEqual(response, self.interest_fact)
    
    @patch('main.requests')
    def test_get_interest_fact_exceptions(self, mock_requests):
        for exception in self.exceptions:
            with self.subTest(exception=exception):
                mock_requests.exceptions = requests.exceptions
                self._check_exception(
                    mock_requests.get,
                    exception,
                    get_interest_fact,
                )

    def _check_exception(self, mock_data, exception, func, *args, **kwargs):
        mock_data.side_effect = self._given_side_effect_exception(exception)

        context = self._when_catch_exception(func, *args, **kwargs)

        self._then_equal_exception(msg_answer=str(context.exception), msg_exception=exception)
    
    def _given_side_effect_exception(self, msg_exception):
        return InterestFactException(msg_exception)

    def _when_catch_exception(self, func, *args, **kwargs):
        with self.assertRaises(InterestFactException) as context:
            func(*args, **kwargs)

        return context

    def _then_equal_exception(self, msg_answer, msg_exception):
        self.assertEqual(msg_answer, msg_exception)

if __name__ == "__main__":
    unittest.main()