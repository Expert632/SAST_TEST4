# src/safe_app.py
"""
Exemple d'application "propre" : fonctions simples, testables, sans patterns dangereux.
But pédagogique : servir de baseline verte pour les scans SAST.
"""

from typing import Union

def safe_divide(a: float, b: float) -> float:
    """Effectue une division en protégeant contre la division par zéro."""
    if b == 0:
        raise ValueError("Division par zéro interdite")
    return a / b

def greet(name: Union[str, None]) -> str:
    """Retourne un message de bienvenue simple et sécuritaire."""
    if not name:
        return "Bonjour, invité !"
    # on évite toute interpolation dangereuse ou exécution
    return f"Bonjour, {name}"

def main() -> None:
    print("Exécution de l'application SAFE")
    print("10 / 2 =", safe_divide(10, 2))
    print(greet("Alice"))

if __name__ == "__main__":
    main()
