from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vbftool',

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version='1.0a0',

    description='Versatile Binary Format Tool',

    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/dsch/vbftool',

    author='David Schneider',
    author_email='schneidav81@gmail.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=['vbftool'],

    python_requires='>=3.5',
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest'],
    },

    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={
        'Bug Reports': 'https://github.com/dsch/vbftool/issues',
        'Source': 'https://github.com/dsch/vbftool',
        'Continuous Integration': 'https://travis-ci.org/dsch/vbftool',
    },
)
