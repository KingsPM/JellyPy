from setuptools import setup

setup(name='pyCIPAPI',
      version='0.1.0',
      description='Python library for access the GELs CPI API',
      url='https://github.com/NHS-NGS/JellyPy',
      packages=['pyCIPAPI'],
      install_requires=[
          'docopt == 0.6.2',
          'Flask == 1.0.3',
          'GelReportModels == 7.2.10',
          'maya == 0.6.1',
          'PyJWT == 1.7.1',
          'requests == 2.22.0'
      ]
      )