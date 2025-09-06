#!/usr/bin/env python3
"""
Installation Helper Script
Demonstrates different installation options for the project

Author: Leonardo Klein
Date: 2025
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Executes command and shows result."""
    print(f"\n{description}:")
    print(f"Command: {command}")
    print("-" * 40)

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print("SUCCESS")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_optional_dependencies():
    """Check if optional Windows dependencies are available."""
    print("\nChecking optional Windows dependencies:")
    print("-" * 50)

    dependencies = [
        ("winshell", "Desktop shortcut creation"),
        ("win32com.client", "Windows COM interface"),
    ]

    available = []
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✓ {module}: Available - {description}")
            available.append(module)
        except ImportError:
            print(f"✗ {module}: Not installed - {description}")

    return len(available) == len(dependencies)


def show_installation_options():
    """Show available installation options."""
    print("=" * 60)
    print("SERIAL INPUT MONITOR - Installation Options")
    print("=" * 60)

    print("\n1. BASIC INSTALLATION (Core features only):")
    print("   pip install -r requirements.txt")
    print("   → PySide6, pyserial, keyboard, configparser")

    print("\n2. FULL INSTALLATION (With Windows shortcuts):")
    print("   pip install -r requirements.txt")
    print("   pip install winshell pywin32")
    print("   → All features including desktop shortcut creation")

    print("\n3. MODERN INSTALLATION (Using pyproject.toml):")
    print("   pip install -e .")
    print("   pip install -e .[windows]  # With Windows extras")
    print("   pip install -e .[dev]      # With development tools")

    print("\n4. CURRENT STATUS:")
    has_optional = check_optional_dependencies()
    if has_optional:
        print("   ✓ Full installation detected - All features available")
    else:
        print("   ⚠ Basic installation detected - Core features only")
        print("   To enable Windows shortcuts, install: pip install winshell pywin32")


def main():
    """Main function."""
    show_installation_options()

    print("\n\nCURRENT ENVIRONMENT:")
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")

    print("\n\nNEXT STEPS:")
    print("1. Choose your installation option above")
    print("2. Run the installation command")
    print("3. Execute: python src/main.py")
    print("4. See INSTALL.md for detailed instructions")


if __name__ == "__main__":
    main()
