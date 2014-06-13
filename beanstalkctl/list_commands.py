import operator

from .base import BaseCommand
from .util import natural_sort_key



class ListCommand(BaseCommand):
    __cmd__ = 'list'
    __help__ = 'not implemented'

    def _print_tubes(self, data, title='Total'):
        print

        key = max(data.iteritems(), key=operator.itemgetter(1))[0]

        fill = data[key]
        if fill < len(title):
            fill = len(title)

        output_format = ' {0:>'+str(fill)+'} | {1}'
        sorted_data = reversed(sorted(data.iteritems(),
                                      key=operator.itemgetter(1)))

        print (' {0:>'+str(fill)+'} | Tube').format(title)
        print '-' + ('-' * fill) + '-+------'

        for tube, value in sorted_data:
            print output_format.format(value, tube)

        print



class ListTubesCommand(BaseCommand):
    __cmd__ = 'tubes'
    __help__ = "List all tubes"

    def run(self, line):
        for tube in sorted(self.beanstalkd.tubes(), key=natural_sort_key):
            print tube



class ListStatusCommand(ListCommand):
    def run(self, line):
        tubes = {}
        for tube in self.beanstalkd.tubes():
            stats = self.beanstalkd.stats_tube(tube)
            count = int(stats['current-jobs-{0}'.format(self.__cmd__)])
            if count:
                tubes[tube] = count

        if not tubes:
            print 'No tubes have {0} messages'.format(self.__cmd__)
            return

        print 'Listing tubes with {0} messages ({1})'.format(self.__cmd__,
                                                             len(tubes))

        self._print_tubes(tubes, self.__cmd__.title())



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
