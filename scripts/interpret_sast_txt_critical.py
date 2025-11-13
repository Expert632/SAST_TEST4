#!/usr/bin/env python3
# scripts/interpret_sast_txt_critical.py
"""
Read a Semgrep TXT report and print a concise English summary:
 - If no critical lines found -> prints "✅ No critical vulnerabilities found in TXT report."
 - If critical lines found -> prints "❌ Critical vulnerability detected:" and
    * lists unique CVE IDs found in those lines (if any),
    * otherwise lists the critical lines + file:line if parsable.
The script is defensive and never raises an uncaught exception (safe for CI).
"""

import re
from pathlib import Path

# Candidate paths (choose one that matches your pipeline)
CANDIDATE_PATHS = [
    Path("sast-reports/semgrep-report.txt"),
    Path("sast-reports/semgrep-report.txt"),  # keep same in case
    Path("semgrep-report.txt"),
    Path("sast-report.txt"),
]

CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)
CRIT_RE = re.compile(r"\[?\s*CRITICAL\s*\]?|\bCRITICAL\b", re.IGNORECASE)
FILELINE_RE = re.compile(r"\(([^:()]+):(\d+)\)\s*$")  # matches "(path/file.py:42)" at end

def find_report_path():
    for p in CANDIDATE_PATHS:
        if p.exists():
            return p
    return None

def parse_critical_lines(text):
    critical_lines = []
    for line in text.splitlines():
        if CRIT_RE.search(line):
            critical_lines.append(line.strip())
    return critical_lines

def extract_cves_from_lines(lines):
    cves = set()
    for line in lines:
        for m in CVE_RE.findall(line):
            cves.add(m.upper())
    return sorted(cves)

def parse_fileline(line):
    """Try to extract (file, line) from trailing '(file:line)' pattern."""
    m = FILELINE_RE.search(line)
    if m:
        return m.group(1), m.group(2)
    return None, None

def main():
    try:
        report_path = find_report_path()
        if report_path is None:
            print("⚠️ TXT report not found in expected locations.")
            print("Searched paths:", ", ".join(str(p) for p in CANDIDATE_PATHS))
            return

        text = report_path.read_text(encoding="utf-8", errors="ignore")
        critical_lines = parse_critical_lines(text)

        if not critical_lines:
            print("✅ No critical vulnerabilities found in TXT report.")
            return

        # extract CVEs
        cves = extract_cves_from_lines(critical_lines)

        print(f"❌ {len(critical_lines)} critical finding(s) found in TXT report.")
        if cves:
            print("Detected CVE(s):")
            for c in cves:
                print(f"  - {c}")
        else:
            print("  - No CVE identifiers found in the critical lines.")
            print("  - Showing critical lines (file:line if present):")
            for ln in critical_lines:
                file, lineno = parse_fileline(ln)
                if file:
                    print(f"    * {file}:{lineno} -> {ln}")
                else:
                    print(f"    * {ln}")

    except Exception as e:
        # Never raise, just show a friendly message (safe for CI)
        print("⚠️ An error occurred while interpreting the TXT report:", str(e))

if __name__ == "__main__":
    main()
