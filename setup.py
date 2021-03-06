import sys

import setuptools.command.build_py
import subprocess
from distutils.spawn import find_executable
from setuptools import setup, find_packages


PY3 = (sys.version_info.major == 3)

install_requires = [
    "requests",
    "posix_ipc",
    "pyjwt",
]

tests_require = [
    "nose",
    "coverage",
    "webtest",
]

if not PY3:
    tests_require.append("mock")
    install_requires.append("enum34")

extras_require = {
    "gevent": [
        "gevent",
    ],

    "thrift": [
        "thrift",
    ],

    "pyramid": [
        "pyramid",
    ],

    "docs": [
        "sphinx",
        "sphinxcontrib-spelling",
        "alabaster",
    ],
}


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command for packaging."""

    def _make_thrift(self):
        """Generate Baseplate Thrift definitions.
        """
        # Verify build dependencies are installed.
        if not find_executable('make'):
            print("'make' not found.")
            exit(1)

        if not find_executable('thrift1'):
            print("Thrift compiler not found.")
            exit(1)

        make_cmd = ['/usr/bin/make', 'thrift']
        subprocess.check_call(make_cmd)

    def run(self):
        self._make_thrift()
        setuptools.command.build_py.build_py.run(self)


setup(
    name="baseplate",
    description="A library to build services on",
    long_description=open("README.rst").read(),
    author="Neil Williams",
    author_email="neil@reddit.com",
    license="BSD",
    url="https://baseplate.readthedocs.io/en/stable/",
    version="0.25.0",

    packages=find_packages(exclude=["tests", "tests.*"]),

    install_requires=install_requires,
    extras_require=extras_require,

    test_suite="tests",
    tests_require=tests_require,

    scripts=[
        "bin/baseplate-serve{:d}".format(sys.version_info.major),
        "bin/baseplate-script{:d}".format(sys.version_info.major),
        "bin/baseplate-tshell{:d}".format(sys.version_info.major),
    ],

    # the thrift compiler must be able to find baseplate.thrift to build
    # services which extend BaseplateService.
    package_data={
        "baseplate.thrift": [
            "*.thrift"
        ],
    },
    zip_safe=False,
    entry_points={
        "distutils.commands": [
            "build_thrift = baseplate.integration.thrift.command:BuildThriftCommand",
        ],

        "console_scripts": [
            "baseplate-healthcheck{:d} = baseplate.server.healthcheck:run_healthchecks".format(
                sys.version_info.major),
        ],

        "paste.app_factory": [
            "main = baseplate.integration.pyramid:paste_make_app",
        ],
    },

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    cmdclass={
        'build_py': BuildPyCommand,
    },
)
