# Proposed guides — reconciliation map

These `.mdx` files are **spec-aligned draft upgrades**, produced alongside the new
OpenAPI specs (FincraNG/fincra-openapi). They are **not wired into `docs.json` navigation**
and do **not** overwrite any existing page — this repo is already populated, so these are
review material for the content team to merge into the live pages, not drop-in replacements.

Each is consistent with the code-derived spec: real header names (`api-key`; `x-pub-key` +
`x-business-id` for Checkout), sandbox base URL, cURL/Node/Python tabs, the shared success/
error envelope, and a sandbox testing section.

## Overlap map (proposed → existing live page to reconcile)

| Proposed draft | Existing live page(s) | Action |
| --- | --- | --- |
| `core/quickstart.mdx` | `quickstart.mdx` (root) | Merge: adopt the spec-aligned first-payout flow. |
| `core/authentication.mdx` | (no dedicated API auth page found; `get-started/*`) | Likely a genuine gap — consider adding an Authentication page. |
| `core/errors.mdx` | `payments/error-codes.mdx`, `conversion/error-codes.mdx`, `payouts/error-codes.mdx` | Consider one cross-cutting Errors page (shared envelope + `errorType` branching) linking the per-product code lists. |
| `core/webhooks-overview.mdx` | `webhooks/overview.mdx` | Reconcile: keep the live page; fold in the `${type}.${status}` event scheme + payload from the spec. |
| `webhooks/verify-signatures.mdx` | `webhooks/verify.mdx` | Reconcile. NOTE: the signing header/algorithm is a placeholder (`x-todo SIG-1`) — confirm from the emitter code before publishing either. |
| `payouts/send-a-payout.mdx` | `payouts/initiate-transfer.mdx` | Reconcile: align payload/fields to `fincra-disbursements.yaml` (spec wins). |
| `collections/overview.mdx` | `payments/overview.mdx` + payments pages | Reconcile: collections service exposes reconcile/refund/chargeback + `POST /transfer/simulate`, not charge-creation (that is created upstream). |
| `conversions/create-a-conversion.mdx` | `conversion/create-a-conversion.mdx` | Reconcile: align to `fincra-fx-conversions.yaml` (consume a `quoteReference`; `QUOTE_EXPIRED`). |

Full flag list is in `proposed-guides/CHANGE-SUMMARY.md`.

## Spec-vs-docs contradictions to check across the LIVE docs (spec wins)

- **Legacy naming:** replace `Identity Management` → Verification, `Payins` → Payments/
  Collections, `fliqpay_wallet` → the spec's wallet naming, wherever they appear.
- **Gateway path prefix:** the specs document paths as routed in code; the public Kong
  prefix (e.g. `/disbursements`, platform `/v2`) is flagged per spec in
  `x-todo-gateway-prefix`. Confirm it and make the live guides + the spec servers agree.
- **Checkout auth:** Checkout uses `x-pub-key` + `x-business-id` (not the secret `api-key`)
  — verify the live Checkout pages say so.
- **Removed endpoints:** QA confirmed some endpoints were removed (e.g. certain
  wallet balance-history/statement/topup and VA temporary/BVN routes). Ensure the live
  pages do not document endpoints absent from the specs.

## Why this shape

Dropping these as live pages would duplicate existing, maintained content and create nav
noise. The high-value, non-destructive change in this PR is **the API reference** (the
`API Reference` tab now renders the 11 real specs from the spec repo, replacing the
Mintlify placeholder). The guide upgrades are staged here for editorial merge.
