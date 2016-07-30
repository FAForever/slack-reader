import os
import codecs

from setuptools import setup

import slackviewer


def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, filename), 'r').read()


install_requires = read("requirements.txt").split()
long_description = read('README.md')


setup(
    name="slack-public-viewer",
    version=slackviewer.__version__,
    url='https://github.com/cheyans/slack-export-viewer',
    license='MIT License',
    author='Cheyan Setayesh',
    author_email='cheyan.set@gmail.com',
    description=('Slack Team Publicizer Viewer'),
    long_description=long_description,
    packages=["slackviewer"],
    install_requires = install_requires,
    entry_points={'console_scripts': [
        'slack-export-viewer = slackviewer.main:main'
    ]},
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
)
