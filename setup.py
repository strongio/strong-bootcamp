import setuptools
from bootcamp import __version__

setuptools.setup(
    name='strong-bootcamp',
    version=__version__,
    packages=[p for p in setuptools.find_packages() if 'bootcamp' in p],
    url='https://www.strong.io',
    license='',
    author='Strong Analytics',
    author_email='contact@strong.io',
    description='Framework for experimenting with and validating models pre-deployment.',
    install_requires=['pyyaml'],
    entry_points={
        'console_scripts': [
            'bootcamp=bootcamp.cli:main'
        ]
    }
)
