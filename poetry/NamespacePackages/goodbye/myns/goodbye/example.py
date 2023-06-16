import os.path


def say_goodbye():
    print("Goodbye")
    print(f"Location of installation: {os.path.dirname(__file__)}")
