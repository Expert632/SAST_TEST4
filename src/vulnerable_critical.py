# src/vulnerable_critical.py
"""
Demonstration file : insecure deserialization (pickle.loads on untrusted input).
This file is intentionally vulnerable for teaching SAST purposes.
Do NOT run this listener on a public/production environment.
"""

import pickle
import socket

def receive_and_unpickle(port: int = 9999):
    """Listen on a TCP port and unpickle any received data (insecure)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"Listening on port {port} (send pickled data to trigger vuln)...")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        data = b''
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
        # ⚠️ INSECURE: untrusted data passed to pickle.loads -> remote code execution risk
        obj = pickle.loads(data)
        print("Received object:", obj)

if __name__ == "__main__":
    # For the lab we do not actually open the listener by default.
    # This is purely an example file that Semgrep should flag.
    print("This file demonstrates insecure deserialization via pickle.loads.")
