from .base import BaseCommand

from __version__ import __version__

class VersionCommand(BaseCommand):
    __cmd__ = 'version'
    __help__ = 'Show the current beanstalkctl version'

    def run(self, line):
        self.respond('beanstalkctl version: {0}'.format(__version__))
