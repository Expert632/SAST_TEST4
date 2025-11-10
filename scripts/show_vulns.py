import json, sys, os

report = "trivy-report.json"
if not os.path.exists(report):
    print("❌ Aucun rapport Trivy trouvé.")
    sys.exit(0)

with open(report) as f:
    data = json.load(f)

critical = []
for result in data.get("Results", []):
    for v in result.get("Vulnerabilities", []) or []:
        if v.get("Severity", "").upper() == "CRITICAL":
            critical.append(v)
            print(f"🔹 ID: {v.get('VulnerabilityID')}")
            print(f"   Package: {v.get('PkgName')}:{v.get('InstalledVersion')}")
            print(f"   Title: {v.get('Title', '')}")
            print(f"   URL: {v.get('PrimaryURL', '')}")
            print("-" * 60)

if not critical:
    print("✅ Aucune vulnérabilité CRITICAL détectée.")
else:
    print(f"🚨 {len(critical)} vulnérabilité(s) CRITICAL détectée(s).")
