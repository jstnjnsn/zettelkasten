"""zk init creates an empty vault with a generic global hub.

Run: python3 -m unittest discover -s tests
"""
import os
import shutil
import subprocess
import tempfile
import unittest

from _hygiene import problems

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZK = os.path.join(REPO, "bin", "zk")


class Init(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.home = os.path.join(self.tmp, "home")
        os.makedirs(self.home)
        self.vault = os.path.join(self.home, ".claude", "zettel")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def zk(self, *args, **env):
        return subprocess.run([ZK, *args], capture_output=True, text=True,
                              env={"PATH": os.environ["PATH"], "HOME": self.home, **env})

    def test_init_creates_a_vault_that_passes_check(self):
        r = self.zk("init")
        self.assertEqual(r.returncode, 0, r.stderr)
        hub = os.path.join(self.vault, "notes", "global", "global.md")
        self.assertTrue(os.path.isfile(hub), r.stdout)
        self.assertIn(self.vault, r.stdout)
        check = self.zk("check")
        self.assertEqual(check.returncode, 0, check.stdout)
        self.assertIn("1 notes, 0 problems, 0 orphans", check.stdout)
        show = self.zk("show", "global")
        self.assertEqual(show.returncode, 0, show.stderr)
        self.assertIn("type: hub", show.stdout)

    def test_hub_is_generic(self):
        self.zk("init")
        with open(os.path.join(self.vault, "notes", "global", "global.md"), encoding="utf-8") as fh:
            hub = fh.read()
        self.assertEqual(problems(hub), [])

    def test_init_never_touches_an_existing_vault(self):
        d = os.path.join(self.vault, "notes", "global")
        os.makedirs(d)
        mine = "---\ntitle: mine\ndescription: my own hub\ntype: hub\nproject: global\n---\nkeep me\n"
        with open(os.path.join(d, "global.md"), "w", encoding="utf-8") as fh:
            fh.write(mine)
        r = self.zk("init")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("already", r.stdout)
        with open(os.path.join(d, "global.md"), encoding="utf-8") as fh:
            self.assertEqual(fh.read(), mine)

    def test_init_respects_zk_vault(self):
        elsewhere = os.path.join(self.tmp, "elsewhere")
        r = self.zk("init", ZK_VAULT=elsewhere)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.isfile(os.path.join(elsewhere, "notes", "global", "global.md")))
        self.assertFalse(os.path.exists(self.vault))

    def test_missing_vault_error_points_at_init(self):
        r = self.zk("list")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("zk init", r.stderr)


if __name__ == "__main__":
    unittest.main()
