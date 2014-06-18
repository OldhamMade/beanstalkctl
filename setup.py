from setuptools import setup, find_packages

from beanstalkctl.__version__ import __author__, __version__, __licence__
import beanstalkctl

setup(
    name='beanstalkctl',
    version='.'.join(str(i) for i in __version__),
    #description=beanstalkctl.__doc__.strip(),
    # long_description=long_description(),
    url='https://github.com/OldhamMade/beanstalkctl',
    download_url='https://github.com/OldhamMade/beanstalkctl',
    author=__author__,
    author_email='info@oldham-made.net',
    license=__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'beanstalkctl = beanstalkctl:main',
        ],
    },
    install_requires=[
        'beanstalkc',
        'docopt',
        'ishell',
        'PyYAML',
    ],
    # classifiers=[
    #     'Development Status :: 5 - Production/Stable',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 2',
    #     'Programming Language :: Python :: 2.6',
    #     'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.1',
    #     'Programming Language :: Python :: 3.2',
    #     'Programming Language :: Python :: 3.3',
    #     'Programming Language :: Python :: 3.4',
    #     'Environment :: Console',
    #     'Intended Audience :: Developers',
    #     'Intended Audience :: System Administrators',
    #     'License :: OSI Approved :: BSD License',
    #     'Topic :: Internet :: WWW/HTTP',
    #     'Topic :: Software Development',
    #     'Topic :: System :: Networking',
    #     'Topic :: Terminals',
    #     'Topic :: Text Processing',
    #     'Topic :: Utilities'
    # ],
)
