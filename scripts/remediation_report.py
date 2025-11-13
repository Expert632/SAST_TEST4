import json
import os

REPORT_BEFORE = "sast-reports/semgrep-report-before.json"
REPORT_AFTER = "sast-reports/semgrep-report.json"
OUTPUT_FILE = "sast-reports/remediation-summary.txt"

def extract_cve_ids(report_path):
    """Extract CVE identifiers from a Semgrep JSON report."""
    if not os.path.exists(report_path):
        print(f"⚠️ File not found: {report_path}")
        return set()

    with open(report_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON file: {report_path}")
            return set()

    cve_ids = set()
    for result in data.get("results", []):
        msg = result.get("extra", {}).get("message", "")
        metadata = result.get("extra", {}).get("metadata", {})

        # Recherche de mentions CVE dans le message
        if "CVE-" in msg:
            cve_ids.update(part for part in msg.split() if "CVE-" in part)

        # Recherche de mentions CVE dans les métadonnées CWE
        cwes = metadata.get("cwe", [])
        for item in cwes:
            if isinstance(item, str) and "CVE-" in item:
                cve_ids.add(item)

    return cve_ids

def main():
    print("📊 Generating remediation summary report...")

    before = extract_cve_ids(REPORT_BEFORE)
    after = extract_cve_ids(REPORT_AFTER)

    fixed = before - after
    remaining = after

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== AUTO REMEDIATION SUMMARY ===\n\n")
        if fixed:
            f.write("✅ Fixed vulnerabilities:\n")
            for cve in sorted(fixed):
                f.write(f"  - {cve}\n")
        else:
            f.write("✅ No fixed vulnerabilities detected.\n")

        f.write("\n")

        if remaining:
            f.write("⚠️ Remaining critical vulnerabilities:\n")
            for cve in sorted(remaining):
                f.write(f"  - {cve}\n")
        else:
            f.write("🎉 No remaining critical vulnerabilities.\n")

    print("\n=== REMEDIATION SUMMARY ===")
    if fixed:
        print("✅ Fixed vulnerabilities:")
        for cve in fixed:
            print(f"  - {cve}")
    else:
        print("✅ No fixed vulnerabilities detected.")

    if remaining:
        print("⚠️ Remaining critical vulnerabilities:")
        for cve in remaining:
            print(f"  - {cve}")
    else:
        print("🎉 All vulnerabilities remediated successfully.")

    print(f"\n📁 Summary written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
