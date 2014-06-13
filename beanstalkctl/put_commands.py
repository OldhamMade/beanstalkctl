from .base import BaseCommand


class PutCommand(BaseCommand):
    __cmd__ = 'put'
    __help__ = 'put a message onto a queue'

    def run(self, line):
        print 'Not implemented'
