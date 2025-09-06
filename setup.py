#!/usr/bin/env python3
"""
Modern setup.py using setuptools for Serial Input Monitor
Supports modern Python packaging standards with optional dependencies

Author: Leonardo Klein
Date: 2025
"""

from setuptools import setup, find_packages

setup(
    name="serial-input-monitor",
    use_scm_version={
        "write_to": "src/_version.py",
        "fallback_version": "1.0.0",
    },
    description="Arduino-based serial communication system for mouse and keyboard control",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Leonardo Klein",
    author_email="leo@ziondev.us",
    url="https://github.com/leonardokr/serial-input-monitor",
    project_urls={
        "Bug Reports": "https://github.com/leonardokr/serial-input-monitor/issues",
        "Source": "https://github.com/leonardokr/serial-input-monitor",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pyserial>=3.5",
        "PySide6>=6.5.0",
        "keyboard>=1.13.0",
    ],
    extras_require={
        "windows": [
            "winshell>=0.6",
            "pywin32>=306",
        ],
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
    },
    setup_requires=["setuptools_scm"],
    entry_points={
        "console_scripts": [
            "serial-control=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Communications",
        "Topic :: System :: Hardware",
    ],
    keywords="serial communication arduino mouse keyboard control",
    include_package_data=True,
    zip_safe=False,
)
