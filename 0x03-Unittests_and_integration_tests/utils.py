#!/usr/bin/env python3
"""Utilities for working with nested maps."""


from typing import Mapping, Any, Tuple


def access_nested_map(nested_map: Mapping, path: Tuple) -> Any:
    """
    Access a value in a nested map with a sequence of keys (path).

    Args:
        nested_map (Mapping): The map to traverse.
        path (Tuple): A tuple of keys representing the path to the desired value.

    Returns:
        Any: The value at the end of the path.

    Raises:
        KeyError: If a key in the path does not exist.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map
