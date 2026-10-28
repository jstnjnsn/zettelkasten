"""The generated register card must not claim the CLI lives in the vault.

Run: python3 -m unittest discover -s tests
"""
import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZK = os.path.join(REPO, "bin", "zk")


class Register(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.vault = os.path.join(self.tmp, "vault")
        subprocess.run([ZK, "init"], capture_output=True, text=True,
                       env={"PATH": os.environ["PATH"], "ZK_VAULT": self.vault}, check=True)
        r = subprocess.run([ZK, "register", "demo"], capture_output=True, text=True,
                           env={"PATH": os.environ["PATH"], "ZK_VAULT": self.vault})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.card = r.stdout

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_card_points_at_the_skill_not_a_vault_binary(self):
        self.assertNotIn(os.path.join(self.vault, "bin"), self.card)
        self.assertNotIn("bin/zk", self.card)
        self.assertIn("zettel", self.card)

    def test_card_still_names_the_vault_and_hubs(self):
        self.assertIn(self.vault, self.card)
        self.assertIn("`zk show global`", self.card)


if __name__ == "__main__":
    unittest.main()
