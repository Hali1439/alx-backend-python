#!/usr/bin/env python3
"""
Unit test for utils.access_nested_map
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map  # Ensure utils.py has the function


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with different nested paths"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
