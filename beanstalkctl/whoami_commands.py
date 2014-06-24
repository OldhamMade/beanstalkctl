from .base import BaseCommand


class WhoAmICommand(BaseCommand):
    __cmd__ = 'whoami'
    __help__ = 'Show the current connection details'

    def run(self, line):
        stats = self.beanstalkd.stats()
        self.respond('Connected to {0} on port {1}'.format(
            stats['hostname'],
            self.beanstalkd_port))
