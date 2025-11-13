# scripts/interpret_sast_report.py
"""
Interprétation du rapport SAST (Pipeline 02) pour GitHub Actions
- Affiche uniquement les vulnérabilités critiques (Critical/High)
- Liste les CVE si disponibles
- Affiche un message clair si aucune vulnérabilité critique
"""

import json
from pathlib import Path

# Chemin du rapport JSON Semgrep
JSON_REPORT = Path("sast-reports/semgrep-report.json")

def interpret_semgrep_report(json_path: Path):
    if not json_path.exists():
        print(f"⚠️ Rapport JSON introuvable : {json_path}")
        return

    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)

    critical_cves = []

    for item in data.get("results", []):
        severity = item.get("extra", {}).get("severity", "").lower()
        cve = item.get("extra", {}).get("cwe", None)  # Semgrep peut stocker CWE/CVE
        if severity in ["critical", "high"] and cve:
            critical_cves.append(cve)

    if not critical_cves:
        print("✅ Aucune vulnérabilité critique détectée.")
    else:
        print(f"❌ {len(critical_cves)} vulnérabilité(s) critique(s) détectée(s) :")
        for cve in sorted(set(critical_cves)):
            print(f"  - CVE : {cve}")

if __name__ == "__main__":
    interpret_semgrep_report(JSON_REPORT)
