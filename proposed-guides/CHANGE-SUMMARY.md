# Change summary — Workstream B (Payouts guides)

Scope of this pass: authored `payouts/send-a-payout.mdx` as the section exemplar,
consistent with `openapi/fincra-disbursements.yaml`. This is the template the rest of
the Payouts section (and every other section) should follow.

## Flagged for a human decision

1. **Gateway path prefix in code samples.** The service routes mount at `/payouts`
   (no version prefix in-repo); the public path is applied at the Kong gateway. The
   guide uses `https://sandboxapi.fincra.com/disbursements/payouts` (the prefix observed
   elsewhere) so the sample is runnable, but **the exact published prefix — `/disbursements`,
   `/v2`, or both — must be confirmed** and, once confirmed, applied identically in the
   spec `servers`/paths and every guide. This is the single blocker to the samples being
   copy-paste runnable. Source: EXTRACTION-REPORT.md x-todo GW-1.

2. **Cross-currency `quoteReference` provenance.** The guide states a `quoteReference` is
   obtained "from the conversion service" and links to a `payouts/quotes-and-fees` page
   that does not exist yet. That page depends on the fx-conversions / quoting-engine spec
   (not yet extracted). Written as a Next-steps link; author the quotes guide from that
   service's spec before publishing.

3. **Webhook signature mechanism.** The guide links to `/webhooks/verify-signatures` and
   says to verify the signature, but the outbound webhook signing header/algorithm was
   not confirmed from code (EXTRACTION-REPORT.md x-todo SIG-1). Confirm before writing
   the signature-verification page so the guide's instruction is real.

## Consistency notes (spec wins — no silent choices)

- **Idempotency:** the guide names `customerReference` as the idempotency key and warns
  against blind retries, matching the code's `DUPLICATE_CUSTOMER_REFERENCE` guard. If
  product prefers a dedicated `Idempotency-Key` header later, the spec must change first,
  then the guide.
- **Error branching:** the guide tells integrators to branch on `errorType`, not the
  human `error` string, and lists only `errorType`s the spec's `x-fincra-error-catalog`
  proves reachable on the create path. No invented error codes.
- **Zero-decimal currencies:** the amount-must-be-integer rule for `UGX/XAF/XOF/RWF` is
  stated in the field table (a real constraint from `CURRENCIES_WITHOUT_DECIMALS`), not
  buried in prose — per the conventions doc.

## Legacy naming

- No legacy terms (`fliqpay_wallet`, `Payins`, `Identity Management`) were needed or
  introduced in this guide. When upgrading existing pages that use them, replace with the
  spec's naming and note the replacement here.

## Not yet written (Payouts section backlog)

`payouts/overview`, `payouts/quotes-and-fees`, `payouts/beneficiaries`,
`payouts/payout-status-and-requery`. Each follows the same spine (see
`workstream-c-theme/conventions.mdx`) and must cite the spec at every endpoint mention.
