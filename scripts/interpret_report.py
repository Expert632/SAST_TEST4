# scripts/interpret_report.py
"""
Analyse le rapport flake8-report.txt et affiche un résumé clair.
- Détecte spécifiquement les erreurs de syntaxe (E999)
- Résume le nombre total de lignes affectées
"""

import re
from pathlib import Path

REPORT_PATH = Path("sast-reports/flake8-report.txt")

def interpret_flake8_report(report_path: Path):
    if not report_path.exists():
        print("⚠️ Rapport introuvable :", report_path)
        return

    with report_path.open(encoding="utf-8") as f:
        lines = f.readlines()

    syntax_errors = []
    for line in lines:
        if "E999" in line or "SyntaxError" in line:
            match = re.match(r"(.+):(\d+):(\d+):", line)
            if match:
                file, lineno, col = match.groups()
                syntax_errors.append((file, lineno, col, line.strip()))
            else:
                syntax_errors.append(("?", "?", "?", line.strip()))

    if not syntax_errors:
        print("✅ Aucune erreur de syntaxe détectée dans le code.")
    else:
        print("❌ Erreurs de syntaxe détectées :")
        for err in syntax_errors:
            file, lineno, col, msg = err
            print(f"  - {file} (ligne {lineno}, colonne {col}) → {msg}")

if __name__ == "__main__":
    interpret_flake8_report(REPORT_PATH)
