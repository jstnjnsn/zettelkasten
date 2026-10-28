"""The example vault under examples/vault is the bench's self-test.

It must be hygienic, carry nothing personal, and every starter question must be
answerable by zk traversal. Run: python3 -m unittest discover -s tests
"""
import os
import subprocess
import unittest

from _hygiene import problems

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(REPO, "examples", "vault")
ENV = {"PATH": os.environ["PATH"], "HOME": REPO, "ZK_VAULT": FIXTURE}


def run(tool, *args):
    return subprocess.run([os.path.join(REPO, "bin", tool), *args],
                          capture_output=True, text=True, env=ENV)


class BenchFixture(unittest.TestCase):
    def test_fixture_is_hygienic(self):
        r = run("zk", "check")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0 problems, 0 orphans", r.stdout)

    def test_fixture_has_more_than_a_hub(self):
        r = run("zk", "list")
        self.assertGreaterEqual(len(r.stdout.strip().splitlines()), 6, r.stdout)

    def test_every_starter_question_is_answered_by_traversal(self):
        r = run("zk_bench", "--arms", "zk")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("misses", r.stdout, r.stdout)
        self.assertNotIn("ranking gap", r.stdout, r.stdout)

    def test_nothing_personal(self):
        for root, _d, files in os.walk(FIXTURE):
            for f in files:
                with open(os.path.join(root, f), encoding="utf-8") as fh:
                    text = fh.read()
                self.assertEqual(problems(text), [], f)


if __name__ == "__main__":
    unittest.main()
