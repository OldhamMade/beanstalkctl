from .base import BaseCommand


class DeleteCommand(BaseCommand):
    __cmd__ = 'delete'
    __help__ = 'not implemented'

    def run(self, line):
        print 'Not implemented'


class DeleteBuriedCommand(DeleteCommand):
    __cmd__ = 'buried'
    __help__ = 'delete the next buried job on a tube'

    def run(self, line):
        print 'Not implemented'
