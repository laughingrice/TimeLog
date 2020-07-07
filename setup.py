import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "TimeLog",
    version = "0.1",
    author = "Micha Feigin",
    author_email = "laughingrice@gmail.com",
    description = ("Time management app"),
    license = "GPL3",
    url = "https://github.com/laughingrice/TimeLog",
    packages=["TimeLog"],
    # packages=setuptools.find_packages(),
    zip_safe=False,
    entry_points={
        "gui_scripts": [
            "TimeLog = TimeLog.TimeLog:main",
        ]
    },
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
