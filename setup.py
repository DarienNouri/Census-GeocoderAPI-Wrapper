from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="geocoder-api-wrapper",
    version="0.1.6",
    author="Darien Nouri",
    author_email="dan9232@nyu.edu",
    description="A wrapper for the Census Geocoder API and Google Maps Geocoding API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dariennouri/geocoder-api-wrapper",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "censusgeocode==0.5.2",
        "requests==2.32.3",
        "pandas==2.2.2",
        "pathlib2==2.3.7.post1",
        "urllib3==2.2.2",
    ],
    entry_points={
        'console_scripts': [
            'post-install = geocoder_wrapper.post_install.py:main',
        ],
    },
)
