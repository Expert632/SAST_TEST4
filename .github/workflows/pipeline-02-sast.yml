# scripts/interpret_sast_report.py
"""
Analyse le rapport SAST TXT (ou JSON) et affiche un résumé pédagogique :
- Détecte les vulnérabilités critiques (Critical/High)
- Affiche CVE si disponible
"""

import json
from pathlib import Path

# Chemins des fichiers générés par Semgrep
JSON_REPORT = Path("sast-reports/semgrep-report.json")
TXT_REPORT = Path("sast-reports/semgrep-report.txt")

def interpret_semgrep_report(json_path: Path, txt_path: Path):
    if not json_path.exists():
        print(f"⚠️ Rapport JSON introuvable : {json_path}")
        return

    # Lire JSON
    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)

    critical_vulns = []
    for item in data.get("results", []):
        severity = item.get("extra", {}).get("severity", "").lower()
        check_id = item.get("check_id", "")
        cve = item.get("extra", {}).get("cwe", "N/A")  # parfois Semgrep utilise CWE au lieu de CVE
        path = item.get("path", "")
        line = item.get("start", {}).get("line", "?")
        if severity in ["critical", "high"]:
            critical_vulns.append((path, line, check_id, cve, severity))

    # Affichage résumé
    if not critical_vulns:
        print("✅ Aucune vulnérabilité critique détectée.")
    else:
        print(f"❌ {len(critical_vulns)} vulnérabilité(s) critique(s) détectée(s) :")
        for v in critical_vulns:
            path, line, check_id, cve, severity = v
            print(f"  - {severity.upper()} : {check_id} ({cve}) à {path} ligne {line}")

    # Afficher un aperçu du TXT
    if txt_path.exists():
        print("\n--- Aperçu du rapport TXT (top 20 lignes) ---")
        with txt_path.open(encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 20:
                    break
                print(line.strip())
        print("--- fin aperçu ---")

if __name__ == "__main__":
    interpret_semgrep_report(JSON_REPORT, TXT_REPORT)
