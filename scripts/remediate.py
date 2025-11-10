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

if not critical:
    print("✅ Rien à remédier, aucune vulnérabilité critique.")
    sys.exit(0)

print("🚧 Début de la remédiation automatique simulée :\n")
for v in critical:
    pkg = v.get("PkgName")
    version = v.get("InstalledVersion")
    vuln_id = v.get("VulnerabilityID")
    remediation = f"Update {pkg} from {version} to latest patched version"
    print(f"Traitement : {vuln_id}")
    print(f"   Package : {pkg}:{version}")
    print(f"   Remédiation : {remediation}")
    print("   Résultat : ✅ Succès simulé")
    print("-" * 60)

print(f"Résumé : {len(critical)} vulnérabilité(s) CRITICAL remédiée(s) (simulation).")
sys.exit("❌ Pipeline échoué : vulnérabilités critiques détectées.")
