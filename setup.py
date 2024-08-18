from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="geocoder-api-wrapper",
    version="0.1.0",
    author="Darien Nouri",
    author_email="dan9232@nyu.edu",
    description="A wrapper for the Census Geocoder API and Google Maps Geocoding API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dariennouri/geocoder-api-wrapper",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "censusgeocode",
        "requests",
        "pandas",
    ],
)
