from setuptools import setup, find_packages

setup(
    name='beanstalkctl',
    version='0.3.0',
    description='beanstalkctl -- interact with, and issue commands to, beanstalkd',
    # long_description=long_description(),
    url='https://github.com/OldhamMade/beanstalkctl',
    download_url='https://github.com/OldhamMade/beanstalkctl',
    author='Phillip B Oldham',
    author_email='info@oldham-made.net',
    license='BSD',
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
