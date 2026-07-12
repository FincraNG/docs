# Live-docs corrections — audited against the code-derived specs

Read-only audit of the existing docs pages against the 11 OpenAPI specs (code is truth).
These are **factual contradictions a merchant would trip on**, each with spec evidence —
not style. Fixes are for the content team to apply to the live pages. Grouped by
severity; "verify" items are where the doc may be right but the supplied specs can't
confirm (endpoint owned by another service).

## Status (2026-07-12) — what is applied vs. what needs a human

Most HIGH items are now **applied on PR #3** (`docs/spec-correctness-fixes`), so this
punch-list is the audit trail plus the still-open items.

- **Applied on PR #3 (code-confirmed):** sandbox base URL → `sandboxapi.fincra.com`;
  zero-decimal currencies (UGX/XAF/XOF/RWF); card keys → snake_case; `payAttitude` →
  `payattitude`; conversion not-found → `CONVERSION_NOT_FOUND`; balance history →
  `GET /wallets/logs`; statement → `GET /wallets/logs/statement`; NGN resolve →
  `type: nuban`; webhook retry schedule → 5 attempts (5m/30m/2h/6h/24h); configure
  timeout → 10s; **Direct Charge auth → `x-business-id`** (now code-confirmed).
- **Applied on PR #3 with an inline HUMAN note** (best-effort correct, one fact still
  needs a human to hand to their AI): conversion post-funding wording;
  `ngn-virtual-accounts` test-mode sim endpoint; `wallets/fund-your-wallet` funding
  endpoint. Each note names the file, the current value, and the exact conditional edit.
- **Webhook signing — RESOLVED (was SIG-1):** header is `signature`, algorithm is
  **HMAC-SHA512** (hex), key is the merchant's **webhook secret key**, signed over the
  delivered JSON body (`{ event, data }`). The live `webhooks/verify.mdx` already matches
  this; the proposed `webhooks/verify-signatures.mdx` placeholder has been filled in.
- **Left for a human** (data not derivable from code): the 4 unconfirmed gateway prefixes
  (`/v2/auth`, notifications outgoing-webhooks path, `/settlements`, `/cards`) tracked in
  the spec repo's `NEEDS-HUMAN.md`; MEDIUM/VERIFY rows below owned by other services.

## HIGH — merchant-breaking, unambiguous (apply)

| Page | Wrong | Correct (spec) |
| --- | --- | --- |
| `payouts/how-payouts-work.mdx` (L149) | sandbox base URL `https://sandbox.fincra.com` | `https://sandboxapi.fincra.com` — the `sandbox.fincra.com` host is not the API; every sandbox call fails. |
| `payouts/currency-precision.mdx` (L13-31) | "all currencies use 2 decimals"; lists UGX/XAF/XOF at 2dp | UGX, XAF, XOF, **RWF** are zero-decimal — amount must be an **integer** (`fincra-disbursements` CreatePayoutRequest.amount). 2dp fails validation on these corridors. |
| `payments/accept-a-payment.mdx` (Direct Charge) | auth header `api-key` (secret) | `POST /charges` uses **`x-business-id`** (checkout-core `BusinessIdAuth`); api-key-only returns 401. |
| `payments/accept-a-payment.mdx` (card example) | card keys `number`, `expiryMonth`, `expiryYear` | `card_number`, `expiry_month`, `expiry_year`, `cvv` (+ optional `card_holder`) — checkout-core `Card` schema (snake_case). |
| `payments/direct-charge.mdx`, `payattitude.mdx`, `accept-a-payment.mdx` | `"type": "payAttitude"` | `"type": "payattitude"` (lowercase) — checkout-core `ChargeType` enum; `payAttitude` fails the enum. |
| `payments/ngn-virtual-accounts.mdx` | sandbox sim `POST /collections/webhooks/wema/callback` | Test-mode inbound sim is `POST /collections/transfer/simulate` (`SimulateCollectionRequest`); documented path/body don't exist. Verify before applying. |
| `conversion/how-currency-conversion-works.mdx` (L86) | "Fincra does not offer credit or post-funding" | Post-funding IS implemented: `settlementType: DEFERRED`, `POST /{id}/amend` (settle), `GET /post-funding-configs`, `POST_FUNDING_LIMIT_EXCEEDED`. Remove the categorical denial. |
| `conversion/error-codes.mdx` (L51) | not-found = `RESOURCE_NOT_FOUND` | `CONVERSION_NOT_FOUND` — the fx `ErrorType` enum has no `RESOURCE_NOT_FOUND`. |
| `wallets/balance-history.mdx` | `GET /wallets/balance-history` | No such endpoint (confirmed removed). Use `GET /wallets/logs` (`walletsListWalletLogs`; params page/perPage/currency/reference/dateFrom/dateTo/action). |
| `wallets/statement-of-account.mdx` | `GET /wallets/statement` | `GET /wallets/logs/statement` (`walletsGetWalletStatement`); `currency`, `dateFrom`, `dateTo` are **required**, perPage max 50. |
| `wallets/fund-your-wallet.mdx` | `POST /wallets/fund` as a prod api-key endpoint | `POST /fund` is sandbox-only + unauthenticated in code. Real funding = `POST /wallets/topups/initiate` and `/wallets/topups/virtual-accounts/initiate`. |
| `verification/nigeria.mdx` (L12/24/33) | NGN resolve `type: bank_account` | `type: nuban` (default) with `bankCode` — `bank_account` is the GHS/SWIFT rail. fincra-core `ResolveAccountRequest`. |
| `webhooks/troubleshooting.mdx` (L17-27) | retry ~2h, every 30s then every 10m | 5 attempts at **5m, 30m, 2h, 6h, 24h** (`WebhookRetryConfig`); ~24h window; opt-in `settings.enableWebhookRetry`. |
| `webhooks/configure.mdx` (L50) | `POST /sandbox/webhooks/test` | No such path. Use `POST /webhooks/outgoing/resend` (notifications) / `POST /payouts/resend-webhook` (disbursements). |

## MEDIUM — misleading, should fix

| Page | Issue | Spec |
| --- | --- | --- |
| `payouts/wallet-transfers.mdx` | claims always `successful` instantly + always fee-free | wallet payout returns a standard `Payout` (status enum incl. processing/failed); spec doesn't guarantee instant-success or zero-fee — confirm from code, else soften + handle processing/failed. |
| `payments/hosted-payment-page.mdx` | lists `api-key` required alongside `x-pub-key` | `POST /payments` uses **only** `x-pub-key` (`PubKeyAuth`); drop api-key unless the gateway requires it. |
| `conversion/how-currency-conversion-works.mdx` (L88) | "no cancellations or amendments" | `POST /{id}/amend` exists (settles a DEFERRED conversion); reword. |
| `wallets/manage-wallets.mdx` | list/get/create wallet as api-key merchant endpoints | those are internal, **unauthenticated** `/` primitives in code — not a merchant surface; keep unpublished or confirm a gateway-exposed read. |
| `webhooks/configure.mdx` (L16/38) | respond within **20s** | delivery `timeoutSeconds` default is **10** — a 20s budget is cut off server-side. |
| `verification/verify-a-bvn.mdx`, `verify-a-beneficiary-account.mdx`, `nigeria/ghana` | `/core/...` path prefix | in-code paths are `/bvn-verification`, `/accounts/resolve`; the `/core` gateway prefix is unconfirmed — verify with Kong and apply consistently (same class as the `/disbursements`, `/collections` prefixes). |

## LOW / VERIFY — not confirmable from the supplied specs (owned elsewhere or unharvested)

- `payouts/initiate-transfer.mdx`: `documentsRequired` field not in the code-derived Payout shape — verify; docs upload is a separate endpoint.
- `payouts/create-beneficiaries.mdx` + retrieve/manage: beneficiary + `/core/banks` endpoints aren't in the disbursements spec (owned by core/beneficiary service) — verify paths there.
- `payouts/how-payouts-work.mdx` + `conversion/*`: `POST /quotes/generate`, `GET /quotes/treasury-orders/rates`, 30-second TTL — owned by the upstream quotes service, not fx-conversions — verify there.
- `payments/hosted-payment-page.mdx` / `drop-in-checkout.mdx`: `feeBearer` marked required — it's optional (checkout-core `InitiatePaymentRequest` requires only amount/currency/customer).
- `payments/create-a-payment-link.mdx`: required fields unverifiable (CreatePaymentLink DTO not harvested).
- `conversion/create-a-conversion.mdx` + `supported-currency-pairs.mdx`: `/conversions` prefix + fixed pair allow-list not confirmable (corridors are quote-driven; codes validated against core).
- `verification/resolve-a-card-bin.mdx`: `GET /checkout/resolve/bin/{bin}` not in core/profile (checkout service) — verify path + auth (likely x-pub-key, not api-key).
- `verification/verify-a-bvn.mdx`: add a note that BVN verification needs the `BVN_VERIFICATION` product entitlement (403 if not).

## Clean (no findings)
Auth on payouts/conversion/wallets/verification correctly uses `api-key`. No legacy naming
(`Identity Management`/`Payins`/`fliqpay_wallet`) anywhere. The `/disbursements`,
`/collections`, `/checkout-core`, `/profile` gateway prefixes are correct (spec's
`x-todo-gateway-prefix`). Webhook envelope `{event, data}` matches the specs.

## Method
6 parallel read-only agents, one per section, each comparing every `.mdx` in the section
against the relevant spec(s); conservative (no false positives — "verify" used where a
spec can't confirm). Full agent output retained in the session.
