import json, sys, os

report_file = "trivy-report.json"

if not os.path.exists(report_file):
    print("❌ Aucun rapport Trivy trouvé. Rien à remédier.")
    sys.exit(0)

with open(report_file) as f:
    data = json.load(f)

critical_vulns = []

for result in data.get("Results", []):
    vulns = result.get("Vulnerabilities", []) or []
    for v in vulns:
        if v.get("Severity", "").upper() == "CRITICAL":
            critical_vulns.append(v)

if not critical_vulns:
    print("✅ Aucune vulnérabilité CRITICAL détectée. Pipeline OK !")
    sys.exit(0)  # exit code 0 → pipeline vert

# Si on a des vulnérabilités critiques, on simule la remédiation
print("🚧 Début de la remédiation automatique simulée :\n")
for v in critical_vulns:
    pkg = v.get("PkgName", "N/A")
    version = v.get("InstalledVersion", "N/A")
    vuln_id = v.get("VulnerabilityID", "N/A")
    remediation = f"Update {pkg} from {version} to latest patched version"
    print(f"Vulnérabilité: {vuln_id}")
    print(f"   Package: {pkg}:{version}")
    print(f"   Remédiation appliquée: {remediation}")
    print("   Résultat: ✅ Succès simulé")
    print("-" * 60)

print(f"Résumé: {len(critical_vulns)} vulnérabilité(s) CRITICAL remédiée(s) (simulation).")
sys.exit(1)  # exit code 1 → pipeline rouge uniquement si vulnérabilités
