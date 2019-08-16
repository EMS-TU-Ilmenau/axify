from setuptools import setup

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

name = 'axify'
version = '0.2'
author = 'S. Semper'
release = '0.2'

setup(
    author='Sebastian Semper',
    version='0.2',
    name=name,
    packages=[name],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'doc/source'),
            'build_dir': ('setup.py', 'doc/build'),
        }
    },
)
