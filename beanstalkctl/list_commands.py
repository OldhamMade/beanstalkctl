from collections import namedtuple

from .base import BaseCommand
from .util import natural_sort_key



class ListCommand(BaseCommand):
    __cmd__ = 'list'
    __help__ = 'not implemented'



class ListAllCommand(ListCommand):
    __cmd__ = 'all'
    __help__ = "List all tubes"

    def run(self, line):
        titles = ('urgent', 'ready', 'delayed', 'buried', 'reserved')
        Row = namedtuple('Row', ('Tube',) + tuple(t.title() for t in titles))

        data = []
        for tube in sorted(self.beanstalkd.tubes(), key=natural_sort_key):
            stats = self.beanstalkd.stats_tube(tube)
            data.append(Row(
                *[tube] + [stats['current-jobs-{0}'.format(t)] for t in titles]
            ))

        print
        self.print_table(data)
        print



class ListStatusCommand(ListCommand):
    def run(self, line):
        Row = namedtuple('Row', ('Tube', self.__cmd__.title()))

        data = []
        total_jobs = 0
        for tube in sorted(self.beanstalkd.tubes(), key=natural_sort_key):
            stats = self.beanstalkd.stats_tube(tube)
            count = int(stats['current-jobs-{0}'.format(self.__cmd__)])
            if count:
                data.append(Row(tube, count))
                total_jobs += count

        if not data:
            print 'No tubes have {0} messages'.format(self.__cmd__)
            return

        total_tubes = len(data)

        print
        self.print_table(data)
        print "\nTotal:\n  {0} {1} job{2} across {3} tube{4}\n".format(
            total_jobs,
            self.__cmd__,
            '' if total_jobs == 1 else 's',
            total_tubes,
            '' if total_tubes == 1 else 's',
        )



class ListReadyCommand(ListStatusCommand):
    __cmd__ = 'ready'
    __help__ = "List all tubes with ready jobs"


class ListBuriedCommand(ListStatusCommand):
    __cmd__ = 'buried'
    __help__ = "List all tubes with buried jobs"


class ListUrgentCommand(ListStatusCommand):
    __cmd__ = 'urgent'
    __help__ = "List all tubes with urgent jobs"


class ListDelayedCommand(ListStatusCommand):
    __cmd__ = 'delayed'
    __help__ = "List all tubes with delayed jobs"


class ListReservedCommand(ListStatusCommand):
    __cmd__ = 'reserved'
    __help__ = "List all tubes with reserved jobs"
