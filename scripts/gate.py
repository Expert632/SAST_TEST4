import json, sys, os

report_file = "trivy-report.json"

if not os.path.exists(report_file):
    print("❌ Aucun rapport trouvé pour la gate. Pipeline OK par défaut.")
    sys.exit(0)

with open(report_file) as f:
    data = json.load(f)

critical_vulns = [
    v
    for result in data.get("Results", [])
    for v in (result.get("Vulnerabilities", []) or [])
    if v.get("Severity", "").upper() == "CRITICAL"
]

if not critical_vulns:
    print("✅ Gate OK : aucune vulnérabilité CRITICAL détectée.")
    sys.exit(0)  # pipeline vert
else:
    print(f"🚨 Gate FAIL : {len(critical_vulns)} vulnérabilités CRITICAL détectées !")
    for v in critical_vulns:
        print(f" - {v.get('VulnerabilityID')} : {v.get('PkgName')}:{v.get('InstalledVersion')}")
    sys.exit(1)  # pipeline rouge = blocage du déploiement
