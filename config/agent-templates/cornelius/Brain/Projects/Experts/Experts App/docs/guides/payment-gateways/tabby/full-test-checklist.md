---
title: "Tabby — full integration QA checklist"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/payments", "topic/tabby"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/payment-gateways-index|Payment gateways index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/guide|Tabby integration guide]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/capture|Tabby capture flow]]

Full Testing Checklist
After the integration is completed from your side - the QA will be performed by the Tabby team. To make sure that all the requirements are covered - kindly review the below checklist which contains the points assessed by our side.
If any of the points cannot be applied to your website/application architecture - please, notify us about that in an email thread and this point will be discussed separately.
This page covers Website (desktop and mobile), iOS and Android custom (direct API) integrations. When integrating Tabby on the E-commerce Platform from the list this section is not applicable.
​
On-Site Messaging
Product and Cart snippets and pop-ups are present in accordance with the:
custom integration documentation
or the SDK documentation used
Product snippets are shown for all products, there is no amount limitation on displaying snippets
Cart snippet is shown for all amounts, there is no amount limitation on displaying snippets
Cart snippet amount is updated successfully when changes are performed with the items in the Cart: addition / removal / deletion of the items
If the store has both Arabic and English languages - snippets should be displayed correctly for both of them
Website: snippets should fit the width of a Mobile Web screen and have suitable width for a Desktop Web as well
In case your store has several countries: Tabby snippets should be displayed only for countries you have already registered with Tabby
If our code is not compatible with yours or you have a non-standard plan: kindly use one of the following custom snippets after the confirmation from your assigned business manager is received
​
Tabby as a Payment Method
Payment method name is present in accordance with the documentation
Tabby logo is present near the payment method name
There should be no restrictions on displaying Tabby payment method from your side - this behaviour should be handled by background pre-scoring process
If the store has both Arabic and English languages - Payment method should be displayed correctly for both of them
In case your store has several countries: Tabby payment method should be displayed only for countries you have already registered with Tabby
​
Checkout
Background Pre-scoring check is present and working in accordance with the documentation
Website: when a customer decides to place an order with Tabby - Tabby Checkout is opened in the same browser window
Mobile apps: no control buttons (e.g., X, close, back, etc.) from your app are present on Tabby Checkout
Total amount on Checkout = amount shown on Tabby Checkout
If the store has both Arabic and English languages - language marker is sent correctly in a session creation request: object “lang”, enum “ar” / “en”
Session creation request contains all the required parameters from Tabby API
Success scenario is working
Cancellation scenario is working
Failure scenario is working
Corner case is supported
​
Payment Verification and Processing
Webhooks are registered one per each merchant_code. Should be “is_test”:“true” to work with testing keys
After a payment is placed successfully with Tabby you receive a webhook to your registered url with status “authorized”
On receiving it you should trigger a getPayment request to verify the status of the payment
If a status is “AUTHORIZED” - a capture request should be triggered from your side
It is an expected behaviour that webhooks return “authorized” in lower case while getPayment - in upper case: “AUTHORIZED”.
A full amount must be captured
If you have any questions considering this Checklist - feel free to contact us in the Integrations thread.
