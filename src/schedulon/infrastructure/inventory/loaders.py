from __future__ import annotations
import csv
from pathlib import Path
import yaml
import httpx

def load_txt(path): return [{"name": l.strip(), "address": l.strip(), "vars": {}} for l in Path(path).read_text().splitlines() if l.strip()]
def load_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return [{"name": r.get("name") or r.get("host"), "address": r.get("address") or r.get("host"), "vars": dict(r)} for r in csv.DictReader(fh)]
def load_yaml(path):
    data=yaml.safe_load(Path(path).read_text()) or {}
    items=data.get("targets", data if isinstance(data,list) else [])
    return [{"name": i.get("name") or i.get("host"), "address": i.get("address") or i.get("host"), "vars": i} for i in items]
def load_git(repo_url, file_path, ref="main", workdir="/tmp/schedulon-inventory"): raise NotImplementedError("Git adapter hook")
def load_http_json(url, headers=None):
    data=httpx.get(url, headers=headers or {}, timeout=30).json()
    items=data.get("results", data.get("items", data if isinstance(data,list) else []))
    return [{"name": i.get("name") or i.get("host") or i.get("fqdn"), "address": i.get("address") or i.get("ip") or i.get("fqdn"), "vars": i} for i in items]
