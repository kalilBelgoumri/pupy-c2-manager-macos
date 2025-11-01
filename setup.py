#!/usr/bin/env python3
"""
Setup script to build macOS .app bundle
Requires: PyQt5, py2app
"""

from setuptools import setup

APP = ["src/main.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "packages": ["PyQt5"],
    "includes": ["PyQt5.QtWidgets", "PyQt5.QtCore", "PyQt5.QtGui"],
}

setup(
    name="Pupy C2 Manager",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    version="1.0.0",
    author="Security Researcher",
    description="Pupy C2 Bundler and Victim Manager for macOS",
)
