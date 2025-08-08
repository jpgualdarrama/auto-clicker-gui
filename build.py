"""
Build script for Auto Clicker GUI

This script uses PyInstaller to compile the application into a Windows executable.
Run this script from the project root.
"""
import subprocess
import sys
import os

SRC_PATH = os.path.join('src', 'main.py')
DIST_PATH = os.path.join('dist', 'main.exe')

def build():
    print('Building executable with PyInstaller...')
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--onefile', '--windowed', SRC_PATH
    ])
    if result.returncode == 0:
        print(f'Build successful! Executable is at {DIST_PATH}')
    else:
        print('Build failed.')
        sys.exit(result.returncode)


def clean():
    print('Cleaning build artifacts...')
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            if os.path.isdir(folder):
                import shutil
                shutil.rmtree(folder)
            else:
                os.remove(folder)
    for spec in [f for f in os.listdir('.') if f.endswith('.spec')]:
        os.remove(spec)
    print('Clean complete.')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Build or clean the project.')
    parser.add_argument('command', choices=['build', 'clean'], help='Action to perform')
    args = parser.parse_args()
    if args.command == 'build':
        build()
    elif args.command == 'clean':
        clean()


if __name__ == '__main__':
    main()
