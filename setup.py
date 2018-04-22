from os import path
import setuptools

# automatically generate requirements
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'bootcamp/requirements.txt')) as f:
    requirements = f.read().split("\n")

    # anticipating this bug in the future:
    requirements = [r for r in requirements if 'bootcamp' not in r]

setuptools.setup(
    name='strong-bootcamp',
    version='0.1',
    packages=[p for p in setuptools.find_packages() if 'bootcamp' in p],
    url='https://www.strong.io',
    license='',
    author='Strong Analytics',
    author_email='contact@strong.io',
    description='Framework for experimenting with and validating models pre-deployment.',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'bootcamp=bootcamp.cli.entry:main'
        ]
    }
)
