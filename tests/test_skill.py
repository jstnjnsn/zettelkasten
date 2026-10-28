"""The shipped skill must work from a plugin install and carry nothing personal.

Run: python3 -m unittest discover -s tests
"""
import os
import re
import unittest

from _hygiene import problems

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(REPO, "skills", "zettel", "SKILL.md")


class Skill(unittest.TestCase):
    def setUp(self):
        with open(SKILL, encoding="utf-8") as fh:
            self.text = fh.read()

    def test_frontmatter(self):
        m = re.match(r"---\nname: zettel\ndescription: .+\n---\n", self.text)
        self.assertIsNotNone(m, self.text[:200])

    def test_tool_is_addressed_through_the_plugin_root(self):
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/bin/zk", self.text)
        self.assertNotIn("<vault>/bin/zk", self.text)
        self.assertNotIn("add to PATH", self.text)

    def test_vault_resolution_matches_the_tool(self):
        self.assertNotIn("directory containing", self.text)
        self.assertIn("~/.claude/zettel", self.text)
        self.assertIn("zk init", self.text)

    def test_nothing_personal(self):
        self.assertEqual(problems(self.text), [])


if __name__ == "__main__":
    unittest.main()
