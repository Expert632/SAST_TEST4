# app/vulnerable_login.py
# FICHIER INTENTIONNELLEMENT VULNÉRABLE POUR TEST SAST
# NE PAS UTILISER EN PRODUCTION

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "test_users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    # compte de test (mot de passe en clair, intentional)
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'alice', 'password123')")
    conn.commit()
    conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    # Récupère les paramètres sans validation stricte
    username = request.values.get("username", "")
    password = request.values.get("password", "")

    # ---------- VULNÉRABILITÉ INTENTIONNELLE ----------
    # Construction dynamique d'une requête SQL à partir d'entrées utilisateur
    # -> susceptible d'entraîner une injection SQL
    query = "SELECT id, username FROM users WHERE username = '%s' AND password = '%s'" % (username, password)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Exécution d'une requête construite de façon non paramétrée
        c.execute(query)
        row = c.fetchone()
        if row:
            return jsonify({"status": "ok", "user_id": row[0], "username": row[1]})
        else:
            return jsonify({"status": "denied"}), 401
    except Exception as e:
        # On renvoie l'erreur brute (inutilement verbeuse, mauvaise pratique)
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
