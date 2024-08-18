# post_install.py
import subprocess

def main():
    commands = [
        "pip install --upgrade twine",
        "pip install --upgrade requests-toolbelt",
        "pip install requests-toolbelt==1.0.0",
    ]

    for command in commands:
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
