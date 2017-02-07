import io
import os
from setuptools import setup

__dir__ = os.path.dirname(__file__)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


readme = read('README.rst')


setup(
    name='flake8-line-trailing-commas',
    author='Jeremy Robin',
    author_email='jeremy@talentpair.com',
    maintainer='Jeremy Robin',
    maintainer_email='jeremy@talentpair.com',
    version='0.0.1',
    install_requires=['flake8>=2, <4.0.0'],
    url='https://github.com/talentpair/flake8-line-trailing-commas/',
    long_description=readme,
    description='Flake8 lint for preventing lines ending with a comma',
    packages=['flake8_line_trailing_commas'],
    include_package_data=True,
    entry_points={
        'flake8.extension': [
            'C81 = flake8_line_trailing_commas:CommaChecker',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Framework :: Flake8',
    ],
)
