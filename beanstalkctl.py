"""
beanstalkctl -- interact with, and issue commands to, beanstalkd

Usage:
  beanstalkd [--host=<host>] [--port=<port>]

Options:
  -H --host=<host>    The beanstalkd host [default: 0.0.0.0]
  -P --port=<port>    The beanstalkd port [default: 11300]
"""
import beanstalkc

from docopt import docopt
from ishell.console import Console
from ishell.command import Command

try:
    import re2 as re
except ImportError:
    import re


__author__ = 'Phillip B Oldham <info@oldham-made.net>'
__version__ = ('0', '1', '0')


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text
            in re.split(_nsre, s)]



class BeanstalkdMixin(object):
    """Mixin providing utility functions for
    connecting and publishing to beanstalkd"""

    beanstalkd_host = '0.0.0.0'
    beanstalkd_port = 11300

    def __get_beanstalkd_connection__(self):
        """Obtain a connection to a beanstalkd server"""
        try:
            if not hasattr(self, '_beanstalkd_connection') or \
               not self._beanstalkd_connection:
                self._beanstalkd_connection = beanstalkc.Connection(
                    host=self.beanstalkd_host,
                    port=int(self.beanstalkd_port))
            return self._beanstalkd_connection

        except beanstalkc.SocketError:
            raise Exception(
                'Unable to connect to beanstalkd on {0}:{1}'.format(
                    self.beanstalkd_host,
                    self.beanstalkd_port))

    # beanstalkd property which will reuse or create a beanstalkd connection
    beanstalkd = property(__get_beanstalkd_connection__)



class BaseCommand(Command, BeanstalkdMixin):
    def __init__(self, *args, **kwargs):
        if 'beanstalkd_host' in kwargs:
            self.beanstalkd_host = kwargs['beanstalkd_host']
            del(kwargs['beanstalkd_host'])

        if 'beanstalkd_port' in kwargs:
            self.beanstalkd_port = kwargs['beanstalkd_port']
            del(kwargs['beanstalkd_port'])

        Command.__init__(self, *args, **kwargs)



class ListCommand(BaseCommand):
    __cmd__ = 'list'
    __help__ = "List all tubes"

    def run(self, line):
        for tube in sorted(self.beanstalkd.tubes(), key=natural_sort_key):
            print tube



class AllStatsCommand(BaseCommand):
    __cmd__ = 'all-stats'
    __help__ = "Show all stats for the server"

    def run(self, line):
        stats = self.beanstalkd.stats()
        print """
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
""".format(**stats)



class StatsCommand(BaseCommand):
    __cmd__ = 'stats'
    __help__ = "Show useful stats for the server"

    def run(self, line):
        stats = self.beanstalkd.stats()
        print """
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
""".format(**stats)



class TubeStatsCommand(BaseCommand):
    __cmd__ = 'tube-stats'
    __help__ = "Show stats for a tube"

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()
        if len(args) == 1:
            print 'Please specify a tube name'
            return

        tube = args[-1]

        if tube not in self.args():
            print 'The tube "{0}" does not exist'.format(tube)
            return

        stats = self.beanstalkd.stats_tube(tube)
        print """
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
""".format(**stats)



class WhoAmICommand(BaseCommand):
    __cmd__ = 'whoami'
    __help__ = 'Show the current connection details'

    def run(self, line):
        print 'Connected to {0} on port {1}'.format(self.beanstalkd_host,
                                                    self.beanstalkd_port)


class PeekCommand(BaseCommand):
    def run(self, line):
        args = line.split()
        if not len(args) == 3:
            print 'Please specify a tube'
            return
        tube  = args[-1]

        self.beanstalkd.use(tube)
        func = getattr(self.beanstalkd, 'peek_{0}'.format(self.__cmd__))
        print func
        job = func()
        print job


class PeekReadyCommand(PeekCommand):
    __cmd__ = 'ready'
    __help__ = 'Peek at the next ready job on a tube'


class PeekBuriedCommand(PeekCommand):
    __cmd__ = 'buried'
    __help__ = 'Peek at the next buried job on a tube'


def apply_chain(console, chain, **kwargs):
    for k, v in chain.iteritems():
        if isinstance(v, dict):
            return apply_chain(console, v, **kwargs)

        cmd = v

        has_args_func = 'args' in cmd.__dict__

        instance = cmd(
            cmd.__cmd__,
            cmd.__help__,
            dynamic_args=has_args_func,
            **kwargs
        )

        console.addChild(instance)

    return console


def main():
    args = docopt(__doc__, version='.'.join(__version__))
    console = Console(prompt="beanstalk", prompt_delim=">")

    chains = {
        'peek': {
            'ready': PeekReadyCommand,
            'buried': PeekBuriedCommand,
        }
    }

    for cmd in (WhoAmICommand, ListCommand, AllStatsCommand,
                StatsCommand, TubeStatsCommand):

        has_args_func = 'args' in cmd.__dict__

        instance = cmd(
            cmd.__cmd__,
            cmd.__help__,
            beanstalkd_host=args['--host'],
            beanstalkd_port=args['--port'],
            dynamic_args=has_args_func
        )
        console.addChild(instance)

    apply_chain(console, chains,
                beanstalkd_host=args['--host'],
                beanstalkd_port=args['--port'],
            )

    try:
        console.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
