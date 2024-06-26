from setuptools import setup, find_packages


# Define your package details
PACKAGE_NAME = 'test_beam_pipelines'
PACKAGE_VERSION = '0.0.1'
DESCRIPTION = 'Test Beam pipelines.'
REQUIREMENTS = [
    'apache-beam',
    'boto3',  # Add boto3 to your requirements
]

# Standard setup
setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)
