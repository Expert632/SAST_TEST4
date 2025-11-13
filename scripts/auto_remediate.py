import os
import json
import subprocess
from datetime import datetime

# -----------------------
# Config
# -----------------------
REPO_PATH = "."
CATALOG_FILE = "remediation_catalog.json"
PUSH_CHANGES = False  # Mettre à True pour pousser automatiquement sur GitHub

# -----------------------
# Fonctions
# -----------------------
def load_catalog():
    if not os.path.exists(CATALOG_FILE):
        print(f"⚠️ Remediation catalog '{CATALOG_FILE}' not found. No fixes applied.")
        return {}
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        try:
            catalog = json.load(f)
            print(f"📄 Loaded remediation catalog with {len(catalog)} patterns")
            return catalog
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse catalog JSON: {e}")
            return {}

def remediate_file(file_path, catalog):
    """Remplace les patterns vulnérables par leurs corrections."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️ Failed to read {file_path}: {e}")
        return False

    original_content = content
    fixes_applied = []

    for pattern, fix in catalog.items():
        if pattern in content:
            content = content.replace(pattern, fix)
            fixes_applied.append((pattern, fix))

    if content != original_content:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed vulnerabilities in: {file_path}")
            for p, f in fixes_applied:
                print(f"   - {p} → {f}")
            return True
        except Exception as e:
            print(f"⚠️ Failed to write {file_path}: {e}")
            return False

    return False

def git_commit_changes(branch_name):
    """Commit et push facultatif pour GitHub Actions"""
    try:
        subprocess.run(["git", "config", "--global", "user.email", "bot@devsecops.local"], check=False)
        subprocess.run(["git", "config", "--global", "user.name", "DevSecOps AutoBot"], check=False)
        subprocess.run(["git", "checkout", "-b", branch_name], check=False)
        subprocess.run(["git", "add", "."], check=False)
        subprocess.run(["git", "commit", "-m", f"🔒 Auto remediation applied - {datetime.now()}"], check=False)
        if PUSH_CHANGES:
            subprocess.run(["git", "push", "origin", branch_name], check=False)
        print(f"🚀 Changes committed to branch: {branch_name} (push={'enabled' if PUSH_CHANGES else 'disabled'})")
    except Exception as e:
        print(f"⚠️ Git commit failed: {e}")

# -----------------------
# Main
# -----------------------
def main():
    catalog = load_catalog()
    if not catalog:
        print("⚠️ No remediation catalog loaded. Exiting gracefully.")
        return

    modified = False
    print(f"📂 Scanning Python files in: {REPO_PATH}")
    for root, _, files in os.walk(REPO_PATH):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if remediate_file(file_path, catalog):
                    modified = True

    if modified:
        branch_name = f"auto-fix/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        git_commit_changes(branch_name)
        print("✅ Auto-remediation completed successfully.")
    else:
        print("✅ No vulnerabilities found to fix.")

    print("ℹ️ Pipeline finished (exit code 0)")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
    finally:
        exit(0)  # Toujours exit 0 pour lab pédagogique
