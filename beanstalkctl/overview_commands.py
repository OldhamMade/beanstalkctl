from .base import BaseCommand


class OverviewCommand(BaseCommand):
    __cmd__ = 'overview'
    __help__ = 'an overview of the current status'

    def run(self, line):
        stats = self.beanstalkd.stats()
        stats['uptime'] = self._format_uptime(stats['uptime'])
        self.respond("""
Hostname: {hostname}
Pid: {pid}
Uptime: {uptime}
Tubes: {current-tubes}

Connections: {total-connections} (total)
  Producers: {current-producers} (current)
    Workers: {current-workers} (current)

Jobs:
    Urgent: {current-jobs-urgent}
     Ready: {current-jobs-ready}
   Delayed: {current-jobs-delayed}
  Reserved: {current-jobs-reserved}
    Buried: {current-jobs-buried}
""".format(**stats))
