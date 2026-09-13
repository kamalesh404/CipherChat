from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cipherchat",
    version="0.1.0",
    description="End-to-end encrypted chat with X25519, AES-GCM, Double Ratchet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kamalesh",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0",
        "fastapi>=0.100",
        "uvicorn>=0.20",
        "cryptography>=42.0",
        "pydantic>=2.0",
    ],
    extras_require={"dev": ["pytest>=7.0", "httpx", "ruff"]},
    entry_points={"console_scripts": ["cipherchat=src.cli.main:cli"]},
    python_requires=">=3.9",
)
