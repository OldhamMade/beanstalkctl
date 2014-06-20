from .base import BaseCommand


class BuryCommand(BaseCommand):
    __cmd__ = 'bury'
    __help__ = 'not implemented'

    def _bury_one(self, tube):

        self.beanstalkd.watch(tube)
        self.respond('\nBurying the next ready job on tube {0}:'.format(tube))

        job = self.beanstalkd.reserve(timeout=1)

        if not job:
            self.respond('  No jobs to bury.')
            return False

        job.bury()

        if not job.stats()['state'] == 'buried':
            self.respond('  Unable to bury job.')
            return False

        self.respond('  Successfully buried job with ID {0}\n'.format(job.jid))

        return True


    def _bury_all(self, tube):

        self.respond('\nBurying the all jobs on tube {0}:'.format(tube))

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

        self.respond('  Successfully buried {0} ready jobs\n'.format(
            buried_ready,
            '' if buried_ready is 1 else 's'
        ))

        return True


class BuryOneCommand(BuryCommand):
    __cmd__ = 'one'
    __help__ = 'bury the next ready job on a tube'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            self.respond('Please specify a tube')
            return False

        tube = args[-1]

        if tube not in self.beanstalkd.tubes():
            self.respond('Tube {0} does not exist.'.format(tube))
            return False

        return self._bury_one(tube)


class BuryByIDCommand(BuryCommand):
    __cmd__ = 'id'
    __help__ = 'bury a job by ID'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            self.respond('Please specify an id')
            return False

        jid = args[-1]

        if not jid.isdigit():
            self.respond('ID must be a number')
            return False

        return self._bury_id(int(jid))


class BuryTubeCommand(BuryCommand):
    __cmd__ = 'tube'
    __help__ = 'bury all jobs on a tube'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            self.respond('Please specify a tube')
            return False

        tube = args[-1]

        if tube not in self.beanstalkd.tubes():
            self.respond('Tube {0} does not exist.'.format(tube))
            return False

        stats = self.beanstalkd.stats_tube(tube)
        total_jobs = int(stats['current-jobs-ready']) + \
                     int(stats['current-jobs-delayed'])

        self.respond((
            '\nYou are about to RESERVE '
            'then BURY all ready ({0}) '
            'jobs on "{1}".').format(
            total_jobs,
            tube,
        ))

        if not self.user_wants_to_continue():
            return False

        return self._bury_all(tube)


