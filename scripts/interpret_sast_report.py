# scripts/interpret_sast_report.py
"""
Interpret Semgrep JSON report (Pipeline 02)
- If no critical/high findings -> print "No critical vulnerabilities detected"
- If critical/high findings -> print "Critical vulnerability detected" + list of CVE only
- Always safe: never fails pipeline
"""

import json
from pathlib import Path
import re

JSON_REPORT = Path("sast-reports/semgrep-report.json")

def find_cve_in_text(text):
    """Extract CVE identifiers from text (CVE-YYYY-NNNN)."""
    if not text:
        return set()
    pattern = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)
    return set(m.upper() for m in pattern.findall(text))

def extract_cves(item):
    """Try to find CVEs in standard fields or messages."""
    cves = set()
    extra = item.get("extra", {}) or {}

    # common fields
    for key in ("cwe", "cve"):
        val = extra.get(key)
        if isinstance(val, str):
            cves.add(val.upper())

    # scan message text
    message = extra.get("message", "")
    cves.update(find_cve_in_text(message))

    # references array
    refs = extra.get("references") or []
    if isinstance(refs, list):
        for r in refs:
            if isinstance(r, str):
                cves.update(find_cve_in_text(r))
            elif isinstance(r, dict):
                for sub in ("id", "url", "name"):
                    if sub in r and isinstance(r[sub], str):
                        cves.update(find_cve_in_text(r[sub]))

    return cves

def main():
    if not JSON_REPORT.exists():
        print(f"⚠️ JSON report not found: {JSON_REPORT}")
        return

    with JSON_REPORT.open(encoding="utf-8") as f:
        data = json.load(f)

    critical_items = [
        item for item in data.get("results", [])
        if str((item.get("extra") or {}).get("severity", "")).lower() in ("critical", "high")
    ]

    if not critical_items:
        print("✅ No critical vulnerabilities detected.")
        return

    # Extract CVEs
    all_cves = set()
    for item in critical_items:
        all_cves.update(extract_cves(item))

    print("❌ Critical vulnerability detected:")
    if all_cves:
        for cve in sorted(all_cves):
            print(f"  - {cve}")
    else:
        print("  - No CVE identifiers found")

if __name__ == "__main__":
    main()
