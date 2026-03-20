from setuptools import setup, find_packages

setup(
    name="mrich",
    version="1.3",
    author="Max Winokan",
    author_email="mwinokan@me.com",
    description="Pretty-printing wrappers around Rich",
    url="https://github.com/mwinokan/mrich",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "rich",
    ],
)
