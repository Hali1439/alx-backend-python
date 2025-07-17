#!/usr/bin/env python3
"""Module containing utility functions for working with nested maps and APIs."""

import requests
from functools import wraps
from typing import Mapping, Any, Tuple, Dict, Callable


def access_nested_map(nested_map: Mapping, path: Tuple) -> Any:
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def memoize(method: Callable) -> Callable:
    """Decorator to cache method outputs."""
    attr_name = f"_memoized_{method.__name__}"

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
