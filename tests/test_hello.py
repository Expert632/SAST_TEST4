from app.hello import greet

def test_greet_with_name():
    assert greet("Alice") == "Hello, Alice!"

def test_greet_without_name():
    assert greet("") == "Hello, world!"
