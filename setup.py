from setuptools import *

LONG_DESC = """
An extension of `manim` for topological data analysis
"""

setup(name='manimtda',
      version='0.0.0',
      description='Topological Data Analysis in `manim`',
      long_description=LONG_DESC,
      author='Bradley Nelson & Anjan Dwaraknath',
      url='https://github.com/bnels/manimtdy',
      install_requires=['manimlib'],
      author_email='bjnelson@stanford.edu',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
