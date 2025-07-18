#!/usr/bin/env python3
"""Unit tests for utils module"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json, memoize, access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map function"""

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError with the correct message"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Get the key that failed and caused the exception
        self.assertEqual(str(cm.exception), repr(path[len(nested_map)]))


class TestGetJson(unittest.TestCase):
    """Test get_json with mocked requests.get"""

    @parameterized.expand([
        (
            "http://example.com",
            {"payload": True}
        ),
        (
            "http://holberton.io",
            {"payload": False}
        ),
    ])
    def test_get_json(self, test_url, test_payload):
        """Mock requests.get and test return of get_json"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get",
                   return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test suite for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method call."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            instance = TestClass()
            first = instance.a_property()
            second = instance.a_property()

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mocked.assert_called_once()
