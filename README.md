# zettel — zettelkasten memory for Claude Code

One vault holds long-term memory across every project. Retrieval is traversal
(register → search → show → follow links), so context cost scales with the depth
of the path walked, not with the size of the vault.

This repo is a Claude Code plugin: the `zk` command-line tool, the `zettel`
skill that teaches Claude how to use it, and nothing else. Notes are yours and
never live in the plugin.

## Install

In Claude Code:

```
/plugin marketplace add https://github.com/jstnjnsn/zettelkasten.git
/plugin install zettel@zettel
```

Requires python3 (stdlib only). No network, no dependencies, no daemon.

The first time the skill runs on a machine it calls `zk init`, which creates the
vault with an empty global hub and nothing else. To do it yourself:

```sh
~/.claude/plugins/cache/zettel/zettel/*/bin/zk init
```

## Where the vault lives

`$ZK_VAULT` if set, else `~/.claude/zettel`. The vault is never inside the
plugin directory, which is replaced on every plugin update. Set `ZK_VAULT` only
when the vault has to live somewhere else (a mandated path, an encrypted volume,
a second vault).

Layout: `<vault>/notes/<project>/<slug>.md`, one atomic note per file, plus
`notes/global/` for knowledge that applies across projects. Slugs are unique
vault-wide; links are `[[slug]]`.

The vault is plain markdown on the local disk. If you back it up or sync it,
treat it like the code it describes and keep it where that code is allowed to
go.

## Daily use

The skill drives these; you rarely type them.

```sh
zk search "<terms>"          # ranked; slug + description only (cheap)
zk show <slug>               # note + one-line stubs of its links and backlinks
zk new <slug> --project P --type T --title "..." --desc "..."
zk check                     # dangling links, dup slugs, orphans — run after writing
zk register <project>        # regenerate that project's MEMORY.md register card
```

Never bulk-load: no `cat notes/**`, no reading a whole project folder. If search
misses, refine the terms.

## Proving it is worth it

`zk_bench` measures the cost of a recall three ways — `flat` (whole memory file in
context), `grep` (a competent flat-file baseline), `zk` (traversal) — and reports
bytes retrieved, wall-clock, hops, and **whether the answer was actually found**.
Bytes are measured; a token column appears only with `--bytes-per-token` and is
labelled derived, because an unmeasured token count is a guess.

```sh
zk_bench                                             # table + summary
zk_bench --json > <vault>/bench/results/before.json  # baseline BEFORE changing anything
```

Ground truth is `<vault>/bench/questions.tsv`: `id, project, query, target_slug, answer_regex`.
Phrase queries the way a session really would, not with the slug's own words.
A `zk` miss is a finding: either the ranking is wrong, or the note that should
answer it was never written.

`examples/vault/` is a small made-up vault with its own questions. It is the
bench's self-test and a worked example of hubs, invariants, maps and decisions:

```sh
ZK_VAULT=examples/vault bin/zk_bench --arms zk
```

## Development

```sh
python3 -m unittest discover -s tests
claude plugin validate .
```
