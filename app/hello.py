def greet(name: str) -> str:
    """Return a greeting message."""
    if not name:
        return "Hello, world!"
    return f"Hello, {name}!"
