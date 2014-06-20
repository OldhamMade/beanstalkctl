from .base import BaseCommand


class AllStatsCommand(BaseCommand):
    __cmd__ = 'full'
    __help__ = "Show all stats for the server"

    def run(self, line):
        stats = self.beanstalkd.stats()
        self.respond("""
hostname: {hostname}
pid: {pid}
uptime: {uptime}
version: {version}
max-job-size: {max-job-size}

job timeouts: {job-timeouts}
total connections: {total-connections}
total jobs: {total-jobs}

current:
  connections: {current-connections}
  waiting: {current-waiting}
  tubes: {current-tubes}
  producers: {current-producers}
  workers: {current-workers}
  jobs:
    urgent: {current-jobs-urgent}
    ready: {current-jobs-ready}
    delayed: {current-jobs-delayed}
    reserved: {current-jobs-reserved}
    buried: {current-jobs-buried}

command calls:
  use: {cmd-use}
  watch: {cmd-watch}
  put: {cmd-put}
  reserve: {cmd-reserve}
    with-timeout: {cmd-reserve-with-timeout}
  release: {cmd-release}
  delete: {cmd-delete}
  bury: {cmd-bury}
  kick: {cmd-kick}
  ignore: {cmd-ignore}
  peek: {cmd-peek}
    ready: {cmd-peek-ready}
    buried: {cmd-peek-buried}
    delayed: {cmd-peek-delayed}
  list:
    tubes: {cmd-list-tubes}
    tubes-watched: {cmd-list-tubes-watched}
    tube-used: {cmd-list-tube-used}
  pause-tube: {cmd-pause-tube}
  stats: {cmd-stats}
    job: {cmd-stats-job}
    tube: {cmd-stats-tube}
  touch: {cmd-touch}

binlog:
  max-size: {binlog-max-size}
  current-index: {binlog-current-index}
  oldest-index: {binlog-oldest-index}
  records-written: {binlog-records-written}
  records-migrated: {binlog-records-migrated}
""".format(**stats))



class StatsCommand(BaseCommand):
    __cmd__ = 'short'
    __help__ = "Show useful stats for the server"

    def run(self, line):
        stats = self.beanstalkd.stats()
        self.respond("""
hostname: {hostname}
pid: {pid}
uptime: {uptime}

total connections: {total-connections}
total jobs: {total-jobs}

current:
  connections: {current-connections}
  waiting: {current-waiting}
  tubes: {current-tubes}
  producers: {current-producers}
  workers: {current-workers}
  jobs:
    urgent: {current-jobs-urgent}
    ready: {current-jobs-ready}
    delayed: {current-jobs-delayed}
    reserved: {current-jobs-reserved}
    buried: {current-jobs-buried}
""".format(**stats))



class TubeStatsCommand(BaseCommand):
    __cmd__ = 'tube'
    __help__ = "Show stats for a tube"

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if len(args) != 3:
            self.respond('Please specify a tube name. Use `list` to view tubes.')
            return False

        tube = args[-1]

        if tube not in self.args():
            self.respond('The tube "{0}" does not exist'.format(tube))
            return False

        stats = self.beanstalkd.stats_tube(tube)
        self.respond("""
name: {name}
total jobs: {total-jobs}

current:
  watching: {current-watching}
  waiting: {current-waiting}
  using: {current-using}

current jobs:
  buried: {current-jobs-buried}
  delayed: {current-jobs-delayed}
  ready: {current-jobs-ready}
  reserved: {current-jobs-reserved}
  urgent: {current-jobs-urgent}

pause: {pause}
  time-left: {pause-time-left}
""".format(**stats))
