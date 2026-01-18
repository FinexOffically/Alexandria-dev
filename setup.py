"""Setup script for Alexandria package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="alexandria",
    version="0.1.0",
    author="Alexandria Team",
    description="A sophisticated knowledge and information management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/alexandria",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "alexandria=alexandria.ui.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
