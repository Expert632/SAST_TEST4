import os
import json
import subprocess
from datetime import datetime

REPO_PATH = "."
CATALOG_FILE = "remediation_catalog.json"

def load_catalog():
    if not os.path.exists(CATALOG_FILE):
        print(f"⚠️  Remediation catalog '{CATALOG_FILE}' not found.")
        return {}
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def remediate_file(file_path, catalog):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    fixes_applied = []

    for pattern, fix in catalog.items():
        if pattern in content:
            content = content.replace(pattern, fix)
            fixes_applied.append((pattern, fix))

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Fixed vulnerabilities in: {file_path}")
        for p, f in fixes_applied:
            print(f"  - {p} → {f}")
        return True
    return False

def git_commit_changes(branch_name):
    subprocess.run(["git", "config", "--global", "user.email", "bot@devsecops.local"])
    subprocess.run(["git", "config", "--global", "user.name", "DevSecOps AutoBot"])
    subprocess.run(["git", "checkout", "-b", branch_name], check=False)
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", f"🔒 Auto remediation applied - {datetime.now()}"], check=False)
    subprocess.run(["git", "push", "origin", branch_name], check=False)

def main():
    catalog = load_catalog()
    if not catalog:
        print("❌ No remediation catalog found. Exiting.")
        return

    modified = False
    for root, _, files in os.walk(REPO_PATH):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if remediate_file(file_path, catalog):
                    modified = True

    if modified:
        branch_name = f"auto-fix/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        git_commit_changes(branch_name)
        print(f"🚀 Auto-remediation completed. Pushed changes to branch: {branch_name}")
    else:
        print("✅ No vulnerabilities found to fix.")

if __name__ == "__main__":
    main()
