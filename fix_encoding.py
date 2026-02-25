import os

# Fix repl.py
repl_path = r"C:\aryanblock\src\repl.py"
with open(repl_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the load_file function to use encoding
content = content.replace(
    "with open(filename, 'r') as f:",
    "with open(filename, 'r', encoding='utf-8') as f:"
)

with open(repl_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed repl.py")

# Fix main.py
main_path = r"C:\aryanblock\src\main.py"
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the run_file function to use encoding
content = content.replace(
    "with open(filename) as f:",
    "with open(filename, 'r', encoding='utf-8') as f:"
)
content = content.replace(
    "with open(filename, 'r') as f:",
    "with open(filename, 'r', encoding='utf-8') as f:"
)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed main.py")
print()
print("Done! Try loading your file again.")