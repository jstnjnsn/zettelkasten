---
title: Ask before any force push or history rewrite
description: rewriting shared history (force push, rebase of a pushed branch, branch deletion) needs explicit permission in the moment, every time
type: feedback
project: global
tags: [git, process]
created: 2026-01-05
---

**Why:** a rewritten branch silently invalidates everyone else's checkout, and the damage is only visible after the fact.

**How to apply:** treat "clean up the branch" as a request to squash locally and show the result. The push itself waits for a plain yes. Related: [[feedback_short_answers_in_chat]] for how to ask.
