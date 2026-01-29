import json
import os
import urllib.request
import xml.etree.ElementTree as ET
import re
from typing import Dict, Any, Optional, List
import importlib.metadata
from packaging import version
from rich.console import Console

console = Console()

WATCHLIST_PATH = os.path.join(os.path.dirname(__file__), "watchlist.json")

def clean_version(v_str: str) -> str:
    match = re.search(r'(\d+\.\d+(?:\.\d+)?(?:[a-zA-Z]+\d+)?)', v_str)
    if match:
        return match.group(1)
    return v_str.strip().lstrip('v')

def fetch_latest_from_atom(url: str) -> Optional[Dict[str, str]]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            tree = ET.parse(response)
            root = tree.getroot()
            ns = {'ns': 'http://www.w3.org/2005/Atom'}
            
            latest_entry = root.find('ns:entry', ns)
            if latest_entry is not None:
                title = latest_entry.find('ns:title', ns).text
                updated = latest_entry.find('ns:updated', ns).text
                content_node = latest_entry.find('ns:content', ns)
                summary = ""
                if content_node is not None:
                    summary = re.sub('<[^<]+?>', '', content_node.text or "")[:500] + "..."
                
                raw_v = title.strip().split()[-1]
                return {
                    "version": clean_version(raw_v) if "==" not in raw_v else clean_version(raw_v.split("==")[-1]),
                    "date": updated,
                    "title": title,
                    "summary": summary
                }
    except Exception:
        return None
    return None

def get_installed_version(package_name: str) -> str:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "Not Installed"

def get_package_evidence(package_name: str) -> Dict[str, Any]:
    if not os.path.exists(WATCHLIST_PATH):
        return {"error": "Watchlist not found"}

    with open(WATCHLIST_PATH, 'r') as f:
        watchlist = json.load(f)

    # Flatten categories to find the package
    for cat_name, cat in watchlist.items():
        if cat_name == "compatibility_rules":
            continue
        for name, info in cat.items():
            if info.get("package") == package_name or name == package_name:
                latest = fetch_latest_from_atom(info["feed"])
                installed = get_installed_version(package_name)
                min_v = info.get("min_version_for_optimizations", "0.0.0")
                
                upgrade_required = False
                if installed != "Not Installed":
                    try:
                        if version.parse(installed) < version.parse(min_v):
                            upgrade_required = True
                    except Exception:
                        pass

                return {
                    "package": package_name,
                    "installed_version": installed,
                    "latest_version": latest["version"] if latest else "Unknown",
                    "min_optimized_version": min_v,
                    "upgrade_required": upgrade_required,
                    "release_date": latest["date"] if latest else "Unknown",
                    "source_url": info["feed"].replace(".atom", ""),
                    "best_practice_context": latest["summary"] if latest else "Check release notes for performance/security enhancements."
                }
    return {"error": f"Package {package_name} not found in watchlist"}

def get_compatibility_report(installed_packages: List[str]) -> List[Dict[str, Any]]:
    if not os.path.exists(WATCHLIST_PATH):
        return []

    with open(WATCHLIST_PATH, 'r') as f:
        watchlist = json.load(f)
    
    rules = watchlist.get("compatibility_rules", [])
    reports = []
    
    # Normalize imports to find root package names
    roots = set()
    for pkg in installed_packages:
        roots.add(pkg.split('.')[0].replace('-', '_'))

    for rule in rules:
        comp_root = rule["component"].replace('-', '_')
        if comp_root in roots:
            # Check for incompatibilities
            for forbidden in rule.get("incompatible_with", []):
                forbidden_root = forbidden.replace('-', '_')
                if forbidden_root in roots:
                    reports.append({
                        "type": "INCOMPATIBLE",
                        "component": rule["component"],
                        "conflict_with": forbidden,
                        "reason": rule["reason"]
                    })
            
            # Check for synergies
            for synergy in rule.get("works_well_with", []):
                synergy_root = synergy.replace('-', '_')
                if synergy_root in roots:
                    reports.append({
                        "type": "SYNERGY",
                        "component": rule["component"],
                        "partner": synergy,
                        "reason": f"Optimally paired with ecosystem partner {synergy}."
                    })

    return reports
