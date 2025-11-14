import json
import sys

# Chemin vers le rapport JSON généré par Pipeline 02
report_path = "sast-reports/semgrep-report.json"

try:
    with open(report_path, "r") as f:
        data = json.load(f)

    # Filtrer les findings critiques
    critical_findings = [f for f in data.get("results", []) if f.get("severity", "").lower() == "critical"]

    if critical_findings:
        print("❌ Security Gate: Critical vulnerability detected!")
        for item in critical_findings:
            path = item.get("path", "unknown file")
            line = item.get("start", {}).get("line", "unknown line")
            print(f" - {path}:{line}")
        # Exit code 1 = Rouge
        sys.exit(1)
    else:
        print("✅ Security Gate: No critical vulnerabilities detected.")
        # Exit code 0 = Vert
        sys.exit(0)

except FileNotFoundError:
    print(f"⚠️ Report file not found: {report_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"⚠️ Failed to parse JSON report: {report_path}")
    sys.exit(1)
