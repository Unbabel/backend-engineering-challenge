from setuptools import setup, find_packages

install_requires = ["pytest == 4.5.0", "numpy == 1.17.2", "pandas == 0.23.4"]


setup(
    name="unbabel_cli",
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    entry_points={"console_scripts": ["unbabel_cli=src.__main__:main"]},
    author="Thomas Metcalfe",
    author_email="tommetcalfe@live.com",
    description="Computes moving averages from translation data",
)
