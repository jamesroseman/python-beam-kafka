import setuptools


setuptools.setup(
    name='test-beam',
    version='1.0',
    install_requires=[
        "boto3",
    ],
    packages=setuptools.find_packages(),
)