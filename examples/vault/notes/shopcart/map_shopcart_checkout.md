---
title: Map — checkout flow
description: cart to paid order: CheckoutController#create builds an Order, PaymentCapture captures with an idempotency key, OrderMailer confirms; gotcha is the capture retry path
type: map
project: shopcart
tags: [checkout, payments]
created: 2026-01-07
verified: 0badc0de
---

1. `app/controllers/checkout_controller.rb:12` builds the Order from the cart.
2. `app/services/payment_capture.rb:20` calls the gateway with the order's `capture_key`; a retry with the same key returns the first result instead of charging again.
3. `app/mailers/order_mailer.rb:8` sends the confirmation after capture succeeds.

Gotcha: a retry that changes the amount is rejected by the gateway; regenerate the key only when the cart changed. Rules: [[shopcart-invariants]]. Hub: [[shopcart]].
