# Product brief

Source: the Developer Experience Operating System (Foundations and Documentation Engineering). When the OS changes, update this brief in the same pull request.

## Description

Fincra is payment infrastructure for businesses that move money across Africa. Developers integrate through Fincra's API to collect payments, issue virtual accounts, send payouts, convert currencies, hold balances, run direct debits, issue cards and verify customers and accounts.

Products, in the order they appear in the sidebar:

- Payments
- Virtual Accounts
- Payouts
- FX and Conversion
- Wallets and Balances
- Direct Debit
- Issuing (launching soon)
- Verification

This documentation is the self-serve home for those products. It works together with the API reference, sandbox, Postman collections, SDKs and dashboard.

## Primary audience

A developer at a business integrating Fincra, with no internal knowledge of Fincra's products or systems. They arrive to decide whether Fincra supports their use case, then to build, test, go live and run the integration without contacting anyone at Fincra.

They are technical, short on time and judge Fincra by whether the documentation matches what the API actually does.

## Jobs to be done

The documentation must let that developer, on their own:

1. Determine whether a product supports their use case, market, currency and payment rail.
2. Get sandbox credentials and complete the product's core integration within one hour of active technical work.
3. Test success, failure, pending and asynchronous behaviour, including webhooks.
4. Identify every production dependency, move safely from sandbox to production and complete a controlled transaction in production.
5. Run the integration day to day: track status, handle errors, retry safely, reconcile, stay within limits and troubleshoot problems.

Each product follows the same journey in the sidebar: Overview, Markets and rails, Requirements, Quickstart, Guides, Test in sandbox, Go live, Operations and API reference.

## Motivation

Fincra's mission is to be the easiest and most reliable payment infrastructure to integrate and operate across Africa. Reliable means the documentation matches how the product behaves in sandbox and in production. Any mismatch is a defect.

A product appears in this documentation only after it passes a recorded end-to-end run from a clean account, by someone who did not build it or write its documentation. There are no previews and no exceptions.

## Writing and content rules

- Write journeys, not endpoint lists. Every journey links to the API reference, but the reference is never the starting point.
- "Fincra" is the actor, for example "Fincra sends a webhook". Use must, can and might. Never use should or may.
- Use these core terms consistently: payout, beneficiary, virtual account, conversion, sandbox and production. Never test, test mode, live, live mode or prod for the environments. "Go live" is fine for the act of launching.
- Show code samples in cURL first, then Node.js. Never use real keys or customer data.
- One contract applies to every merchant. Never document behaviour that depends on which merchant sends a request.
- Never write about sub-accounts. Fincra does not offer them.
- Never name upstream partners, except where the developer chooses a network.
- British spelling, no em dashes, no serial comma.
