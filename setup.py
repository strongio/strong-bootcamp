import itertools
import os
import setuptools
import sys

setup_kwargs = {}

if 'develop' in sys.argv:
    setup_kwargs['packages'] = [p for p in setuptools.find_packages() if 'bootcamp' in p]

else:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext

    # declare Cythonized extensions
    extensions = list(itertools.chain.from_iterable(
        [
            setuptools.Extension('{}.{}'.format(p, f.replace('.py', '')), [os.path.join(p.replace('.', '/'), f)])
            for f in os.listdir(p.replace('.', '/')) if f[-3:] == '.py'
        ]
        for p in setuptools.find_packages() if 'bootcamp' in p
    ))

    setup_kwargs['ext_modules'] = cythonize(
        extensions, language_level="3", build_dir="build", compiler_directives=dict(always_allow_keywords=True)
    )
    setup_kwargs['cmdclass'] = {'build_ext': build_ext}
    setup_kwargs['packages'] = []

setuptools.setup(
    **setup_kwargs
)
