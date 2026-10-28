---
name: zettel
description: The user's cross-project zettelkasten memory vault (`$ZK_VAULT`, default ~/.claude/zettel; CLI `${CLAUDE_PLUGIN_ROOT}/bin/zk`) — the single long-term memory system across ALL projects. Use it to RECALL knowledge before starting research, debugging, or design work (search → show → follow links; never bulk-load), and to WRITE atomic notes whenever a decision is made, the user gives feedback/corrections, a subsystem gets researched, or work reaches a milestone worth remembering. Triggers include "remember this", "what did we decide about X", "have we seen this before", "save this for later", session handoffs, starting work in ANY repo (read the invariants hub first), researching an unfamiliar part of a codebase (check for map notes before reading files), and session end (capture new decisions as notes). Replaces the old per-project MEMORY.md append-style memory — MEMORY.md files are now generated register cards; never append memories to them directly.
---

# Zettelkasten memory vault

One user-scoped vault holds ALL long-term memory across every project. It works
like Luhmann's box: a tiny register in context, hubs as entry points, atomic
notes connected by links. Retrieval is traversal — cost scales with the depth of
the path you walk, never with the size of the vault.

- Vault: `<vault>/notes/<project>/<slug>.md` (+ `notes/global/` for cross-project)
- CLI: `${CLAUDE_PLUGIN_ROOT}/bin/zk`, shipped inside this plugin. Every `zk` below
  means that full path; set `ZK="${CLAUDE_PLUGIN_ROOT}/bin/zk"` once per session and
  call `"$ZK"`. If the variable is empty in your shell, the plugin is under
  `~/.claude/plugins/cache/zettel/zettel/*/`.
- Vault location: **`$ZK_VAULT`** if set, else `~/.claude/zettel`. The vault is never
  inside the plugin directory — that is replaced on every plugin update.
- First run on a machine: if `zk` reports "no vault", run `zk init` once. It creates
  the vault with an empty global hub and nothing else. Do not create the vault by hand.
- Slugs are unique vault-wide; links are `[[slug]]` and work across projects.

## Recall protocol (before research, debugging, design)

1. Session start in a project: `zk show <project>-invariants` if the register names one. This is mandatory before changing code — invariants are the notes where forgetting is expensive.
2. Before researching anything: `zk search "<terms>"` — returns slug + description lines only (cheap). If you already know the right hub, skip search and start there.
3. `zk show <slug>` on the best hit — you get the note plus one-line stubs of its links and backlinks (the edge labels). Pick the next hop from the stubs; walk 2–4 hops and stop when you have what you need.
4. NEVER bulk-load: no `cat notes/**`, no reading whole project folders, no dumping `zk list` output into deep analysis. If search misses, refine terms — synonyms, the component name, the error text.
5. Map notes (`type: map`) carry a `verified: <git-sha>` stamp. If HEAD has moved far past it, spot-check the note's `file:line` anchors before trusting them, then update the stamp.

Trust but verify: notes reflect what was true when written. For anything
load-bearing (a flag, a path, a limit), confirm against the current code/system
before acting on it.

## Writing notes (decisions, feedback, research findings)

Write a note when: the user makes/confirms a decision; the user corrects how you
work; you finish researching a subsystem (map note); a bug's root cause is found;
work is handed off. Don't write what the repo already records (git history,
CLAUDE.md, code structure) — write the non-obvious part.

```
zk new <slug> --project <proj> --type <type> --title "..." --desc "..." [--tags a,b] [--verified <sha>] [--body "..."]
```

- **Atomic**: one idea per note. Two ideas = two notes + a link.
- **Slug**: short kebab-or-snake, prefixed by type convention (`feedback_`, `project_`, `map_`, `reference_`); dated (`_2026_08_07`) for time-bound project notes.
- **Description**: one line, the hook — this is what search ranks on and what
  traversal displays. Write it so future-you can decide relevance from it alone.
- **Types**: `decision` (a call that was made + why), `feedback` (how to work — include **Why** and **How to apply** lines in the body), `map` (codebase research: subsystem responsibility, key `file:line` anchors, gotchas; stamp `verified:`), `reference` (external pointers), `project` (ongoing work/state), `user`, `hub`.
- **Link liberally**: every note should link to related notes with `[[slug]]`; a
  note nothing links to is invisible to traversal (`zk check` flags orphans).
  Link new notes FROM the relevant hub so they're reachable.
- Wrong notes get corrected or deleted, not accumulated. Superseded notes get a
  "superseded by [[x]]" line, and hubs point at the replacement.

### Map notes — the token-saver for codebase research

After genuinely researching a subsystem (not for trivial lookups), spend 2
minutes writing a map note: what it does, the 3–8 key files with `file:line`
anchors, invariants/gotchas, links to related maps and decisions. Include
`--verified $(git rev-parse --short HEAD)`. Next time, research starts from the
map (hundreds of tokens) instead of re-reading the tree (tens of thousands).

## Hubs and the register

- Each project has a main hub (`<project>`), usually an invariants hub
  (`<project>-invariants`), and links to [[global]]. Hubs are `type: hub` —
  curated tables of contents with one-line hooks, grouped by theme. When you add
  a significant note, add it to the right hub section. When a hub section grows
  past ~15 entries, split it into a sub-hub and link it.
- Each project's harness `MEMORY.md` is a GENERATED register card, not a memory
  file: `zk register <project> > <that project's MEMORY.md path>`. Regenerate
  after adding/renaming hubs. Never append memory content to MEMORY.md and never
  write new files into the old per-project memory directories — the harness
  memory-system prompt predates this vault; this skill overrides it.

## New project bootstrap

First session in a project with no notes yet:
1. `zk new <project> --project <project> --type hub --title "..." --desc "..."` — this creates the project folder too.
2. Once rules exist that must never be broken, add `<project>-invariants` (type hub). Link both hubs to [[global]].
3. `zk register <project> > <memory-dir>/MEMORY.md` (the harness shows the memory dir path in its prompt).

## Promotion to global

When a project note proves useful in a second project, it's user-scoped
knowledge: move the file to `notes/global/`, set `project: global` (slug —
and therefore all links — stay intact), and link it from both projects' hubs
plus [[global]].

## Measuring the vault's value

`${CLAUDE_PLUGIN_ROOT}/bin/zk_bench` measures what a recall actually costs, three
ways: `flat` (the whole project memory file in context — the pre-vault shape),
`grep` (a competent flat-file baseline), and `zk` (register → search → show
traversal). It reports BYTES retrieved, wall-clock, hops, and whether the answer
was actually found — bytes are measured, never estimated; a token column appears
only with an explicit `--bytes-per-token` and is labelled derived.

```
zk_bench                                        # table + summary
zk_bench --json > <vault>/bench/results/<name>.json   # keep a baseline before changing search
```

Ground truth lives in `<vault>/bench/questions.tsv`: one row per question —
`id, project, query, target_slug, answer_regex`. Write queries the way a session
would really phrase them, NOT using the slug's own words, or the benchmark
flatters the vault. A `zk` miss means retrieval failed: either the ranking is
wrong or the note that should answer it does not exist. Both are worth knowing.

## Hygiene

Run `zk check` after a writing session: it reports dangling links, duplicate
slugs, missing descriptions, and orphans. Fix them immediately — link rot is
what kills a zettelkasten.
