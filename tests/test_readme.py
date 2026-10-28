"""The README describes the plugin install, and the tarball machinery is gone.

Run: python3 -m unittest discover -s tests
"""
import os
import unittest

from _hygiene import problems

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Readme(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(REPO, "README.md"), encoding="utf-8") as fh:
            self.text = fh.read()

    def test_install_is_the_plugin_commands(self):
        self.assertIn("/plugin marketplace add", self.text)
        self.assertIn("/plugin install zettel@zettel", self.text)
        self.assertIn("zk init", self.text)

    def test_tarball_install_is_gone(self):
        for stale in ("tar xzf", "install.sh", "package.sh", "ln -sf"):
            self.assertNotIn(stale, self.text, stale)
        self.assertFalse(os.path.exists(os.path.join(REPO, "install.sh")))
        self.assertFalse(os.path.exists(os.path.join(REPO, "package.sh")))

    def test_nothing_personal(self):
        self.assertEqual(problems(self.text), [])


if __name__ == "__main__":
    unittest.main()
