from setuptools import setup

setup(
  name='core',
  version='1.0',
  description='Analises a datastrem input file in order to compute the average delivery time for each minutes based on a given window size',
  author='J. Pedro Oliveira',
  author_email='j.pedrodiasoliveira@gmail.com',
  packages=[],
  install_requires=[],
  entry_points={
    'console_scripts': [
      'unbabel_cli=core_cli:run'
    ]
  }
)
