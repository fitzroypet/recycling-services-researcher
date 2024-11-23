from setuptools import setup, find_packages

setup(
    name="irecycle-digital-research",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "googlemaps>=4.10.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "pyodbc>=5.0.0",
        "sqlalchemy>=2.0.0",
        "unixodbc>=1.0.0",
        "python-dotenv>=1.0.0",
        "typing>=3.7.4",
        "pytest>=8.3.3",
        "pytest-mock>=3.12.0",
    ],
    author="Fitzroy Petgrave",
    author_email="fitzroy@irecycle.world",
    description="A tool for finding and analyzing recycling services",
    keywords="recycling, environment, data engineering",
) 