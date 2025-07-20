#!/usr/bin/env python3
"""Fixtures for testing GithubOrgClient"""

org_payload = {
    "login": "testorg",
    "id": 123456,
    "url": "https://api.github.com/orgs/testorg",
    "repos_url": "https://api.github.com/orgs/testorg/repos",
    "description": "A test organization",
}

repos_payload = [
    {
        "id": 1,
        "name": "repo1",
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 2,
        "name": "repo2",
        "license": {"key": "mit"},
    },
    {
        "id": 3,
        "name": "repo3",
        "license": {"key": "apache-2.0"},
    },
    {
        "id": 4,
        "name": "repo4",
        "license": None,
    }
]

expected_repos = ["repo1", "repo2", "repo3", "repo4"]

apache2_repos = ["repo1", "repo3"]
