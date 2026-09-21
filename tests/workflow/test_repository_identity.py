"""Focused preflight tests; Git transport is mocked, safety checks still execute."""
import os
import tempfile
import unittest
from unittest.mock import Mock

from test_reconciliation import r


class RepositoryIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = r.Repository(self.temp.name)
        self.head = "a" * 40
        self.config = {
            "schema_version": 1,
            "default_branch": "master",
            "github_repository": "example/portable",
            "expected_origin": "git@github-zuno-edu:example/portable.git",
        }
        self.origin = self.config["expected_origin"]
        self.top = self.repo.root.as_posix()
        self.repo.json = Mock(return_value=self.config)
        self.repo.git = Mock(side_effect=self.git)

    def git(self, *args):
        return {
            ("rev-parse", "--show-toplevel"): self.top,
            ("branch", "--show-current"): "master",
            ("status", "--porcelain", "--untracked-files=all"): "",
            ("ls-files", "--others", "--exclude-standard"): "",
            ("rev-parse", "HEAD"): self.head,
            ("remote", "get-url", "origin"): self.origin,
            ("rev-parse", "refs/heads/master"): self.head,
            ("rev-parse", "refs/remotes/origin/master"): self.head,
            ("ls-remote", "--exit-code", "origin", "refs/heads/master"):
                f"{self.head}\trefs/heads/master",
        }[args]

    def test_configured_alias_and_standard_github_origins_accepted(self):
        for origin in (self.origin, "git@github.com:example/portable.git",
                       "https://github.com/example/portable.git",
                       "https://github.com/example/portable"):
            with self.subTest(origin=origin):
                self.origin = origin
                self.assertEqual(self.repo.synchronize_check(), (self.head, self.config))
                self.repo.git.assert_any_call("ls-remote", "--exit-code", "origin", "refs/heads/master")

    def test_different_repository_and_unapproved_hosts_rejected(self):
        for origin in ("git@github.com:fork/portable.git",
                       "https://github.com/example/other.git",
                       "git@github-zuno-edu:example/other.git",
                       "git@unapproved:example/portable.git",
                       "https://github.com.evil.test/example/portable.git",
                       "https://evil.test/example/portable.git",
                       "https://github.com/example/portable.git?redirect=other"):
            with self.subTest(origin=origin):
                self.origin = origin
                with self.assertRaisesRegex(r.Blocked, "approved repository identity"):
                    self.repo.synchronize_check()

    def test_missing_identity_configuration_still_rejected(self):
        for key in ("expected_origin", "github_repository"):
            with self.subTest(key=key):
                original = self.config[key]
                self.config[key] = None
                with self.assertRaises(r.Blocked):
                    self.repo.synchronize_check()
                self.config[key] = original

    def test_equivalent_resolved_root_accepted(self):
        for top in (self.repo.root.as_posix(), str(self.repo.root),
                    str(self.repo.root) + os.sep + "."):
            with self.subTest(top=top):
                self.top = top
                self.assertEqual(self.repo.synchronize_check()[0], self.head)

    def test_different_root_rejected(self):
        self.top = str(self.repo.root / "other")
        with self.assertRaisesRegex(r.Blocked, "repository root"):
            self.repo.synchronize_check()


if __name__ == "__main__":
    unittest.main()
