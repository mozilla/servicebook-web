from setuptools import setup, find_packages
from serviceweb import __version__


setup(name='serviceweb',
      version=__version__,
      packages=find_packages(),
      description="Mozilla Service Book Web App",
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'requests',
        'flask',
        'flask-bootstrap',
        'flask-iniconfig',
        'flask-markdown',
        'flask-nav',
        'flask-pyoidc',
        'Flask-WTF',
        'PyYAML',
        'humanize',
        'boto3',
        'raven[flask]',
      ],
      entry_points="""
      [console_scripts]
      serviceweb = serviceweb.server:main
      """)
