from unittest.mock import patch, MagicMock
import unittest

import requests.exceptions
from requests.exceptions import Timeout

from main import (
    get_interest_fact, count_word_in_interest_fact, InterestFactException,
    TIMEOUT_EXCEPTION, CONNECTION_EXCEPTION, INTERNAL_SERVER_EXCEPTION, BAD_REQUEST_EXCEPTION
)

def mock_get_interest_fact():
    raise InterestFactException("Time has been limit reached")
class TestInterestFact(unittest.TestCase):

    def setUp(self):
        self.interest_fact = "Just not interest fact"
        self.word = "just"
        self.count = 1
        self.success_status = 200
        self.timeout_exception = TIMEOUT_EXCEPTION
        self.connection_exception = CONNECTION_EXCEPTION
        self.bad_request_exception = BAD_REQUEST_EXCEPTION
        self.server_exception = INTERNAL_SERVER_EXCEPTION

    @patch('main.get_interest_fact')
    def test_count_word_in_interest_fact(self, mock_get_interest_fact):
        mock_get_interest_fact.return_value = self.interest_fact

        count_word = count_word_in_interest_fact(word=self.word)

        self.assertEqual(count_word, self.count)

    @patch('main.get_interest_fact')
    def test_count_word_in_interest_fact_timeout_exception(self, mock_get_interest_fact):
        self.__check_exception(
            mock_get_interest_fact, 
            self.timeout_exception,
            count_word_in_interest_fact,
            self.word
        )

    @patch('main.get_interest_fact')
    def test_count_word_in_interest_fact_connection_exception(self, mock_get_interest_fact):
        self.__check_exception(
            mock_get_interest_fact, 
            self.connection_exception,
            count_word_in_interest_fact,
            self.word,
        )    

    @patch('main.get_interest_fact')
    def test_count_word_in_interest_fact_bad_request_exception(self, mock_get_interest_fact):
        self.__check_exception(
            mock_get_interest_fact, 
            self.bad_request_exception,
            count_word_in_interest_fact,
            self.word,
        )

    @patch('main.get_interest_fact')
    def test_count_word_in_interest_fact_server_exception(self, mock_get_interest_fact):
        self.__check_exception(
            mock_get_interest_fact, 
            self.server_exception,
            count_word_in_interest_fact,
            self.word,
        )

    @patch('main.requests')
    def test_get_interest_fact(self, mock_requests):
        mock_response = MagicMock(
            status_code=self.success_status,
            text=self.interest_fact
        )
        mock_requests.get.return_value = mock_response

        response = get_interest_fact()

        self.assertEqual(response, self.interest_fact)
    
    @patch('main.requests')
    def test_get_interest_fact_timeout_error(self, mock_requests):
        self.__check_exception_and_set_exception_for_get_interest(
            mock_requests,
            self.timeout_exception,
            get_interest_fact,
        )

    @patch('main.requests')
    def test_get_interest_fact_connection_error(self, mock_requests):
        self.__check_exception_and_set_exception_for_get_interest(
            mock_requests,
            self.connection_exception,
            get_interest_fact,
        )


    @patch('main.requests')
    def test_get_interest_fact_bad_request_error(self, mock_requests):
        self.__check_exception_and_set_exception_for_get_interest(
            mock_requests,
            self.bad_request_exception,
            get_interest_fact,
        )

    @patch('main.requests')
    def test_get_interest_fact_server_error(self, mock_requests):
        self.__check_exception_and_set_exception_for_get_interest(
            mock_requests,
            self.server_exception,
            get_interest_fact,
        )


    def __check_exception_and_set_exception_for_get_interest(self, mock_data, *args, **kwargs):
        mock_data.exceptions = requests.exceptions
        self.__check_exception(
            mock_data.get,
            *args,
            **kwargs
        )

    def __check_exception(
        self, 
        mock_data, 
        exception,
        func,
        *args,
        **kwargs,
    ):
        mock_data.side_effect = self.__given_side_effect_exception(exception)

        context = self.__when_catch_exception(func, *args, **kwargs)

        self.__then_equal_exception(msg_answer=str(context.exception), msg_exception=exception)
    
    def __given_side_effect_exception(self, msg_exception):
        return InterestFactException(msg_exception)

    def __when_catch_exception(self, func, *args, **kwargs):
        with self.assertRaises(InterestFactException) as context:
            func(*args, **kwargs)

        return context

    def __then_equal_exception(self, msg_answer, msg_exception):
        self.assertEqual(msg_answer, msg_exception)

if __name__ == "__main__":
    unittest.main()