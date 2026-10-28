"""Where zk looks for the vault.

Run: python3 -m unittest discover -s tests
"""
import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZK = os.path.join(REPO, "bin", "zk")


def write_note(vault, project, slug):
    d = os.path.join(vault, "notes", project)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, slug + ".md"), "w", encoding="utf-8") as fh:
        fh.write(f"---\ntitle: {slug}\ndescription: {slug} desc\ntype: hub\nproject: {project}\n---\nbody\n")


class VaultResolution(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.home = os.path.join(self.tmp, "home")
        os.makedirs(self.home)
        # a copy of the tool with a vault-shaped sibling, as a checkout or a plugin cache would have
        self.install = os.path.join(self.tmp, "install")
        os.makedirs(os.path.join(self.install, "bin"))
        shutil.copy(ZK, os.path.join(self.install, "bin", "zk"))
        write_note(self.install, "global", "sibling_note")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_zk(self, *args, **env):
        e = {"PATH": os.environ["PATH"], "HOME": self.home, **env}
        return subprocess.run([os.path.join(self.install, "bin", "zk"), *args],
                              capture_output=True, text=True, env=e)

    def test_env_var_wins(self):
        vault = os.path.join(self.tmp, "elsewhere")
        write_note(vault, "global", "env_note")
        r = self.run_zk("list", ZK_VAULT=vault)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("env_note", r.stdout)
        self.assertNotIn("sibling_note", r.stdout)

    def test_default_is_home_vault(self):
        vault = os.path.join(self.home, ".claude", "zettel")
        write_note(vault, "global", "home_note")
        r = self.run_zk("list")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("home_note", r.stdout)
        self.assertNotIn("sibling_note", r.stdout)

    def test_directory_beside_binary_is_never_a_vault(self):
        # no ZK_VAULT, no ~/.claude/zettel: the sibling notes/ must NOT be used.
        # Under a plugin install that sibling is the disposable plugin cache.
        r = self.run_zk("list")
        self.assertNotEqual(r.returncode, 0, "used the sibling directory as a vault:\n" + r.stdout)
        self.assertNotIn("sibling_note", r.stdout)
        self.assertIn(os.path.join(self.home, ".claude", "zettel"), r.stderr)

    def test_bench_uses_the_same_vault_as_zk(self):
        vault = os.path.join(self.home, ".claude", "zettel")
        write_note(vault, "global", "home_note")
        os.makedirs(os.path.join(vault, "bench"))
        with open(os.path.join(vault, "bench", "questions.tsv"), "w", encoding="utf-8") as fh:
            fh.write("q1\tglobal\thome_note desc\thome_note\tdesc\n")
        shutil.copy(os.path.join(REPO, "bin", "zk_bench"), os.path.join(self.install, "bin", "zk_bench"))
        r = subprocess.run([os.path.join(self.install, "bin", "zk_bench"), "--json"],
                           capture_output=True, text=True,
                           env={"PATH": os.environ["PATH"], "HOME": self.home})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(f'"vault": "{vault}"', r.stdout)


if __name__ == "__main__":
    unittest.main()
