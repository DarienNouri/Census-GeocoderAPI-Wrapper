# post_install.py
import subprocess

def main():
    commands = [
        "pip install --upgrade twine",
        "pip install --upgrade requests-toolbelt"
    ]

    for command in commands:
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
