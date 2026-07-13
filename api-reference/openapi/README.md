# Vendored OpenAPI specs — do not hand-edit

These 12 specs are **published copies** from the source-of-truth spec repo
[`FincraNG/fincra-openapi`](https://github.com/FincraNG/fincra-openapi). `docs.json`
points the API Reference tab at these local files (root-relative paths), not at the spec
repo over the network.

| | |
| --- | --- |
| Source repo | `FincraNG/fincra-openapi` |
| Synced from | branch `dev`, commit `e0f43d1` |
| Files | 12 self-contained specs (each resolves only internal `#/components/...` refs) |

## Why these are vendored, not fetched by URL

Mintlify's build fetches OpenAPI files as an **anonymous** client. `fincra-openapi` is a
**private** repo, so `https://raw.githubusercontent.com/FincraNG/fincra-openapi/dev/...`
returns `404` during the build and every API page fails to render. Vendoring the specs
into this repo makes them local files that need no auth.

Even after the spec repo is made public, the docs should keep consuming a **pinned,
published copy** — never a live branch URL. A live `dev` URL is a moving target (CDN
cache, force-push, breaking edits) and would let an unrelated spec change break the docs
build with no review here.

## How to update these

Do **not** edit these files directly. Edit the spec in `FincraNG/fincra-openapi`, then
publish the change into this folder:

- **Automatic:** the `publish-to-docs` workflow in `fincra-openapi` opens a sync PR here
  on each tagged release, updating these files and stamping the row above. The spec repo
  stays the single source of truth.
- **Manual (if needed):** copy the changed `openapi/*.yaml` from `fincra-openapi` into
  this folder, update the commit hash above, and open a docs PR.
