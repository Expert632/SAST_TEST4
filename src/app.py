"""
DevSecOps Lab - Sample Python Application
This file contains a deliberately introduced critical vulnerability
for testing SAST pipelines and security gates.
"""

import os

def safe_function():
    """
    Example of safe code that does nothing harmful.
    """
    print("✅ This is a safe function.")

def dangerous_function(user_input):
    """
    🚨 Critical vulnerability: Command Injection
    Demonstrates unsafe use of os.system with untrusted input.
    """
    print(f"Received input: {user_input}")
    # DO NOT DO THIS IN PRODUCTION
    os.system(f"echo {user_input}")

def main():
    print("=== DevSecOps SAST Lab Demo ===")
    
    # Safe function call
    safe_function()
    
    # Dangerous function call (simulated vulnerability)
    user_input = "test; echo HACKED"
    dangerous_function(user_input)

if __name__ == "__main__":
    main()
