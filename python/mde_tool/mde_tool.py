import argparse
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional

import msal
import requests


@dataclass(frozen=True)
class Config:
    tenant_id: str
    client_id: str
    scope: str
    base_url: str  # ex: https://api.securitycenter.microsoft.com OR gov variant
    timeout_s: int = 30


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def get_env(name: str, required: bool = True) -> str:
    v = os.getenv(name, "").strip()
    if required and not v:
        die(f"Missing env var: {name}")
    return v


def acquire_token_device_code(cfg: Config) -> str:
    """
    Safe interactive auth for personal tooling.
    No secrets required. Works well for lab/test usage.
    """
    authority = f"https://login.microsoftonline.com/{cfg.tenant_id}"
    app = msal.PublicClientApplication(client_id=cfg.client_id, authority=authority)

    flow = app.initiate_device_flow(scopes=[cfg.scope])
    if "user_code" not in flow:
        die(f"Device flow initiation failed: {flow}")

    print(flow["message"])  # user instructions
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        die(f"Token acquisition failed: {result.get('error_description') or result}")
    return result["access_token"]


def api_request(cfg: Config, token: str, method: str, path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
    url = cfg.base_url.rstrip("/") + "/" + path.lstrip("/")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.request(method, url, headers=headers, json=json_body, timeout=cfg.timeout_s)
    if resp.status_code >= 400:
        die(f"{method} {url} failed: {resp.status_code} {resp.text}")
    if resp.text.strip():
        return resp.json()
    return None


def cmd_list_machines(cfg: Config, token: str) -> None:
    data = api_request(cfg, token, "GET", "/api/machines")
    for m in data.get("value", []):
        print(f"{m.get('id')} | {m.get('computerDnsName')} | {m.get('riskScore')} | {m.get('healthStatus')}")


def cmd_tag_machine(cfg: Config, token: str, machine_id: str, tag: str) -> None:
    body = {"Value": tag, "Action": "Add"}
    api_request(cfg, token, "POST", f"/api/machines/{machine_id}/tags", json_body=body)
    print(f"Tagged machine {machine_id} with '{tag}'")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mde_tool", description="Portable MDE API CLI (no secrets).")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-machines", help="List machines (id, dns, risk, health).")

    t = sub.add_parser("tag-machine", help="Add an MDE tag to a machine by ID.")
    t.add_argument("--machine-id", required=True)
    t.add_argument("--tag", required=True)

    return p


def main() -> None:
    # Required env vars
    cfg = Config(
        tenant_id=get_env("MDE_TENANT_ID"),
        client_id=get_env("MDE_CLIENT_ID"),
        scope=get_env("MDE_SCOPE"),
        base_url=get_env("MDE_BASE_URL"),
    )

    token = acquire_token_device_code(cfg)
    args = build_parser().parse_args()

    if args.cmd == "list-machines":
        cmd_list_machines(cfg, token)
    elif args.cmd == "tag-machine":
        cmd_tag_machine(cfg, token, args.machine_id, args.tag)
    else:
        die("Unknown command")


if __name__ == "__main__":
    main()
