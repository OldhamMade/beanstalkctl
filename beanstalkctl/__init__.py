"""
beanstalkctl -- interact with, and issue commands to, beanstalkd

Usage:
  beanstalkd [--host=<host>] [--port=<port>]

Options:
  -H --host=<host>    The beanstalkd host [default: 0.0.0.0]
  -P --port=<port>    The beanstalkd port [default: 11300]
"""
import operator

from docopt import docopt
from ishell.console import Console

from .bury_commands import *
from .clear_commands import *
from .delete_commands import *
from .kick_commands import *
from .list_commands import *
from .overview_commands import *
from .peek_commands import *
from .populate_commands import *
from .put_commands import *
from .stats_commands import *
from .uptime_commands import *
from .version_commands import *
from .whoami_commands import *

from .base import BaseCommand
from .util import apply_command_chains

from .__version__ import __version__


console = Console(prompt="beanstalkctl", prompt_delim=">")


class HelpCommand(BaseCommand):
    __cmd__ = 'help'
    __help__ = 'print this help message'

    def run(self, line):
        console.print_childs_help()


def main():
    args = docopt(__doc__, version='.'.join(__version__))

    command_chains = {
        'help': HelpCommand,
        'whoami': WhoAmICommand,
        'overview': OverviewCommand,
        'list': {
            'all': ListAllCommand,
            'urgent': ListUrgentCommand,
            'delayed': ListDelayedCommand,
            'ready': ListReadyCommand,
            'buried': ListBuriedCommand,
            'reserved': ListReservedCommand,
        },
        'peek': {
            'id': PeekByIDCommand,
            'ready': PeekReadyCommand,
            'buried': PeekBuriedCommand,
            'delayed': PeekDelayedCommand,
        },
        'stats': {
            'short': StatsCommand,
            'full': AllStatsCommand,
            'tube': TubeStatsCommand,
        },
        'put': PutCommand,
        'populate': {
            'tube': PopulateTubeCommand,
            'tubes': PopulateTubesCommand,
        },
        'delete': DeleteCommand,
        'bury': {
            'one': BuryOneCommand,
            'tube': BuryTubeCommand,
        },
        'kick': {
            'list': KickListCommand,
            'one': KickOneCommand,
            'tube': KickTubeCommand,
            'everything': KickEverythingCommand,
        },
        'clear': {
            'tube': ClearTubeCommand,
            'everything': ClearEverythingCommand,
        },
        'version': VersionCommand,
        'uptime': UptimeCommand,
    }

    apply_command_chains(console, command_chains,
                         beanstalkd_host=args['--host'],
                         beanstalkd_port=args['--port'])
    try:
        console.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
