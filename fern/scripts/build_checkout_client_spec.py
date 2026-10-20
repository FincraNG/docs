"""Build the client-side (React Native / browser) spec from api/specs/checkout.yaml.

Keeps only the endpoints that are safe to call from a customer's device: the ones
that use the public key or no key. Run: python build_checkout_client_spec.py
(needs PyYAML). Output: ../apis/checkout-client/openapi/checkout-client.yaml
"""
import copy, json, os, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../api/specs/checkout.yaml")
OUT = os.path.join(HERE, "../apis/checkout-client/openapi/checkout-client.yaml")

spec = yaml.safe_load(open(SRC))
default_security = spec.get("security", [])
keep = {}
for path, ops in spec["paths"].items():
    for method, op in ops.items():
        if method not in ("get", "post", "put", "patch", "delete"):
            continue
        security = op.get("security", default_security)
        schemes = {name for req in security for name in req}
        if schemes <= {"publicKey"}:  # public key only, or no auth
            keep.setdefault(path, {})[method] = copy.deepcopy(op)

client = {
    "openapi": spec["openapi"],
    "info": {**spec["info"], "title": "Fincra Checkout (client)",
             "description": "Client-side Checkout endpoints. Uses your public key only, never your secret key."},
    "servers": spec["servers"],
    "security": [],
    "paths": keep,
    "components": {**spec["components"],
                   "securitySchemes": {"publicKey": spec["components"]["securitySchemes"]["publicKey"]}},
}

# drop schemas, parameters and responses that the kept endpoints don't reference
def refs(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "$ref" and isinstance(v, str):
                acc.add(v)
            else:
                refs(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            refs(v, acc)
    return acc

used = refs(client["paths"], set())
while True:
    more = set()
    for r in used:
        _, _, kind, name = r.split("/", 3)
        more |= refs(spec["components"].get(kind, {}).get(name, {}), set())
    if more <= used:
        break
    used |= more
for kind in ("schemas", "parameters", "responses", "requestBodies"):
    if kind in client["components"]:
        client["components"][kind] = {n: v for n, v in client["components"][kind].items()
                                      if f"#/components/{kind}/{n}" in used}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write("# GENERATED from api/specs/checkout.yaml by fern/scripts/build_checkout_client_spec.py. Do not edit.\n")
    yaml.safe_dump(client, f, sort_keys=False, allow_unicode=True)
print("kept:", json.dumps({p: list(o) for p, o in keep.items()}))
