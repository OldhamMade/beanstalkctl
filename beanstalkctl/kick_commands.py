from .base import BaseCommand


class KickListCommand(BaseCommand):
    __cmd__ = 'list'
    __help__ = 'list all tubes with buried jobs'

    def run(self, line):
        print 'Not implemented'



class KickOneCommand(BaseCommand):
    __cmd__ = 'one'
    __help__ = 'kick the next buried job on a tube'

    def run(self, line):
        print 'Not implemented'



class KickTubeCommand(BaseCommand):
    __cmd__ = 'tube'
    __help__ = 'kick all buried jobs on a tube'

    def run(self, line):
        print 'Not implemented'



class KickEverythingCommand(BaseCommand):
    __cmd__ = 'everything'
    __help__ = 'kick all buried jobs from all tubes'

    def run(self, line):
        print 'Not implemented'
