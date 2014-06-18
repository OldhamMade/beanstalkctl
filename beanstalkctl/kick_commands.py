from .base import BaseCommand
from .list_commands import ListBuriedCommand
from .util import natural_sort_key


class KickListCommand(ListBuriedCommand):
    __cmd__ = 'list'
    __help__ = 'list all tubes with buried jobs'

    def run(self, line):
        self.__cmd__ = 'buried'
        ListBuriedCommand.run(self, line)


class KickCommand(BaseCommand):
    __cmd__ = 'kick'
    __help__ = 'not implemented'

    def _kick(self, tube, count=None):
        self.beanstalkd.use(tube)

        if not count:
            # find out how many buried jobs there are
            # and kick that many, plus an additional
            # amount for good measure
            stats = self.beanstalkd.stats_tube(tube)
            count = stats['current-jobs-buried'] + 1

        # return the number of jobs that were
        # actually kicked
        return self.beanstalkd.kick(count)


class KickOneCommand(KickCommand):
    __cmd__ = 'one'
    __help__ = 'kick the next buried job on a tube'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            print 'Please specify a tube'
            return

        tube = args[-1]

        if tube not in self.beanstalkd.tubes():
            print 'Tube {0} does not exist.'.format(tube)
            return

        print '\nKicking the next buried job on tube {0}:'.format(tube)

        result = self._kick(tube, 1)

        print '  Successfully kicked {0} job{1}\n'.format(
            result,
            '' if result is 1 else 's'
        )


class KickTubeCommand(KickCommand):
    __cmd__ = 'tube'
    __help__ = 'kick all buried jobs on a tube'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            print 'Please specify a tube'
            return

        tube = args[-1]

        if tube not in self.beanstalkd.tubes():
            print 'Tube {0} does not exist.'.format(tube)
            return

        stats = self.beanstalkd.stats_tube(tube)
        total_jobs = stats['current-jobs-buried']

        print '\nYou are about to KICK all ({0}) jobs from "{1}".'.format(
            total_jobs,
            tube,
        )

        if not self.user_wants_to_continue():
            return

        print '\nKicking all buried jobs on tube {0}:'.format(tube)

        result = self._kick(tube)

        print '  Successfully kicked {0} job{1}\n'.format(
            result,
            '' if result is 1 else 's'
        )



class KickEverythingCommand(KickCommand):
    __cmd__ = 'everything'
    __help__ = 'kick all buried jobs from all tubes'

    def run(self, line):
        tubes = {}
        for tube in self.beanstalkd.tubes():
            stats = self.beanstalkd.stats_tube(tube)
            count = int(stats['current-jobs-buried'])
            if count:
                tubes[tube] = count

        total_tubes = len(tubes)
        total_jobs = sum(tubes.values())

        print '\nYou are about to KICK all ({0}) jobs from ALL tubes ({1}).'.format(
            total_jobs,
            total_tubes,
        )

        if not self.user_wants_to_continue():
            return

        print '\nKicking all buried jobs:'

        for tube in sorted(tubes.keys(), key=natural_sort_key):
            result = self._kick(tube)

            print '  successfully kicked {0} job{1} on tube {2}'.format(
                result,
                '' if result is 1 else 's',
                tube,
            )
        print
