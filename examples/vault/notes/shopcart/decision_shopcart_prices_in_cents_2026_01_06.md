---
title: Prices are integer cents
description: 2026-01-06 decided: every price, tax and total is an integer number of cents; floats caused a rounding drift of one cent per hundred line items
type: decision
project: shopcart
tags: [money, data-model]
created: 2026-01-06
---

**Chosen:** integer cents everywhere, formatted only at the view layer.

**Why:** a float total drifted by about one cent per hundred line items and the ledger stopped balancing.

**Consequence:** the `price_cents` column replaces `price`; the invariant is recorded in [[shopcart-invariants]].
