#!/usr/bin/env python3
"""Module containing utility functions for working with nested maps and APIs."""

import requests
from typing import Mapping, Any, Tuple, Dict

def access_nested_map(nested_map: Mapping, path: Tuple) -> Any:
    # Traverses the path to access deeply nested values
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url: str) -> Dict:
    # Fetches JSON data from the given URL
    response = requests.get(url)
    response.raise_for_status()  # Good practice, ensures failed requests raise an error
    return response.json()
