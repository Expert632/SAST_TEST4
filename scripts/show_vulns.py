import json, sys, os

report_file = "trivy-report.json"

if not os.path.exists(report_file):
    print("❌ Aucun rapport Trivy trouvé.")
    sys.exit(0)

with open(report_file) as f:
    data = json.load(f)

critical_vulns = []

for result in data.get("Results", []):
    vulns = result.get("Vulnerabilities", []) or []
    for v in vulns:
        if v.get("Severity", "").upper() == "CRITICAL":
            critical_vulns.append(v)
            print(f"🔹 ID: {v.get('VulnerabilityID')}")
            print(f"   Package: {v.get('PkgName')}:{v.get('InstalledVersion')}")
            print(f"   Title: {v.get('Title', '')}")
            print(f"   URL: {v.get('PrimaryURL', '')}")
            print("-" * 60)

if not critical_vulns:
    print("✅ Aucune vulnérabilité CRITICAL détectée.")
else:
    print(f"🚨 Total CRITICAL vulnérabilités détectées: {len(critical_vulns)}")
