from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mls-scraper",
    version="1.0.0",
    author="Michael Miller",
    description="Production-grade real estate MLS scraper for Zillow, Redfin, and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MTM077/mls-scraper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=1.5.0",
        "aiohttp>=3.9.0",
    ],
)
