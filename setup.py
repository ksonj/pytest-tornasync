import sys
import os

from setuptools import setup
from setuptools.command.test import test

import pytest_tornasync


here_dir = os.path.abspath(os.path.dirname(__file__))


# require python-3.5+, since we only support the native coroutine 'async def'
# style for tests that were introduced in python 3.5.
if sys.version_info < (3, 5):
    print("pytest-tornasync requires Python 3.5 or newer")
    sys.exit(1)


def read(*filenames):
    buf = []
    for filename in filenames:
        with open(os.path.join(here_dir, filename)) as f:
            buf.append(f.read())
    return '\n\n'.join(buf)


class PyTest(test):

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='pytest-tornasync',
    version=pytest_tornasync.__version__,
    license='http://www.opensource.org/licenses/mit-license.php',
    url='https://github.com/eukaryote/pytest-tornasync',
    description='py.test plugin for testing Python 3.5+ Tornado code',
    long_description=read('README.rst', 'CHANGES.rst'),
    keywords='testing py.test tornado',
    author='Calvin Smith',
    author_email='sapientdust+pytest-tornasync@gmail.com',
    packages=[pytest_tornasync.__name__],
    platforms='any',
    cmdclass={'test': PyTest},
    install_requires=[
        'pytest>=2.4',
        'tornado>=4.0',
    ],
    tests_require=['pytest>=2.4'],
    test_suite='tests',
    entry_points={
        'pytest11': ['tornado = pytest_tornasync.plugin'],
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Pytest',
        'Topic :: Software Development :: Testing',
    ],
)
