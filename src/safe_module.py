def greet_user(name: str) -> str:
    """Return a safe, formatted greeting."""
    if not name.isalpha():
        return "Invalid name."
    return f"Hello, {name.capitalize()}!"
