from setuptools import setup, find_packages

setup(
    name='py_lambda_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'botocore'
    ],
    python_requires='>=3.7',
)
