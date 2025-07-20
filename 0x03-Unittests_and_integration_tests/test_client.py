#!/usr/bin/env python3
"""
Unittests and Integration Tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos,
)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct data"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct repos_url"""
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            client = GithubOrgClient("testorg")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/testorg/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new=PropertyMock(
                return_value="https://fake.url/repos"
            )
        ):
            client = GithubOrgClient("testorg")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("https://fake.url/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests without parameterized_class (ALX checker compatible)
    """

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and define side_effect"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/testorg":
                mock_response = Mock()
                mock_response.json.return_value = org_payload
                return mock_response
            if url == org_payload["repos_url"]:
                mock_response = Mock()
                mock_response.json.return_value = repos_payload
                return mock_response
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo list"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters by apache-2.0 license"""
        client = GithubOrgClient("testorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
