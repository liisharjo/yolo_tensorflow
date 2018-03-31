from setuptools import find_packages, setup

setup(
    name='trainer',
    version='0.1',
    packages=['train', 'utils', 'yolo'],
    include_package_data=True,
    description='Trainer application package.'
)
