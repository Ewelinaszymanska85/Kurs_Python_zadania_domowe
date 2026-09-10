import os

name = os.environ.get("NAME", "World")
print(f"Hello, {name}!")