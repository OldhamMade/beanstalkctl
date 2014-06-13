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

from .delete_commands import *
from .kick_commands import *
from .list_commands import *
from .overview_commands import *
from .peek_commands import *
from .put_commands import *
from .stats_commands import *
from .whoami_commands import *

from util import apply_command_chains


__author__ = 'Phillip B Oldham <info@oldham-made.net>'
__version__ = ('0', '1', '0')


def main():
    args = docopt(__doc__, version='.'.join(__version__))
    console = Console(prompt="beanstalk", prompt_delim=">")

    command_chains = {
        'whoami': WhoAmICommand,
        'overview': OverviewCommand,
        'list': {
            'tubes': ListTubesCommand,
            'urgent': ListUrgentCommand,
            'delayed': ListDelayedCommand,
            'ready': ListReadyCommand,
            'buried': ListBuriedCommand,
        },
        'peek': {
            'id': PeekByIDCommand,
            'ready': PeekReadyCommand,
            'buried': PeekBuriedCommand,
        },
        'stats': {
            'short': StatsCommand,
            'full': AllStatsCommand,
            'tube': TubeStatsCommand,
        },
        'put': PutCommand,
        'delete': {
            'buried': DeleteBuriedCommand,
        },
        'kick': {
            'list': KickListCommand,
            'one': KickOneCommand,
            'tube': KickTubeCommand,
            'everything': KickEverythingCommand,
        },
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
