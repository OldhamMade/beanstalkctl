from .base import BaseCommand

class UptimeCommand(BaseCommand):
    __cmd__ = 'uptime'
    __help__ = 'Show the beanstalkd instance uptime'

    def run(self, line):
        stats = self.beanstalkd.stats()
        self.respond('beanstalkd uptime: {0}'.format(
            self._format_uptime(stats['uptime'])))
