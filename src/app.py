from safe_module import greet_user

def main():
    user = input("Enter your name: ")
    print(greet_user(user))

if __name__ == "__main__":
    main()
