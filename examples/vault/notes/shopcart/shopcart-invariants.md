---
title: Shopcart invariants
description: rules that must hold in shopcart no matter what: integer money, idempotent payment capture, no direct SQL in controllers
type: hub
project: shopcart
tags: [invariants]
created: 2026-01-06
---

- Money is stored and computed as integer cents. See [[decision_shopcart_prices_in_cents_2026_01_06]].
- Payment capture is idempotent on the order's `capture_key`; retrying never double-charges. See [[map_shopcart_checkout]].
- Controllers never issue raw SQL; queries live in query objects.

Part of [[shopcart]].
