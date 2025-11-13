# src/vulnerable_app.py
"""
Exemple volontairement vulnérable pour démonstration SAST.
Pattern ciblé par Semgrep/CodeQL : usage direct d'eval() sur une entrée utilisateur.
NE PAS utiliser tel quel en production.
"""

def run_code():
    try:
        user_input = input("Entrez une expression Python (ex: 1+1) : ")
        # ⚠️ VULN: exécution directe de code utilisateur -> injection possible
        result = eval(user_input)
        print("Résultat de l'expression :", result)
    except Exception as e:
        print("Erreur lors de l'exécution :", e)

if __name__ == "__main__":
    run_code()
