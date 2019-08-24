# This file is part of axify.

# axify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# axify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with axify. If not, see <http://www.gnu.org/licenses/>.
'''Setup script for axify installation using pip'''

#import modules
import platform
import sys
import os
import re
import subprocess
from distutils import sysconfig
from sphinx.setup_command import BuildDoc


def WARNING(string):
    print("\033[91mWARNING:\033[0m %s" % (string))


def INFO(string):
    print("\033[96mINFO:\033[0m %s" % (string))


# load setup and extensions from setuptools. If that fails, try distutils
try:
    from setuptools import setup
except ImportError:
    WARNING("Could not import setuptools.")
    raise

cmdclass = {'build_sphinx': BuildDoc}

packageName = 'axify'
name = packageName
packageVersion = '0.2'
version = packageVersion
author = 'Sebastian Semper'
release = '0.2'
strVersionFile  = "%s/version.py" %(packageName)

VERSION_PY = """
# -*- coding: utf-8 -*-
# This file carries the module's version information which will be updated
# during execution of the installation script, setup.py. Distribution tarballs
# contain a pre-generated copy of this file.

__version__ = '%s'
"""

##############################################################################
### function and class declaration section. DO NOT PUT SCRIPT CODE IN BETWEEN
##############################################################################

def getCurrentVersion():
    '''
    Determine package version and put it in the signatures.
    '''
    global packageVersion
    global fullVersion

    # check if there is a manual version override
    if os.path.isfile(".version"):
        with open(".version", "r") as f:
            stdout = f.read().split('\n')[0]
        print("Override of version string to '%s' (from .version file )" % (
            stdout))

        fullVersion = stdout

    else:
        # check if source directory is a git repository
        if not os.path.exists(".git"):
            print(("Installing from something other than a Git repository; " +
                   "Version file '%s' untouched.") % (strVersionFile))
            return

        # fetch current tag and commit description from git
        try:
            p = subprocess.Popen(
                ["git", "describe", "--tags", "--dirty", "--always"],
                stdout=subprocess.PIPE
            )
        except EnvironmentError:
            print("Not a git repository; Version file '%s' not touched." % (
                strVersionFile))
            return

        stdout = p.communicate()[0].strip()
        if stdout is not str:
            stdout = stdout.decode()

        if p.returncode != 0:
            print(("Unable to fetch version from git repository; " +
                   "leaving version file '%s' untouched.") % (strVersionFile))
            return

        fullVersion = stdout

    # output results to version string, extract package version number from
    # `fullVersion` as this string might also contain additional tags (e.g.
    # commit hashes or `-dirty` flags from git tags)
    versionMatch = re.match(r"[.+\d+]+\d*[abr]\d*", fullVersion)
    if versionMatch:
        packageVersion = versionMatch.group(0)
        print("Fetched package version number from git tag (%s)." % (
            packageVersion))

# determine requirements for install and setup
def checkRequirement(lstRequirements, importName, requirementName):
    '''
    Don't add packages unconditionally as this involves the risk of updating an
    already installed package. Sometimes this may break during install or mix
    up dependencies after install. Consider an update only if the requested
    package is not installed at all or if we are building an installation
    wheel.
    '''
    try:
        __import__(importName)
    except ImportError:
        lstRequirements.append(requirementName)
    else:
        if 'bdist_wheel' in sys.argv[1:]:
            lstRequirements.append(requirementName)

##############################################################################
### The actual script. KEEP THE `import filter` ALIVE AT ALL TIMES
##############################################################################

if __name__ == '__main__':
    # get version from git and update axify/__init__.py accordingly
    getCurrentVersion()

    # make sure there exists a version.py file in the project
    with open(strVersionFile, "w") as f:
        f.write(VERSION_PY % (fullVersion))
    print("Set %s to '%s'" % (strVersionFile, fullVersion))

    # get the long description from the README file.
    # CAUTION: Python2/3 utf encoding shit calls needs some adjustments
    fileName = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'README.md'
    )

    f = (open(fileName, 'r') if sys.version_info < (3, 0)
         else open(fileName, 'r', encoding='utf-8'))
    longDescription = f.read()
    f.close()

    print("Building %s v%s" % (
        packageName,
        packageVersion
    ))

    # check if all requirements are met prior to actually calling setup()
    setupRequires = []
    installRequires = []
    checkRequirement(setupRequires, 'setuptools', 'setuptools>=18.0')
    checkRequirement(installRequires, 'numpy', 'numpy>=1.16.4')
    checkRequirement(installRequires, 'colorfy', 'colorfy>=0.0.2')
    checkRequirement(installRequires, 'matplotlib', 'matplotlib>=3.0.3')
    checkRequirement(installRequires, 'numpydoc', 'numpydoc>=0.9.1')

    print("Requirements for setup: %s" % (setupRequires))
    print("Requirements for install: %s" % (installRequires))

    # everything's set. Fire in the hole.
    setup(
        author=author,
        version=packageVersion,
        name=packageName,
        packages=[packageName],
        scripts=['bin/axify'],
        description=('Script to convert a large numpy array to a png and ' +
        'also generate a tikzpicture, which plots the png with axes to be ' +
        'included in a TeX document.'),
        long_description=longDescription,
        url='https://github.com/EMS-TU-Ilmenau/axify',
        license='GNU General Public License 3',
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Scientific/Engineering',
        ],
        command_options={
            'build_sphinx': {
                'project': ('setup.py', name),
                'version': ('setup.py', version),
                'release': ('setup.py', release),
                'source_dir': ('setup.py', 'doc/source'),
                'build_dir': ('setup.py', 'doc/build'),
            }
        },
        setup_requires=setupRequires,
        install_requires=installRequires,
    )
