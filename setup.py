import setuptools

setuptools.setup(
    name='strong-bootcamp',
    version='0.1',
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
