# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="dataclasses-io",
    version="0.0.5",
    author="kaparoo",
    author_email="kaparoo2001@gmail.com",
    description="Supports save/load APIs for dataclasses",
    long_description=readme,
    long_description_content_type="test/markdown",
    keywords=["dataclasses", "json", "yaml"],
    license="MIT",
    url="https://github.com/kaparoo/dataclasses-io",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["PyYAML"],
    packages=find_packages(exclude=("test*",)),
)
