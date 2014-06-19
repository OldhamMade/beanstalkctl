from .base import BaseCommand


class BuryCommand(BaseCommand):
    __cmd__ = 'bury'
    __help__ = 'not implemented'

    def _bury_one(self, tube):

        self.beanstalkd.watch(tube)
        print '\nBurying the next ready job on tube {0}:'.format(tube)

        job = self.beanstalkd.reserve(timeout=1)

        if not job:
            print '  No jobs to bury.'
            return False

        job.bury()

        if not job.stats()['state'] == 'buried':
            print '  Unable to bury job.'
            return False

        print '  Successfully buried job with ID {0}\n'.format(job.jid)

        return True


    def _bury_all(self, tube):

        print '\nBurying the all jobs on tube {0}:'.format(tube)

        buried_ready = 0

        self.beanstalkd.watch(tube)

        job = self.beanstalkd.reserve(timeout=1)
        while job:
            if not job:
                break

            job.bury()

            if job.stats()['state'] == 'buried':
                buried_ready += 1

            job = self.beanstalkd.reserve(timeout=1)

        print '  Successfully buried {0} ready jobs\n'.format(
            buried_ready,
            '' if buried_ready is 1 else 's'
        )

        return True


class BuryOneCommand(BuryCommand):
    __cmd__ = 'one'
    __help__ = 'bury the next ready job on a tube'

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

        return self._bury_one(tube)


class BuryByIDCommand(BuryCommand):
    __cmd__ = 'id'
    __help__ = 'bury a job by ID'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            print 'Please specify an id'
            return

        jid = args[-1]

        if not jid.isdigit():
            print 'ID must be a number'
            return

        return self._bury_id(int(jid))


class BuryTubeCommand(BuryCommand):
    __cmd__ = 'tube'
    __help__ = 'bury all jobs on a tube'

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
        total_jobs = int(stats['current-jobs-ready']) + \
                     int(stats['current-jobs-delayed'])

        print '\nYou are about to RESERVE then BURY all ready ({0}) jobs on "{1}".'.format(
            total_jobs,
            tube,
        )

        if not self.user_wants_to_continue():
            return

        return self._bury_all(tube)


